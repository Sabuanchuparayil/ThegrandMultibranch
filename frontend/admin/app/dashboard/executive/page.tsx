'use client';

import { useState, useEffect } from 'react';
import { useQuery, gql } from '@apollo/client';
import {
  ChartBarIcon,
  CurrencyDollarIcon,
  ShoppingBagIcon,
  UserGroupIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
} from '@heroicons/react/24/outline';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

// GraphQL Queries
const GET_EXECUTIVE_KPIS = gql`
  query GetExecutiveKPIs($regionCode: String, $dateFrom: DateTime, $dateTo: DateTime) {
    # Sales KPIs
    salesSummary: orders(filter: { status: FULFILLED, created: { gte: $dateFrom, lte: $dateTo } }) {
      totalCount
      edges {
        node {
          total {
            gross {
              amount
              currency
            }
          }
        }
      }
    }
    
    # Additional KPIs would come from your custom extensions
    # These are examples - you'll need to implement the actual queries
  }
`;

const GET_SALES_TREND = gql`
  query GetSalesTrend($days: Int!, $regionCode: String) {
    # Sales trend data for chart
    # Implement based on your GraphQL schema
  }
`;

const GET_REGION_PERFORMANCE = gql`
  query GetRegionPerformance($dateFrom: DateTime, $dateTo: DateTime) {
    # Performance by region
    # Implement based on your GraphQL schema
  }
`;

// KPI Card Component
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

