'use client';

import { useState, useEffect } from 'react';
import { useQuery, gql } from '@apollo/client';
import { PlusIcon, MagnifyingGlassIcon, PencilIcon, TrashIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { useErrorCache } from '@/hooks/useErrorCache';

const GET_PRODUCTS = gql`
  query GetProducts($first: Int, $after: String, $search: String) {
    products(first: $first, after: $after, filter: { search: $search }) {
      edges {
        node {
          id
          name
          slug
          description
          isPublished
          variants {
            id
            name
            sku
            price {
              amount
              currency
            }
          }
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
    }
  }
`;

export default function ProductsModule() {
  const [searchTerm, setSearchTerm] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState<any>(null);

  const { data, loading, error, refetch } = useQuery(GET_PRODUCTS, {
    variables: {
      first: 50,
      search: searchTerm || null,
    },
    fetchPolicy: 'cache-first',
    errorPolicy: 'all',
    notifyOnNetworkStatusChange: false,
  });

  // Error caching mechanism
  const { shouldShowError, handleError, clearError } = useErrorCache({
    queryName: 'GetProducts',
    variables: { first: 50, search: searchTerm || null },
    enabled: true,
  });

  // Update error cache when error changes
  // Note: handleError is memoized with useCallback, so it's stable and safe to include
  // However, we only depend on error to avoid unnecessary re-runs
  useEffect(() => {
    if (error) {
      handleError(error as Error);
    } else {
      handleError(null);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [error]); // Only depend on error, handleError is stable

  // Mock data fallback
  const mockProducts = [
    { id: '1', name: 'Gold Ring 22K', slug: 'gold-ring-22k', description: 'Beautiful gold ring', isPublished: true, variants: [{ id: '1', name: 'Size 6', sku: 'GR22K-6', price: { amount: 250000, currency: 'GBP' } }] },
    { id: '2', name: 'Diamond Necklace', slug: 'diamond-necklace', description: 'Elegant diamond necklace', isPublished: true, variants: [{ id: '2', name: 'Standard', sku: 'DN-STD', price: { amount: 500000, currency: 'GBP' } }] },
    { id: '3', name: 'Silver Bracelet', slug: 'silver-bracelet', description: 'Classic silver bracelet', isPublished: false, variants: [{ id: '3', name: 'Medium', sku: 'SB-M', price: { amount: 120000, currency: 'GBP' } }] },
  ];

  // Get products from API or fallback to mock data
  // Only use mock data if there's an error AND we should show it (not cached/suppressed)
  const rawProducts = (error && shouldShowError) || !data?.products?.edges
    ? mockProducts
    : data.products.edges.map((edge: any) => edge.node);

  // Apply client-side filtering to both API and mock data
  const products = rawProducts.filter((product: any) => {
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      const name = product.name?.toLowerCase() || '';
      const description = product.description?.toLowerCase() || '';
      if (!name.includes(searchLower) && !description.includes(searchLower)) {
        return false;
      }
    }
    return true;
  });

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Error Banner - Only show if error is not cached/suppressed */}
        {error && shouldShowError && (
          <div className="mb-6 bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3 flex-1">
                <p className="text-sm text-yellow-700">
                  <strong>Backend connection error:</strong> Unable to load products from the API. Showing sample data for demonstration purposes.
                  {error.message && <span className="block mt-1 text-xs">Error: {error.message}</span>}
                </p>
                <button
                  onClick={clearError}
                  className="mt-2 text-xs text-yellow-800 underline hover:text-yellow-900"
                >
                  Dismiss (errors will be cached for 5 minutes)
                </button>
              </div>
            </div>
          </div>
        )}
        
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Product Management</h1>
            <p className="text-gray-600 mt-1">Manage jewellery products and variants</p>
          </div>
          <button
            onClick={() => {
              setEditingProduct(null);
              setShowForm(true);
            }}
            className="flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Add Product
          </button>
        </div>

        {/* Search */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search products..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
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
                    Variants
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Price Range
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
                    <td colSpan={5} className="px-6 py-4 text-center text-gray-500">
                      Loading...
                    </td>
                  </tr>
                ) : products.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="px-6 py-4 text-center text-gray-500">
                      No products found
                    </td>
                  </tr>
                ) : (
                  products.map((product: any) => {
                    const variants = product.variants || [];
                    const prices = variants
                      .map((v: any) => parseFloat(v.price?.amount || 0))
                      .filter((p: number) => p > 0);
                    const minPrice = prices.length > 0 ? Math.min(...prices) : 0;
                    const maxPrice = prices.length > 0 ? Math.max(...prices) : 0;

                    return (
                      <tr key={product.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4">
                          <div className="text-sm font-medium text-gray-900">{product.name}</div>
                          <div className="text-sm text-gray-500 line-clamp-2">
                            {product.description || 'No description'}
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {variants.length} variant{variants.length !== 1 ? 's' : ''}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {minPrice > 0 ? (
                            <>
                              {new Intl.NumberFormat('en-GB', {
                                style: 'currency',
                                currency: variants[0]?.price?.currency || 'GBP',
                              }).format(minPrice / 100)}
                              {minPrice !== maxPrice && ` - ${new Intl.NumberFormat('en-GB', {
                                style: 'currency',
                                currency: variants[0]?.price?.currency || 'GBP',
                              }).format(maxPrice / 100)}`}
                            </>
                          ) : (
                            'N/A'
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          {product.isPublished ? (
                            <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                              Published
                            </span>
                          ) : (
                            <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                              Draft
                            </span>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                          <button
                            onClick={() => {
                              setEditingProduct(product);
                              setShowForm(true);
                            }}
                            className="text-blue-600 hover:text-blue-900 mr-4"
                          >
                            <PencilIcon className="h-5 w-5 inline" />
                          </button>
                          <button
                            onClick={() => {
                              if (confirm('Are you sure you want to delete this product?')) {
                                // TODO: Implement delete mutation
                                console.log('Delete product:', product.id);
                              }
                            }}
                            className="text-red-600 hover:text-red-900"
                          >
                            <TrashIcon className="h-5 w-5 inline" />
                          </button>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Product Form Modal */}
        {showForm && (
          <ProductFormModal
            product={editingProduct}
            onClose={() => {
              setShowForm(false);
              setEditingProduct(null);
            }}
            onSuccess={() => {
              setShowForm(false);
              setEditingProduct(null);
              refetch();
            }}
          />
        )}
      </div>
    </div>
  );
}

// Product Form Modal
function ProductFormModal({ product, onClose, onSuccess }: any) {
  const [formData, setFormData] = useState({
    name: product?.name || '',
    description: product?.description || '',
    slug: product?.slug || '',
    isPublished: product?.isPublished ?? false,
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement GraphQL mutation
    console.log('Submit product:', formData);
    onSuccess();
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto m-4">
        <div className="p-6 border-b border-gray-200 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-900">
            {product ? 'Edit Product' : 'Add New Product'}
          </h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Product Name *</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Slug</label>
            <input
              type="text"
              value={formData.slug}
              onChange={(e) => setFormData({ ...formData, slug: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="flex items-center">
              <input
                type="checkbox"
                checked={formData.isPublished}
                onChange={(e) => setFormData({ ...formData, isPublished: e.target.checked })}
                className="mr-2 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <span className="text-sm text-gray-700">Published</span>
            </label>
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
              {product ? 'Update' : 'Create'} Product
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

