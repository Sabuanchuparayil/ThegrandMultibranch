'use client';

import { useState } from 'react';
import { useQuery, gql } from '@apollo/client';
import { PlusIcon, MagnifyingGlassIcon, AdjustmentsHorizontalIcon } from '@heroicons/react/24/outline';

const GET_BRANCH_INVENTORY = gql`
  query GetBranchInventory($branchId: ID, $search: String, $lowStockOnly: Boolean) {
    branchInventory(branchId: $branchId, lowStockOnly: $lowStockOnly) {
      id
      quantity
      availableQuantity
      reservedQuantity
      isLowStock
      lowStockThreshold
      productVariant {
        id
        name
        sku
        product {
          name
        }
      }
      branch {
        id
        name
        code
      }
    }
  }
`;

export default function InventoryModule() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedBranch, setSelectedBranch] = useState<string | null>(null);
  const [lowStockOnly, setLowStockOnly] = useState(false);

  const { data, loading, error } = useQuery(GET_BRANCH_INVENTORY, {
    variables: {
      branchId: selectedBranch,
      lowStockOnly,
    },
    fetchPolicy: 'cache-and-network',
    errorPolicy: 'all',
    skip: false, // Always try to fetch, but fallback to mock data
  });

  // Mock data fallback
  const mockInventory = [
    { id: '1', quantity: 50, availableQuantity: 45, reservedQuantity: 5, isLowStock: false, productVariant: { id: '1', name: 'Size 6', sku: 'GR22K-6', product: { name: 'Gold Ring 22K' } }, branch: { id: '1', name: 'London - Mayfair', code: 'LON-001' } },
    { id: '2', quantity: 3, availableQuantity: 2, reservedQuantity: 1, isLowStock: true, productVariant: { id: '2', name: 'Standard', sku: 'DN-STD', product: { name: 'Diamond Necklace' } }, branch: { id: '1', name: 'London - Mayfair', code: 'LON-001' } },
    { id: '3', quantity: 25, availableQuantity: 20, reservedQuantity: 5, isLowStock: false, productVariant: { id: '3', name: 'Medium', sku: 'SB-M', product: { name: 'Silver Bracelet' } }, branch: { id: '2', name: 'Dubai - Marina', code: 'DXB-001' } },
  ];

  // Get inventory from API or fallback to mock data
  const rawInventory = error || !data?.branchInventory 
    ? mockInventory
    : data.branchInventory;

  // Apply client-side filtering to both API and mock data
  const inventoryItems = rawInventory.filter((item: any) => {
    // Branch filter
    if (selectedBranch && item.branch?.id !== selectedBranch) {
      return false;
    }
    // Low stock filter
    if (lowStockOnly && !item.isLowStock) {
      return false;
    }
    // Search filter
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      const sku = item.productVariant?.sku?.toLowerCase() || '';
      const productName = item.productVariant?.product?.name?.toLowerCase() || '';
      if (!sku.includes(searchLower) && !productName.includes(searchLower)) {
        return false;
      }
    }
    return true;
  });

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Error Banner */}
        {error && (
          <div className="mb-6 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-yellow-700">
                  <strong>Backend connection error:</strong> Unable to load inventory from the API. Showing sample data for demonstration purposes.
                  {error.message && <span className="block mt-1 text-xs">Error: {error.message}</span>}
                </p>
              </div>
            </div>
          </div>
        )}
        
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Inventory Management</h1>
            <p className="text-gray-600 mt-1">Manage stock levels across all branches</p>
          </div>
          <button className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <PlusIcon className="h-5 w-5 mr-2" />
            Add Inventory
          </button>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search by SKU, product name..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <select
              value={selectedBranch || 'all'}
              onChange={(e) => setSelectedBranch(e.target.value === 'all' ? null : e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Branches</option>
              <option value="1">London - Mayfair</option>
              <option value="2">Dubai - Marina</option>
              <option value="3">Mumbai - Bandra</option>
            </select>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={lowStockOnly}
                onChange={(e) => setLowStockOnly(e.target.checked)}
                className="mr-2 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="text-sm text-gray-700">Low Stock Only</span>
            </label>
          </div>
        </div>

        {/* Data Table */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Product
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    SKU
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Branch
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Quantity
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Available
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Reserved
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {loading ? (
                  <tr>
                    <td colSpan={8} className="px-6 py-4 text-center text-gray-500">
                      Loading...
                    </td>
                  </tr>
                ) : inventoryItems.length === 0 ? (
                  <tr>
                    <td colSpan={8} className="px-6 py-4 text-center text-gray-500">
                      No inventory items found
                    </td>
                  </tr>
                ) : (
                  inventoryItems.map((item: any) => (
                    <tr key={item.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="text-sm font-medium text-gray-900">
                          {item.productVariant?.product?.name || 'N/A'}
                        </div>
                        <div className="text-sm text-gray-500">
                          {item.productVariant?.name || ''}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {item.productVariant?.sku || 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {item.branch?.name || 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {item.quantity}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {item.availableQuantity}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {item.reservedQuantity}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {item.isLowStock ? (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                            Low Stock
                          </span>
                        ) : (
                          <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                            In Stock
                          </span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button className="text-blue-600 hover:text-blue-900 mr-4">Edit</button>
                        <button className="text-gray-600 hover:text-gray-900">Adjust</button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

