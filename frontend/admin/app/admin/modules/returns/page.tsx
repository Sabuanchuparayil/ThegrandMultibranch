'use client';

import { useState } from 'react';
import { MagnifyingGlassIcon, ArrowPathIcon } from '@heroicons/react/24/outline';

export default function ReturnsModule() {
  const returns = [
    { id: '1', orderNumber: '#1234', rma: 'RMA-001', reason: 'Defective', status: 'Pending', date: '2024-01-15' },
    { id: '2', orderNumber: '#1235', rma: 'RMA-002', reason: 'Wrong Size', status: 'Approved', date: '2024-01-14' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Returns & Refunds</h1>
          <p className="text-gray-600 mt-1">Manage return requests and refunds</p>
        </div>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">RMA #</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Order #</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reason</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {returns.map((item) => (
                <tr key={item.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">{item.rma}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{item.orderNumber}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{item.reason}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-800">{item.status}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{item.date}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <button
                      onClick={() => {
                        // TODO: Open return detail/process modal
                        console.log('Process return:', item.id);
                      }}
                      className="text-blue-600 hover:text-blue-900"
                    >
                      <ArrowPathIcon className="h-5 w-5 inline" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

