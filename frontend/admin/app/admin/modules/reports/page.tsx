'use client';

import { ChartBarIcon, DocumentArrowDownIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';

const reportTypes = [
  { id: 'sales', name: 'Sales Report', description: 'Revenue, orders, and sales trends', icon: ChartBarIcon, color: 'blue' },
  { id: 'inventory', name: 'Inventory Report', description: 'Stock levels and movements', icon: ChartBarIcon, color: 'green' },
  { id: 'customer', name: 'Customer Report', description: 'Customer analytics and behavior', icon: ChartBarIcon, color: 'purple' },
  { id: 'financial', name: 'Financial Report', description: 'Revenue, expenses, and profits', icon: ChartBarIcon, color: 'yellow' },
];

export default function ReportsModule() {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Reports & Analytics</h1>
          <p className="text-gray-600 mt-1">Generate and view business reports</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {reportTypes.map((report) => {
            const Icon = report.icon;
            return (
              <Link
                key={report.id}
                href={`/admin/modules/reports/${report.id}`}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
              >
                <div className={`w-12 h-12 bg-${report.color}-500 rounded-lg flex items-center justify-center mb-4`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{report.name}</h3>
                <p className="text-sm text-gray-500">{report.description}</p>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}

