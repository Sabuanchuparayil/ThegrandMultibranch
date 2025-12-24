'use client';

import { useState } from 'react';
import { MagnifyingGlassIcon, TruckIcon } from '@heroicons/react/24/outline';

export default function FulfillmentModule() {
  const [filter, setFilter] = useState('all');

  const shipments = [
    { id: '1', orderNumber: '#1234', tracking: 'TRACK123', courier: 'DHL', status: 'In Transit', date: '2024-01-15' },
    { id: '2', orderNumber: '#1235', tracking: 'TRACK124', courier: 'FedEx', status: 'Delivered', date: '2024-01-14' },
  ];

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Fulfillment & Shipping</h1>
          <p className="text-gray-600 mt-1">Manage shipments and deliveries</p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <select value={filter} onChange={(e) => setFilter(e.target.value)} className="px-4 py-2 border border-gray-300 rounded-lg">
            <option value="all">All Shipments</option>
            <option value="pending">Pending</option>
            <option value="in_transit">In Transit</option>
            <option value="delivered">Delivered</option>
          </select>
        </div>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Order #</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tracking #</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Courier</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {shipments.map((shipment) => (
                <tr key={shipment.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">{shipment.orderNumber}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{shipment.tracking}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">{shipment.courier}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800">{shipment.status}</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{shipment.date}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right">
                    <button className="text-blue-600 hover:text-blue-900"><TruckIcon className="h-5 w-5 inline" /></button>
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

