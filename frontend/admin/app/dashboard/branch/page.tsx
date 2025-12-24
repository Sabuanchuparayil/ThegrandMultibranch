'use client';

import { useState, useEffect, Suspense } from 'react';
import { useQuery, gql } from '@apollo/client';
import {
  ChartBarIcon,
  CurrencyDollarIcon,
  ShoppingBagIcon,
  UserGroupIcon,
  CubeIcon,
  ExclamationTriangleIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
} from '@heroicons/react/24/outline';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { useSearchParams } from 'next/navigation';

// GraphQL Queries
const GET_BRANCH_KPIS = gql`
  query GetBranchKPIs($branchId: ID!, $dateFrom: DateTime, $dateTo: DateTime) {
    branch(id: $branchId) {
      id
      name
      code
    }
    
    # Branch-specific KPIs
    # Implement based on your GraphQL schema
  }
`;

const GET_BRANCH_INVENTORY_STATUS = gql`
  query GetBranchInventoryStatus($branchId: ID!) {
    branchInventory(branchId: $branchId, lowStockOnly: false) {
      id
      quantity
      availableQuantity
      isLowStock
      productVariant {
        name
        sku
      }
    }
  }
`;

const GET_BRANCH_SALES_TREND = gql`
  query GetBranchSalesTrend($branchId: ID!, $days: Int!) {
    # Sales trend for this branch
    # This query will be implemented when the backend schema is ready
    orders(
      filter: {
        # Add branch filter when available
      }
      first: 100
    ) {
      totalCount
      edges {
        node {
          id
          number
          total {
            gross {
              amount
            }
          }
        }
      }
    }
  }
`;

// KPI Card Component (reused from executive dashboard)
interface KPICardProps {
  title: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  icon: React.ComponentType<{ className?: string }>;
  trend?: 'up' | 'down' | 'neutral';
  color?: string;
}

function KPICard({ title, value, change, changeLabel, icon: Icon, trend, color = 'blue' }: KPICardProps) {
  const trendColors = {
    up: 'text-green-600',
    down: 'text-red-600',
    neutral: 'text-gray-600',
  };

  const bgColors = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    purple: 'bg-purple-500',
    orange: 'bg-orange-500',
    red: 'bg-red-500',
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
          {change !== undefined && (
            <div className="flex items-center mt-2">
              {trend === 'up' && <ArrowTrendingUpIcon className={`h-4 w-4 ${trendColors.up} mr-1`} />}
              {trend === 'down' && <ArrowTrendingDownIcon className={`h-4 w-4 ${trendColors.down} mr-1`} />}
              <span className={`text-sm font-medium ${trend ? trendColors[trend] : 'text-gray-600'}`}>
                {change > 0 ? '+' : ''}{change}% {changeLabel}
              </span>
            </div>
          )}
        </div>
        <div className={`${bgColors[color as keyof typeof bgColors] || bgColors.blue} p-3 rounded-lg`}>
          <Icon className="h-8 w-8 text-white" />
        </div>
      </div>
    </div>
  );
}

