'use client';

import { useState } from 'react';
import { PlusIcon, PencilIcon } from '@heroicons/react/24/outline';

export default function TaxesModule() {
  const taxRules = [
    { id: '1', region: 'UK', type: 'VAT', rate: 20, description: 'Standard VAT rate', status: 'Active' },
    { id: '2', region: 'UAE', type: 'VAT', rate: 5, description: 'Standard VAT rate', status: 'Active' },
    { id: '3', region: 'India', type: 'GST', rate: 3, description: 'GST on jewellery', status: 'Active' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Tax Configuration</h1>
            <p className="text-gray-600 mt-1">Manage tax rules by region and product type</p>
          </div>
          <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <PlusIcon className="h-5 w-5 mr-2" /> Add Tax Rule
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Region</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tax Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rate (%)</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Description</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {taxRules.map((rule) => (
                <tr key={rule.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">{rule.region}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{rule.type}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-bold">{rule.rate}%</td>
                  <td className="px-6 py-4 text-sm text-gray-500">{rule.description}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">{rule.status}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <button className="text-blue-600 hover:text-blue-900"><PencilIcon className="h-5 w-5 inline" /></button>
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

