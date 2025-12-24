'use client';

import { useState } from 'react';
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';

export default function PricingModule() {
  const [showForm, setShowForm] = useState(false);

  // Mock data - replace with GraphQL query
  const goldRates = [
    { id: '1', region: 'UK', metal: 'Gold 22K', rate: 1850.50, date: '2024-01-15', status: 'Active' },
    { id: '2', region: 'UAE', metal: 'Gold 22K', rate: 8250.00, date: '2024-01-15', status: 'Active' },
    { id: '3', region: 'India', metal: 'Gold 22K', rate: 6250.75, date: '2024-01-15', status: 'Active' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Pricing Management</h1>
            <p className="text-gray-600 mt-1">Manage gold rates, making charges, and pricing rules</p>
          </div>
          <button onClick={() => setShowForm(true)} className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <PlusIcon className="h-5 w-5 mr-2" /> Add Gold Rate
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Gold Rates</h3>
            <div className="space-y-2">
              {goldRates.map((rate) => (
                <div key={rate.id} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <div>
                    <div className="font-medium">{rate.region} - {rate.metal}</div>
                    <div className="text-sm text-gray-500">{rate.date}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold">{rate.rate}</div>
                    <div className="text-xs text-green-600">{rate.status}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Making Charge Rules</h3>
            <p className="text-sm text-gray-500">Configure making charge calculation rules</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Pricing Overrides</h3>
            <p className="text-sm text-gray-500">Branch and region-specific pricing</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Region</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Metal Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rate</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {goldRates.map((rate) => (
                <tr key={rate.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">{rate.region}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{rate.metal}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-bold">{rate.rate}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{rate.date}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">{rate.status}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <button className="text-blue-600 hover:text-blue-900 mr-4"><PencilIcon className="h-5 w-5 inline" /></button>
                    <button className="text-red-600 hover:text-red-900"><TrashIcon className="h-5 w-5 inline" /></button>
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

