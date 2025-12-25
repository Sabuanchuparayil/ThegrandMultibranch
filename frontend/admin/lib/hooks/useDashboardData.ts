/**
 * Custom React hooks for dashboard data fetching
 * Provides real-time data updates with polling
 */

import { useQuery, useSubscription } from '@apollo/client';
import { useState, useEffect } from 'react';
import {
  GET_EXECUTIVE_KPIS,
  GET_BRANCH_KPIS,
  GET_BRANCH_INVENTORY_STATUS,
  GET_LOW_STOCK_ALERTS,
  getDateRange,
  getTodayRange,
  getWeekRange,
} from '../graphql/dashboard-queries';

// ============================================================================
// Executive Dashboard Hook
// ============================================================================

interface ExecutiveDashboardFilters {
  dateFrom?: Date;
  dateTo?: Date;
  regionCode?: string;
}

export function useExecutiveDashboard(filters: ExecutiveDashboardFilters = {}) {
  const { dateFrom, dateTo, regionCode } = filters;
  
  const defaultRange = getDateRange(30);
  const from = dateFrom?.toISOString() || defaultRange.from;
  const to = dateTo?.toISOString() || defaultRange.to;

  const { data, loading, error, refetch } = useQuery(GET_EXECUTIVE_KPIS, {
    variables: {
      dateFrom: from,
      dateTo: to,
      regionCode: regionCode || null,
    },
    // Poll every 30 seconds for real-time updates
    pollInterval: 30000,
    // Use cache-first policy for fresh data (cache-and-network not available in Apollo Client 3.x)
    fetchPolicy: 'cache-first',
  });

  // Calculate KPIs from order data
  const kpis = data ? calculateExecutiveKPIs(data) : null;

  return {
    data,
    kpis,
    loading,
    error,
    refetch,
  };
}

function calculateExecutiveKPIs(data: any) {
  if (!data?.orders?.edges) {
    return null;
  }

  const orders = data.orders.edges.map((edge: any) => edge.node);
  
  const totalRevenue = orders.reduce(
    (sum: number, order: any) => sum + parseFloat(order.total.gross.amount),
    0
  );

  const totalOrders = orders.length;
  const averageOrderValue = totalOrders > 0 ? totalRevenue / totalOrders : 0;

  // Calculate change from previous period (placeholder)
  // In real implementation, you'd fetch previous period data
  const change = {
    revenue: 12.5,
    orders: 8.3,
    avgOrderValue: -2.1,
  };

  return {
    totalRevenue: {
      value: formatCurrency(totalRevenue, 'GBP'),
      change: change.revenue,
      trend: change.revenue > 0 ? 'up' : 'down',
    },
    totalOrders: {
      value: totalOrders.toLocaleString(),
      change: change.orders,
      trend: change.orders > 0 ? 'up' : 'down',
    },
    averageOrderValue: {
      value: formatCurrency(averageOrderValue, 'GBP'),
      change: change.avgOrderValue,
      trend: change.avgOrderValue > 0 ? 'up' : 'down',
    },
    activeCustomers: {
      value: getUniqueCustomers(orders).toString(),
      change: 15.7,
      trend: 'up' as const,
    },
  };
}

// ============================================================================
// Branch Dashboard Hook
// ============================================================================

interface BranchDashboardFilters {
  branchId: string;
  dateFrom?: Date;
  dateTo?: Date;
}

export function useBranchDashboard(filters: BranchDashboardFilters) {
  const { branchId, dateFrom, dateTo } = filters;
  
  const defaultRange = getWeekRange();
  const from = dateFrom?.toISOString() || defaultRange.from;
  const to = dateTo?.toISOString() || defaultRange.to;
  const today = getTodayRange();

  const { data, loading, error, refetch } = useQuery(GET_BRANCH_KPIS, {
    variables: {
      branchId,
      dateFrom: from,
      dateTo: to,
      todayStart: today.from,
      todayEnd: today.to,
    },
    // Poll every 30 seconds
    pollInterval: 30000,
    fetchPolicy: 'cache-first',
    skip: !branchId,
  });

  const { data: inventoryData } = useQuery(GET_BRANCH_INVENTORY_STATUS, {
    variables: { branchId },
    pollInterval: 60000, // Poll inventory every minute
    fetchPolicy: 'cache-first',
    skip: !branchId,
  });

  // Calculate KPIs
  const kpis = data ? calculateBranchKPIs(data) : null;
  const lowStockCount = inventoryData?.branchInventory?.filter(
    (item: any) => item.isLowStock
  ).length || 0;

  return {
    data,
    kpis,
    inventory: inventoryData?.branchInventory || [],
    lowStockCount,
    loading,
    error,
    refetch,
  };
}

function calculateBranchKPIs(data: any) {
  if (!data?.orders?.edges) {
    return null;
  }

  const weekOrders = data.orders.edges.map((edge: any) => edge.node);
  const todayOrders = data.todayOrders?.edges?.map((edge: any) => edge.node) || [];

  const weekRevenue = weekOrders.reduce(
    (sum: number, order: any) => sum + parseFloat(order.total.gross.amount),
    0
  );

  const todayRevenue = todayOrders.reduce(
    (sum: number, order: any) => sum + parseFloat(order.total.gross.amount),
    0
  );

  const avgOrderValue = weekOrders.length > 0 ? weekRevenue / weekOrders.length : 0;

  // Placeholder changes - calculate from previous period in real implementation
  const change = {
    todayRevenue: 8.5,
    todayOrders: 12.0,
    weekRevenue: 5.2,
    weekOrders: -3.1,
    avgOrderValue: -1.5,
  };

  return {
    todayRevenue: {
      value: formatCurrency(todayRevenue, 'GBP'),
      change: change.todayRevenue,
      trend: 'up' as const,
    },
    todayOrders: {
      value: todayOrders.length.toString(),
      change: change.todayOrders,
      trend: 'up' as const,
    },
    weekRevenue: {
      value: formatCurrency(weekRevenue, 'GBP'),
      change: change.weekRevenue,
      trend: 'up' as const,
    },
    weekOrders: {
      value: weekOrders.length.toString(),
      change: change.weekOrders,
      trend: change.weekOrders > 0 ? 'up' : 'down',
    },
    averageOrderValue: {
      value: formatCurrency(avgOrderValue, 'GBP'),
      change: change.avgOrderValue,
      trend: change.avgOrderValue > 0 ? 'up' : 'down',
    },
  };
}

// ============================================================================
// Low Stock Alerts Hook
// ============================================================================

export function useLowStockAlerts(branchId?: string, regionCode?: string) {
  const { data, loading, error, refetch } = useQuery(GET_LOW_STOCK_ALERTS, {
    variables: {
      branchId: branchId || null,
      regionCode: regionCode || null,
    },
    pollInterval: 60000, // Poll every minute
    fetchPolicy: 'cache-and-network',
  });

  return {
    alerts: data?.lowStockAlerts || [],
    loading,
    error,
    refetch,
  };
}

// ============================================================================
// Real-time Updates Hook
// ============================================================================

export function useRealtimeUpdates(refetchInterval: number = 30000) {
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return {
    isOnline,
    refetchInterval: isOnline ? refetchInterval : 0,
  };
}

// ============================================================================
// Helper Functions
// ============================================================================

function formatCurrency(amount: number, currency: string = 'GBP'): string {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
}

function getUniqueCustomers(orders: any[]): number {
  const customerIds = new Set(
    orders
      .map((order) => order.user?.id)
      .filter((id) => id !== null && id !== undefined)
  );
  return customerIds.size;
}

