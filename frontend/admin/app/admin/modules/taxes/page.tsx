'use client';

import { useState } from 'react';
import { PlusIcon, PencilIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { useToastContext } from '@/components/notifications/ToastProvider';

export default function TaxesModule() {
  const [showForm, setShowForm] = useState(false);
  const [editingTaxRule, setEditingTaxRule] = useState<any>(null);
  const toast = useToastContext();

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
          <button
            onClick={() => {
              setEditingTaxRule(null);
              setShowForm(true);
            }}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
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
                    <button
                      onClick={() => {
                        setEditingTaxRule(rule);
                        setShowForm(true);
                      }}
                      className="text-blue-600 hover:text-blue-900"
                    >
                      <PencilIcon className="h-5 w-5 inline" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Tax Rule Form Modal */}
        {showForm && (
          <TaxRuleFormModal
            rule={editingTaxRule}
            onClose={() => {
              setShowForm(false);
              setEditingTaxRule(null);
            }}
            onSuccess={() => {
              setShowForm(false);
              setEditingTaxRule(null);
              toast.success(editingTaxRule ? 'Tax rule updated successfully' : 'Tax rule created successfully');
            }}
          />
        )}
      </div>
    </div>
  );
}

// Tax Rule Form Modal
function TaxRuleFormModal({ rule, onClose, onSuccess }: any) {
  const [formData, setFormData] = useState({
    region: rule?.region || '',
    type: rule?.type || 'VAT',
    rate: rule?.rate || 0,
    description: rule?.description || '',
    status: rule?.status || 'Active',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement GraphQL mutation
    console.log('Submit tax rule:', formData);
    onSuccess();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto m-4">
        <div className="p-6 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">
            {rule ? 'Edit Tax Rule' : 'Add New Tax Rule'}
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Region *</label>
              <select
                required
                value={formData.region}
                onChange={(e) => setFormData({ ...formData, region: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Select Region</option>
                <option value="UK">United Kingdom</option>
                <option value="UAE">United Arab Emirates</option>
                <option value="India">India</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tax Type *</label>
              <select
                required
                value={formData.type}
                onChange={(e) => setFormData({ ...formData, type: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="VAT">VAT</option>
                <option value="GST">GST</option>
                <option value="Sales Tax">Sales Tax</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Rate (%) *</label>
              <input
                type="number"
                step="0.01"
                required
                value={formData.rate}
                onChange={(e) => setFormData({ ...formData, rate: parseFloat(e.target.value) })}
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
            <div className="col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                rows={3}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
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
              {rule ? 'Update' : 'Create'} Tax Rule
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