// Dashboard Page Component
export default function ExecutiveDashboard() {
  const [dateRange, setDateRange] = useState({
    from: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // 30 days ago
    to: new Date(),
  });
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null);

  // Mock data - Replace with actual GraphQL queries
  const kpis = {
    totalRevenue: {
      value: '£2,450,000',
      change: 12.5,
      trend: 'up' as const,
    },
    totalOrders: {
      value: '1,245',
      change: 8.3,
      trend: 'up' as const,
    },
    averageOrderValue: {
      value: '£1,967',
      change: -2.1,
      trend: 'down' as const,
    },
    activeCustomers: {
      value: '3,421',
      change: 15.7,
      trend: 'up' as const,
    },
    inventoryValue: {
      value: '£8,500,000',
      change: 5.2,
      trend: 'up' as const,
    },
    lowStockItems: {
      value: '42',
      change: -18.5,
      trend: 'up' as const,
    },
  };

  // Mock chart data - Replace with actual GraphQL queries
  const salesTrendData = [
    { date: 'Jan', sales: 40000, orders: 120 },
    { date: 'Feb', sales: 45000, orders: 135 },
    { date: 'Mar', sales: 52000, orders: 150 },
    { date: 'Apr', sales: 48000, orders: 145 },
    { date: 'May', sales: 61000, orders: 180 },
    { date: 'Jun', sales: 68000, orders: 200 },
    { date: 'Jul', sales: 72000, orders: 210 },
  ];

  const regionPerformanceData = [
    { region: 'UK', sales: 850000, orders: 520, customers: 1200 },
    { region: 'UAE', sales: 950000, orders: 480, customers: 980 },
    { region: 'India', sales: 650000, orders: 245, customers: 1241 },
  ];

  const categorySalesData = [
    { name: 'Rings', value: 35, amount: 857500 },
    { name: 'Necklaces', value: 25, amount: 612500 },
    { name: 'Earrings', value: 20, amount: 490000 },
    { name: 'Bracelets', value: 12, amount: 294000 },
    { name: 'Others', value: 8, amount: 196000 },
  ];

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

  // Refresh data every 30 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      // Refetch data
      // This would trigger Apollo refetch in real implementation
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Executive Dashboard</h1>
          <p className="text-gray-600">Real-time overview of business performance across all regions</p>
          
          {/* Filters */}
          <div className="mt-4 flex gap-4 items-center">
            <select
              value={selectedRegion || 'all'}
              onChange={(e) => setSelectedRegion(e.target.value === 'all' ? null : e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Regions</option>
              <option value="UK">United Kingdom</option>
              <option value="UAE">United Arab Emirates</option>
              <option value="INDIA">India</option>
            </select>
            
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

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <KPICard
            title="Total Revenue"
            value={kpis.totalRevenue.value}
            change={kpis.totalRevenue.change}
            changeLabel="vs last period"
            trend={kpis.totalRevenue.trend}
            icon={CurrencyDollarIcon}
            color="green"
          />
          <KPICard
            title="Total Orders"
            value={kpis.totalOrders.value}
            change={kpis.totalOrders.change}
            changeLabel="vs last period"
            trend={kpis.totalOrders.trend}
            icon={ShoppingBagIcon}
            color="blue"
          />
          <KPICard
            title="Average Order Value"
            value={kpis.averageOrderValue.value}
            change={kpis.averageOrderValue.change}
            changeLabel="vs last period"
            trend={kpis.averageOrderValue.trend}
            icon={ChartBarIcon}
            color="purple"
          />
          <KPICard
            title="Active Customers"
            value={kpis.activeCustomers.value}
            change={kpis.activeCustomers.change}
            changeLabel="vs last period"
            trend={kpis.activeCustomers.trend}
            icon={UserGroupIcon}
            color="orange"
          />
          <KPICard
            title="Inventory Value"
            value={kpis.inventoryValue.value}
            change={kpis.inventoryValue.change}
            changeLabel="vs last period"
            trend={kpis.inventoryValue.trend}
            icon={ChartBarIcon}
            color="blue"
          />
          <KPICard
            title="Low Stock Items"
            value={kpis.lowStockItems.value}
            change={kpis.lowStockItems.change}
            changeLabel="vs last period"
            trend={kpis.lowStockItems.trend}
            icon={ChartBarIcon}
            color="red"
          />
        </div>

        {/* Charts Row 1: Sales Trend & Region Performance */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Sales Trend Chart */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Sales Trend (Last 7 Months)</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={salesTrendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="sales"
                  stroke="#3B82F6"
                  strokeWidth={2}
                  name="Sales (£)"
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="orders"
                  stroke="#10B981"
                  strokeWidth={2}
                  name="Orders"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Region Performance Chart */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Performance by Region</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={regionPerformanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="region" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Bar yAxisId="left" dataKey="sales" fill="#3B82F6" name="Sales (£)" />
                <Bar yAxisId="right" dataKey="orders" fill="#10B981" name="Orders" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Charts Row 2: Category Sales */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Category Sales Pie Chart */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Sales by Category</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categorySalesData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${((percent || 0) * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {categorySalesData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 space-y-2">
              {categorySalesData.map((item, index) => (
                <div key={item.name} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div
                      className="w-4 h-4 rounded mr-2"
                      style={{ backgroundColor: COLORS[index % COLORS.length] }}
                    />
                    <span className="text-sm text-gray-600">{item.name}</span>
                  </div>
                  <span className="text-sm font-medium text-gray-900">
                    £{item.amount.toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Recent Activity / Top Products */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Top Performing Products</h2>
            <div className="space-y-4">
              {[
                { name: '18K Gold Ring Set', sales: 125000, orders: 85, growth: 12 },
                { name: 'Diamond Necklace', sales: 98000, orders: 62, growth: 8 },
                { name: 'Platinum Earrings', sales: 87000, orders: 58, growth: 15 },
                { name: '22K Gold Bracelet', sales: 75000, orders: 45, growth: -3 },
                { name: 'Pearl Set', sales: 68000, orders: 52, growth: 22 },
              ].map((product, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{product.name}</p>
                    <p className="text-sm text-gray-600">
                      {product.orders} orders • £{product.sales.toLocaleString()}
                    </p>
                  </div>
                  <div className="text-right">
                    <span
                      className={`text-sm font-medium ${
                        product.growth > 0 ? 'text-green-600' : 'text-red-600'
                      }`}
                    >
                      {product.growth > 0 ? '+' : ''}{product.growth}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
