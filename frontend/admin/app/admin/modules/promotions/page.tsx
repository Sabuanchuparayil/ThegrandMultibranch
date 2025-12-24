'use client';

import { useState } from 'react';
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';

export default function PromotionsModule() {
  const promotions = [
    { id: '1', name: 'New Year Sale', code: 'NY2024', type: 'Percentage', value: 20, status: 'Active', start: '2024-01-01', end: '2024-01-31' },
    { id: '2', name: 'Valentine\'s Special', code: 'LOVE2024', type: 'Fixed Amount', value: 100, status: 'Active', start: '2024-02-01', end: '2024-02-14' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Promotions & Coupons</h1>
            <p className="text-gray-600 mt-1">Manage discounts, coupons, and campaigns</p>
          </div>
          <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <PlusIcon className="h-5 w-5 mr-2" /> Add Promotion
          </button>
        </div>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Code</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Value</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Period</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {promotions.map((promo) => (
                <tr key={promo.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">{promo.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-mono">{promo.code}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{promo.type}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-bold">
                    {promo.type === 'Percentage' ? `${promo.value}%` : `£${promo.value}`}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {promo.start} to {promo.end}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">{promo.status}</span>
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