// Dashboard Page Component (Inner component that uses searchParams)
function BranchDashboardContent() {
  const searchParams = useSearchParams();
  const branchId = searchParams.get('branchId') || '1'; // Default or from URL
  
  const [dateRange, setDateRange] = useState({
    from: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000), // 7 days ago
    to: new Date(),
  });

  // Mock data - Replace with actual GraphQL queries
  const branchInfo = {
    name: 'London - Mayfair',
    code: 'LON-001',
    region: 'UK',
  };

  const kpis = {
    todayRevenue: {
      value: '£45,250',
      change: 8.5,
      trend: 'up' as const,
    },
    todayOrders: {
      value: '23',
      change: 12.0,
      trend: 'up' as const,
    },
    weekRevenue: {
      value: '£285,000',
      change: 5.2,
      trend: 'up' as const,
    },
    weekOrders: {
      value: '142',
      change: -3.1,
      trend: 'down' as const,
    },
    inventoryValue: {
      value: '£1,250,000',
      change: 2.8,
      trend: 'up' as const,
    },
    lowStockItems: {
      value: '8',
      change: -25.0,
      trend: 'up' as const,
    },
    averageOrderValue: {
      value: '£2,007',
      change: -1.5,
      trend: 'down' as const,
    },
    clickCollectOrders: {
      value: '15',
      change: 20.0,
      trend: 'up' as const,
    },
  };

  // Mock chart data
  const dailySalesData = [
    { day: 'Mon', sales: 32000, orders: 18, walkIn: 12, online: 6 },
    { day: 'Tue', sales: 38000, orders: 22, walkIn: 15, online: 7 },
    { day: 'Wed', sales: 41000, orders: 24, walkIn: 16, online: 8 },
    { day: 'Thu', sales: 45000, orders: 26, walkIn: 18, online: 8 },
    { day: 'Fri', sales: 52000, orders: 30, walkIn: 20, online: 10 },
    { day: 'Sat', sales: 68000, orders: 38, walkIn: 25, online: 13 },
    { day: 'Sun', sales: 59000, orders: 34, walkIn: 22, online: 12 },
  ];

  const hourlySalesData = Array.from({ length: 12 }, (_, i) => ({
    hour: `${9 + i}:00`,
    sales: Math.floor(Math.random() * 5000) + 2000,
    customers: Math.floor(Math.random() * 10) + 5,
  }));

  const categoryPerformanceData = [
    { category: 'Rings', sales: 85000, units: 42, avgPrice: 2024 },
    { category: 'Necklaces', sales: 72000, units: 28, avgPrice: 2571 },
    { category: 'Earrings', sales: 55000, units: 65, avgPrice: 846 },
    { category: 'Bracelets', sales: 38000, units: 25, avgPrice: 1520 },
    { category: 'Others', sales: 35000, units: 18, avgPrice: 1944 },
  ];

  // Low stock items
  const lowStockItems = [
    { name: '18K Gold Ring - Size 6', currentStock: 3, threshold: 10, sku: 'RING-18K-6' },
    { name: 'Diamond Necklace - 1ct', currentStock: 2, threshold: 8, sku: 'NECK-DIA-1CT' },
    { name: 'Platinum Earrings', currentStock: 5, threshold: 12, sku: 'EARR-PLT-STD' },
    { name: '22K Gold Bracelet', currentStock: 4, threshold: 10, sku: 'BRAC-22K-STD' },
  ];

  // Refresh data every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      // Refetch data
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{branchInfo.name}</h1>
              <p className="text-gray-600 mt-1">Branch Code: {branchInfo.code} • Region: {branchInfo.region}</p>
            </div>
            <div className="flex gap-4 items-center">
              <input
                type="date"
                value={dateRange.from.toISOString().split('T')[0]}
                onChange={(e) => setDateRange({ ...dateRange, from: new Date(e.target.value) })}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <span className="text-gray-600">to</span>
              <input
                type="date"
                value={dateRange.to.toISOString().split('T')[0]}
                onChange={(e) => setDateRange({ ...dateRange, to: new Date(e.target.value) })}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <KPICard
            title="Today's Revenue"
            value={kpis.todayRevenue.value}
            change={kpis.todayRevenue.change}
            changeLabel="vs yesterday"
            trend={kpis.todayRevenue.trend}
            icon={CurrencyDollarIcon}
            color="green"
          />
          <KPICard
            title="Today's Orders"
            value={kpis.todayOrders.value}
            change={kpis.todayOrders.change}
            changeLabel="vs yesterday"
            trend={kpis.todayOrders.trend}
            icon={ShoppingBagIcon}
            color="blue"
          />
          <KPICard
            title="Week Revenue"
            value={kpis.weekRevenue.value}
            change={kpis.weekRevenue.change}
            changeLabel="vs last week"
            trend={kpis.weekRevenue.trend}
            icon={ChartBarIcon}
            color="purple"
          />
          <KPICard
            title="Week Orders"
            value={kpis.weekOrders.value}
            change={kpis.weekOrders.change}
            changeLabel="vs last week"
            trend={kpis.weekOrders.trend}
            icon={ShoppingBagIcon}
            color="orange"
          />
          <KPICard
            title="Inventory Value"
            value={kpis.inventoryValue.value}
            change={kpis.inventoryValue.change}
            changeLabel="vs last month"
            trend={kpis.inventoryValue.trend}
            icon={CubeIcon}
            color="blue"
          />
          <KPICard
            title="Low Stock Items"
            value={kpis.lowStockItems.value}
            change={kpis.lowStockItems.change}
            changeLabel="vs last week"
            trend={kpis.lowStockItems.trend}
            icon={ExclamationTriangleIcon}
            color="red"
          />
          <KPICard
            title="Avg Order Value"
            value={kpis.averageOrderValue.value}
            change={kpis.averageOrderValue.change}
            changeLabel="vs last week"
            trend={kpis.averageOrderValue.trend}
            icon={ChartBarIcon}
            color="purple"
          />
          <KPICard
            title="Click & Collect"
            value={kpis.clickCollectOrders.value}
            change={kpis.clickCollectOrders.change}
            changeLabel="vs last week"
            trend={kpis.clickCollectOrders.trend}
            icon={UserGroupIcon}
            color="orange"
          />
        </div>

        {/* Charts Row 1: Daily Sales & Hourly Performance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Daily Sales Trend */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Daily Sales Trend (This Week)</h2>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={dailySalesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Area
                  yAxisId="left"
                  type="monotone"
                  dataKey="sales"
                  stroke="#3B82F6"
                  fill="#3B82F6"
                  fillOpacity={0.6}
                  name="Sales (£)"
                />
                <Area
                  yAxisId="right"
                  type="monotone"
                  dataKey="orders"
                  stroke="#10B981"
                  fill="#10B981"
                  fillOpacity={0.6}
                  name="Orders"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Hourly Performance Today */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Hourly Performance (Today)</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={hourlySalesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Bar yAxisId="left" dataKey="sales" fill="#3B82F6" name="Sales (£)" />
                <Bar yAxisId="right" dataKey="customers" fill="#10B981" name="Customers" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Charts Row 2: Category Performance & Low Stock Alerts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Category Performance */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Sales by Category (This Week)</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={categoryPerformanceData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="category" type="category" width={100} />
                <Tooltip />
                <Legend />
                <Bar dataKey="sales" fill="#3B82F6" name="Sales (£)" />
                <Bar dataKey="units" fill="#10B981" name="Units Sold" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Low Stock Alerts */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold text-gray-900">Low Stock Alerts</h2>
              <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium">
                {lowStockItems.length} Items
              </span>
            </div>
            <div className="space-y-3">
              {lowStockItems.map((item, index) => (
                <div
                  key={index}
                  className="flex items-center justify-between p-4 bg-red-50 border border-red-200 rounded-lg"
                >
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{item.name}</p>
                    <p className="text-sm text-gray-600">SKU: {item.sku}</p>
                    <div className="mt-2 flex items-center">
                      <div className="flex-1 bg-gray-200 rounded-full h-2 mr-2">
                        <div
                          className="bg-red-500 h-2 rounded-full"
                          style={{
                            width: `${(item.currentStock / item.threshold) * 100}%`,
                          }}
                        />
                      </div>
                      <span className="text-sm font-medium text-red-600">
                        {item.currentStock} / {item.threshold}
                      </span>
                    </div>
                  </div>
                  <button className="ml-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium">
                    Reorder
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Sales Channel Breakdown */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Sales Channel Breakdown (This Week)</h2>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={dailySalesData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="walkIn" stackId="a" fill="#3B82F6" name="Walk-in" />
              <Bar dataKey="online" stackId="a" fill="#10B981" name="Online" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

// Wrapper component with Suspense boundary
export default function BranchDashboard() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center h-screen">
        <div className="text-lg text-gray-600">Loading branch dashboard...</div>
      </div>
    }>
      <BranchDashboardContent />
    </Suspense>
  );
}

