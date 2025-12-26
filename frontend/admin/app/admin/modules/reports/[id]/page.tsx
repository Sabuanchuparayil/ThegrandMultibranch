'use client';

import { useParams, useRouter } from 'next/navigation';
import { ChartBarIcon, DocumentArrowDownIcon, ArrowLeftIcon } from '@heroicons/react/24/outline';
import { useState } from 'react';

const reportConfigs: Record<string, { name: string; description: string; color: string }> = {
  sales: {
    name: 'Sales Report',
    description: 'Revenue, orders, and sales trends analysis',
    color: 'blue',
  },
  inventory: {
    name: 'Inventory Report',
    description: 'Stock levels, movements, and inventory analytics',
    color: 'green',
  },
  customer: {
    name: 'Customer Report',
    description: 'Customer analytics, behavior, and segmentation',
    color: 'purple',
  },
  financial: {
    name: 'Financial Report',
    description: 'Revenue, expenses, profits, and financial metrics',
    color: 'yellow',
  },
};

export default function ReportDetailPage() {
  const params = useParams();
  const router = useRouter();
  const reportId = params.id as string;
  const report = reportConfigs[reportId];

  const [dateRange, setDateRange] = useState({
    from: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
    to: new Date().toISOString().split('T')[0],
  });

  if (!report) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-8 text-center">
            <h1 className="text-2xl font-bold text-gray-900 mb-4">Report Not Found</h1>
            <p className="text-gray-600 mb-6">The requested report does not exist.</p>
            <button
              onClick={() => router.push('/admin/modules/reports')}
              className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
            >
              Back to Reports
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => router.back()}
            className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeftIcon className="h-5 w-5 mr-2" />
            Back to Reports
          </button>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{report.name}</h1>
              <p className="text-gray-600 mt-1">{report.description}</p>
            </div>
            <button className="flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
              <DocumentArrowDownIcon className="h-5 w-5 mr-2" />
              Export Report
            </button>
          </div>
        </div>

        {/* Date Range Filter */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="flex items-center space-x-4">
            <label className="text-sm font-medium text-gray-700">Date Range:</label>
            <input
              type="date"
              value={dateRange.from}
              onChange={(e) => setDateRange({ ...dateRange, from: e.target.value })}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
            <span className="text-gray-600">to</span>
            <input
              type="date"
              value={dateRange.to}
              onChange={(e) => setDateRange({ ...dateRange, to: e.target.value })}
              className="border border-gray-300 rounded-md px-3 py-2 text-sm"
            />
            <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm hover:bg-blue-700">
              Generate Report
            </button>
          </div>
        </div>

        {/* Report Content */}
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="text-center py-12">
            <ChartBarIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Report Generation</h2>
            <p className="text-gray-600 mb-6">
              This report will be generated based on the selected date range and filters.
            </p>
            <p className="text-sm text-gray-500">
              Report data will be displayed here once the backend GraphQL queries are implemented.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}


