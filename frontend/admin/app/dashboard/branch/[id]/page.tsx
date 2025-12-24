/**
 * Branch Dashboard Page
 * Branch-specific KPIs and metrics
 */
'use client';

import React, { useState } from 'react';
import { useQuery } from '@apollo/client';
import { useParams, useRouter } from 'next/navigation';
import { KPICard, KPIData } from '@/components/dashboard/KPICard';
import { SalesChart, SalesDataPoint } from '@/components/dashboard/SalesChart';
import { RealTimeIndicator } from '@/components/dashboard/RealTimeIndicator';
import {
  GET_BRANCH_KPIS,
  GET_SALES_CHART_DATA,
  GET_TOP_PRODUCTS,
  GET_BRANCH_INVENTORY_STATUS,
} from '@/lib/graphql/dashboard-queries';

export default function BranchDashboardPage() {
  const params = useParams();
  const router = useRouter();
  const branchId = params.id as string;

  const [dateRange, setDateRange] = useState({
    start: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    end: new Date().toISOString().split('T')[0],
  });
  const [selectedPeriod, setSelectedPeriod] = useState('30d');
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  // Calculate today's date range
  const getTodayRange = () => {
    const today = new Date();
    const start = new Date(today);
    start.setHours(0, 0, 0, 0);
    const end = new Date(today);
    end.setHours(23, 59, 59, 999);
    return {
      todayStart: start.toISOString(),
      todayEnd: end.toISOString(),
    };
  };

  const todayRange = getTodayRange();

  // Fetch branch KPIs
  const { data: kpisData, loading: kpisLoading, error: kpisError } = useQuery(GET_BRANCH_KPIS, {
    variables: {
      branchId: branchId,
      dateFrom: dateRange.start,
      dateTo: dateRange.end,
      todayStart: todayRange.todayStart,
      todayEnd: todayRange.todayEnd,
    },
    skip: !branchId,
    pollInterval: 60000, // Refresh every minute
    onCompleted: () => setLastUpdate(new Date()),
  });

  // Calculate date range from period
  const getPeriodDates = (period: string) => {
    const now = new Date();
    const to = now.toISOString();
    const from = new Date(now);
    
    switch (period) {
      case '7d':
        from.setDate(from.getDate() - 7);
        break;
      case '30d':
        from.setDate(from.getDate() - 30);
        break;
      case '90d':
        from.setDate(from.getDate() - 90);
        break;
      case '1y':
        from.setDate(from.getDate() - 365);
        break;
      default:
        from.setDate(from.getDate() - 30);
    }
    
    return {
      dateFrom: from.toISOString(),
      dateTo: to,
    };
  };

  const periodDates = getPeriodDates(selectedPeriod);

  // Fetch sales chart data for branch
  const { data: chartData } = useQuery(GET_SALES_CHART_DATA, {
    variables: {
      branchId: branchId,
      dateFrom: periodDates.dateFrom,
      dateTo: periodDates.dateTo,
    },
    skip: !branchId,
    pollInterval: 60000,
  });

  // Fetch inventory status for branch
  const { data: inventoryData } = useQuery(GET_BRANCH_INVENTORY_STATUS, {
    variables: {
      branchId: branchId,
    },
    skip: !branchId,
    pollInterval: 60000,
  });

  // Fetch top products
  const { data: productsData } = useQuery(GET_TOP_PRODUCTS, {
    variables: {
      branchId: branchId,
      limit: 10,
      startDate: dateRange.start,
      endDate: dateRange.end,
    },
    skip: !branchId,
    pollInterval: 60000,
  });

  const kpis: KPIData[] = kpisData?.branchKpis || [];
  const salesData: SalesDataPoint[] = chartData?.salesChartData || [];
  const topProducts = productsData?.topProducts || [];

  if (kpisLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-lg text-gray-600">Loading branch dashboard...</div>
      </div>
    );
  }

  if (kpisError) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-red-600">Error loading dashboard: {kpisError.message}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <button
              onClick={() => router.back()}
              className="text-blue-600 hover:text-blue-800 mb-2 flex items-center"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Executive Dashboard
            </button>
            <h1 className="text-3xl font-bold text-gray-900">Branch Dashboard</h1>
            <p className="mt-2 text-gray-600">Performance metrics and KPIs for this branch</p>
          </div>
          <RealTimeIndicator lastUpdate={lastUpdate} />
        </div>

        {/* Date Range Selector */}
        <div className="mb-6 flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-gray-700">From:</label>
            <input
              type="date"
              value={dateRange.start}
              onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
          </div>
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-gray-700">To:</label>
            <input
              type="date"
              value={dateRange.end}
              onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
          </div>
          <div className="flex space-x-2">
            {['7d', '30d', '90d', '1y'].map((period) => (
              <button
                key={period}
                onClick={() => setSelectedPeriod(period)}
                className={`px-4 py-2 rounded-md text-sm font-medium ${
                  selectedPeriod === period
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                {period.toUpperCase()}
              </button>
            ))}
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {kpis.map((kpi, index) => (
            <KPICard key={index} {...kpi} />
          ))}
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Sales Chart */}
          <div className="lg:col-span-2">
            <SalesChart data={salesData} type="area" height={350} showOrders />
          </div>
        </div>

        {/* Inventory and Products Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Inventory Status */}
          {inventoryData?.inventoryStatus && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Inventory Status</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-gray-600">Total Items</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {inventoryData.inventoryStatus.totalItems}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Low Stock</p>
                  <p className="text-2xl font-bold text-yellow-600">
                    {inventoryData.inventoryStatus.lowStockItems}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Out of Stock</p>
                  <p className="text-2xl font-bold text-red-600">
                    {inventoryData.inventoryStatus.outOfStockItems}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-600">Total Value</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {new Intl.NumberFormat('en-US', {
                      style: 'currency',
                      currency: inventoryData.inventoryStatus.currency || 'GBP',
                    }).format(inventoryData.inventoryStatus.totalValue)}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Top Products */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900">Top Products</h3>
            </div>
            <div className="p-6">
              {topProducts.length > 0 ? (
                <div className="space-y-4">
                  {topProducts.map((product: any, index: number) => (
                    <div key={product.productId || index} className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-900">{product.productName}</p>
                        <p className="text-xs text-gray-500">Qty: {product.quantity}</p>
                      </div>
                      <p className="text-sm font-medium text-gray-900">
                        {new Intl.NumberFormat('en-US', {
                          style: 'currency',
                          currency: product.currency || 'GBP',
                        }).format(product.sales)}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500">No product data available</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
