/**
 * Sales Chart Component
 * Displays sales data as a line or area chart
 */
'use client';

import React from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

export interface SalesDataPoint {
  date: string;
  value: number;
  orders: number;
  currency: string;
}

interface SalesChartProps {
  data: SalesDataPoint[];
  type?: 'line' | 'area';
  height?: number;
  showOrders?: boolean;
}

export const SalesChart: React.FC<SalesChartProps> = ({
  data,
  type = 'area',
  height = 300,
  showOrders = false,
}) => {
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const formatCurrency = (value: number, currency: string = 'GBP') => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const ChartComponent = type === 'area' ? AreaChart : LineChart;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Sales Trend</h3>
      <ResponsiveContainer width="100%" height={height}>
        <ChartComponent data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="date"
            tickFormatter={formatDate}
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <YAxis
            tickFormatter={(value) => formatCurrency(value, data[0]?.currency || 'GBP')}
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <Tooltip
            formatter={(value: number | undefined, name: string) => {
              if (name === 'value') {
                return formatCurrency(value ?? 0, data[0]?.currency || 'GBP');
              }
              return value ?? 0;
            }}
            labelFormatter={formatDate}
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
            }}
          />
          <Legend />
          <Area
            type="monotone"
            dataKey="value"
            stroke="#3b82f6"
            fill="#3b82f6"
            fillOpacity={0.2}
            name="Revenue"
          />
          {showOrders && (
            <Line
              type="monotone"
              dataKey="orders"
              stroke="#10b981"
              strokeWidth={2}
              name="Orders"
              yAxisId={1}
            />
          )}
        </ChartComponent>
      </ResponsiveContainer>
    </div>
  );
};

