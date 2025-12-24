'use client';

import { useState } from 'react';
import { PlusIcon, PencilIcon, TrashIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { useToastContext } from '@/components/notifications/ToastProvider';

export default function PricingModule() {
  const [showGoldRateForm, setShowGoldRateForm] = useState(false);
  const [showMakingChargeForm, setShowMakingChargeForm] = useState(false);
  const [showPricingOverrideForm, setShowPricingOverrideForm] = useState(false);
  const [editingGoldRate, setEditingGoldRate] = useState<any>(null);
  const toast = useToastContext();

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
          <button onClick={() => {
            setEditingGoldRate(null);
            setShowGoldRateForm(true);
          }} className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
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
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Making Charge Rules</h3>
              <button
                onClick={() => setShowMakingChargeForm(true)}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium"
              >
                Configure
              </button>
            </div>
            <p className="text-sm text-gray-500">Configure making charge calculation rules</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Pricing Overrides</h3>
              <button
                onClick={() => setShowPricingOverrideForm(true)}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium"
              >
                Configure
              </button>
            </div>
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
                    <button
                      onClick={() => {
                        setEditingGoldRate(rate);
                        setShowGoldRateForm(true);
                      }}
                      className="text-blue-600 hover:text-blue-900 mr-4"
                    >
                      <PencilIcon className="h-5 w-5 inline" />
                    </button>
                    <button
                      onClick={() => {
                        if (confirm('Are you sure you want to delete this gold rate?')) {
                          toast.success('Gold rate deleted successfully');
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

        {/* Gold Rate Form Modal */}
        {showGoldRateForm && (
          <GoldRateFormModal
            rate={editingGoldRate}
            onClose={() => {
              setShowGoldRateForm(false);
              setEditingGoldRate(null);
            }}
            onSuccess={() => {
              setShowGoldRateForm(false);
              setEditingGoldRate(null);
              toast.success(editingGoldRate ? 'Gold rate updated successfully' : 'Gold rate created successfully');
            }}
          />
        )}

        {/* Making Charge Rules Form Modal */}
        {showMakingChargeForm && (
          <MakingChargeFormModal
            onClose={() => setShowMakingChargeForm(false)}
            onSuccess={() => {
              setShowMakingChargeForm(false);
              toast.success('Making charge rules updated successfully');
            }}
          />
        )}

        {/* Pricing Overrides Form Modal */}
        {showPricingOverrideForm && (
          <PricingOverrideFormModal
            onClose={() => setShowPricingOverrideForm(false)}
            onSuccess={() => {
              setShowPricingOverrideForm(false);
              toast.success('Pricing override configured successfully');
            }}
          />
        )}
      </div>
    </div>
  );
}

// Gold Rate Form Modal
function GoldRateFormModal({ rate, onClose, onSuccess }: any) {
  const [formData, setFormData] = useState({
    region: rate?.region || '',
    metal: rate?.metal || 'Gold 22K',
    rate: rate?.rate || 0,
    date: rate?.date || new Date().toISOString().split('T')[0],
    status: rate?.status || 'Active',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement GraphQL mutation
    console.log('Submit gold rate:', formData);
    onSuccess();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto m-4">
        <div className="p-6 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">
            {rate ? 'Edit Gold Rate' : 'Add New Gold Rate'}
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
              <label className="block text-sm font-medium text-gray-700 mb-1">Metal Type *</label>
              <select
                required
                value={formData.metal}
                onChange={(e) => setFormData({ ...formData, metal: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="Gold 22K">Gold 22K</option>
                <option value="Gold 18K">Gold 18K</option>
                <option value="Gold 14K">Gold 14K</option>
                <option value="Silver">Silver</option>
                <option value="Platinum">Platinum</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Rate (per gram) *</label>
              <input
                type="number"
                step="0.01"
                required
                value={formData.rate}
                onChange={(e) => setFormData({ ...formData, rate: parseFloat(e.target.value) || 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Date *</label>
              <input
                type="date"
                required
                value={formData.date}
                onChange={(e) => setFormData({ ...formData, date: e.target.value })}
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
              {rate ? 'Update' : 'Create'} Gold Rate
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Making Charge Rules Form Modal
function MakingChargeFormModal({ onClose, onSuccess }: any) {
  const [formData, setFormData] = useState({
    calculationType: 'percentage', // percentage or fixed
    percentage: 10,
    fixedAmount: 0,
    minCharge: 0,
    maxCharge: 0,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement GraphQL mutation
    console.log('Submit making charge rules:', formData);
    onSuccess();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto m-4">
        <div className="p-6 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">Configure Making Charge Rules</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Calculation Type *</label>
            <select
              required
              value={formData.calculationType}
              onChange={(e) => setFormData({ ...formData, calculationType: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="percentage">Percentage of Gold Value</option>
              <option value="fixed">Fixed Amount</option>
            </select>
          </div>
          {formData.calculationType === 'percentage' ? (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Percentage (%) *</label>
              <input
                type="number"
                step="0.01"
                required
                value={formData.percentage}
                onChange={(e) => setFormData({ ...formData, percentage: parseFloat(e.target.value) || 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          ) : (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Fixed Amount *</label>
              <input
                type="number"
                step="0.01"
                required
                value={formData.fixedAmount}
                onChange={(e) => setFormData({ ...formData, fixedAmount: parseFloat(e.target.value) || 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          )}
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Minimum Charge</label>
              <input
                type="number"
                step="0.01"
                value={formData.minCharge}
                onChange={(e) => setFormData({ ...formData, minCharge: parseFloat(e.target.value) || 0 })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Maximum Charge</label>
              <input
                type="number"
                step="0.01"
                value={formData.maxCharge}
                onChange={(e) => setFormData({ ...formData, maxCharge: parseFloat(e.target.value) || 0 })}
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
              Save Rules
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

// Pricing Override Form Modal
function PricingOverrideFormModal({ onClose, onSuccess }: any) {
  const [formData, setFormData] = useState({
    branchId: '',
    regionId: '',
    productId: '',
    overrideType: 'percentage' as 'percentage' | 'fixed',
    value: 0,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement GraphQL mutation
    console.log('Submit pricing override:', formData);
    onSuccess();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto m-4">
        <div className="p-6 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">Configure Pricing Override</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Branch</label>
            <select
              value={formData.branchId}
              onChange={(e) => setFormData({ ...formData, branchId: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Branches</option>
              <option value="1">London - Mayfair</option>
              <option value="2">Dubai - Marina</option>
              <option value="3">Mumbai - Bandra</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Region</label>
            <select
              value={formData.regionId}
              onChange={(e) => setFormData({ ...formData, regionId: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Regions</option>
              <option value="1">United Kingdom</option>
              <option value="2">United Arab Emirates</option>
              <option value="3">India</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Product</label>
            <select
              value={formData.productId}
              onChange={(e) => setFormData({ ...formData, productId: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="">All Products</option>
              <option value="1">Gold Ring 22K</option>
              <option value="2">Diamond Necklace</option>
              <option value="3">Silver Bracelet</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Override Type *</label>
            <select
              required
              value={formData.overrideType}
              onChange={(e) => setFormData({ ...formData, overrideType: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="percentage">Percentage Adjustment</option>
              <option value="fixed">Fixed Amount</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              {formData.overrideType === 'percentage' ? 'Percentage (%)' : 'Fixed Amount'} *
            </label>
            <input
              type="number"
              step="0.01"
              required
              value={formData.value}
              onChange={(e) => setFormData({ ...formData, value: parseFloat(e.target.value) || 0 })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
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
              Save Override
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

