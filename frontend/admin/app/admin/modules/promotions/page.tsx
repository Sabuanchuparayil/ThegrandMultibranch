'use client';

import { useState } from 'react';
import { PlusIcon, PencilIcon, TrashIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { useToastContext } from '@/components/notifications/ToastProvider';

export default function PromotionsModule() {
  const [showForm, setShowForm] = useState(false);
  const [editingPromotion, setEditingPromotion] = useState<any>(null);
  const toast = useToastContext();

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
          <button
            onClick={() => {
              setEditingPromotion(null);
              setShowForm(true);
            }}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
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
                    <button
                      onClick={() => {
                        setEditingPromotion(promo);
                        setShowForm(true);
                      }}
                      className="text-blue-600 hover:text-blue-900 mr-4"
                    >
                      <PencilIcon className="h-5 w-5 inline" />
                    </button>
                    <button
                      onClick={() => {
                        if (confirm('Are you sure you want to delete this promotion?')) {
                          toast.success('Promotion deleted successfully');
                        }
                      }}
                      className="text-red-600 hover:text-red-900"
                    >
                      <TrashIcon className="h-5 w-5 inline" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Promotion Form Modal */}
        {showForm && (
          <PromotionFormModal
            promotion={editingPromotion}
            onClose={() => {
              setShowForm(false);
              setEditingPromotion(null);
            }}
            onSuccess={() => {
              setShowForm(false);
              setEditingPromotion(null);
              toast.success(editingPromotion ? 'Promotion updated successfully' : 'Promotion created successfully');
            }}
          />
        )}
      </div>
    </div>
  );
}

// Promotion Form Modal
function PromotionFormModal({ promotion, onClose, onSuccess }: any) {
  const [formData, setFormData] = useState({
    name: promotion?.name || '',
    code: promotion?.code || '',
    type: promotion?.type || 'Percentage',
    value: promotion?.value || 0,
    start: promotion?.start || new Date().toISOString().split('T')[0],
    end: promotion?.end || new Date().toISOString().split('T')[0],
    status: promotion?.status || 'Active',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement GraphQL mutation
    console.log('Submit promotion:', formData);
    onSuccess();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto m-4">
        <div className="p-6 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">
            {promotion ? 'Edit Promotion' : 'Add New Promotion'}
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Name *</label>
              <input
                type="text"
                required
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Code *</label>
              <input
                type="text"
                required
                value={formData.code}
                onChange={(e) => setFormData({ ...formData, code: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Type *</label>
              <select
                required
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="Percentage">Percentage</option>
                <option value="Fixed Amount">Fixed Amount</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {formData.type === 'Percentage' ? 'Percentage (%)' : 'Fixed Amount'} *
              </label>
              <input
                type="number"
                step="0.01"
                required
                value={formData.value}
                onChange={(e) => setFormData({ ...formData, value: parseFloat(e.target.value) })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Start Date *</label>
              <input
                type="date"
                required
                value={formData.start}
                onChange={(e) => setFormData({ ...formData, start: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">End Date *</label>
              <input
                type="date"
                required
                value={formData.end}
                onChange={(e) => setFormData({ ...formData, end: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status *</label>
              <select
                required
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="Active">Active</option>
                <option value="Inactive">Inactive</option>
              </select>
            </div>
          </div>
          <div className="flex justify-end space-x-4 pt-4 border-t border-gray-200">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              {promotion ? 'Update' : 'Create'} Promotion
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

