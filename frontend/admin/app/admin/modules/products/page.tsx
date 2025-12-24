'use client';

import { useState } from 'react';
import { useQuery, gql } from '@apollo/client';
import { PlusIcon, MagnifyingGlassIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline';

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

  const { data, loading, error } = useQuery(GET_PRODUCTS, {
    variables: {
      first: 50,
      search: searchTerm || null,
    },
    fetchPolicy: 'cache-and-network',
    errorPolicy: 'all',
  });

  // Mock data fallback
  const mockProducts = [
    { id: '1', name: 'Gold Ring 22K', slug: 'gold-ring-22k', description: 'Beautiful gold ring', isPublished: true, variants: [{ id: '1', name: 'Size 6', sku: 'GR22K-6', price: { amount: 250000, currency: 'GBP' } }] },
    { id: '2', name: 'Diamond Necklace', slug: 'diamond-necklace', description: 'Elegant diamond necklace', isPublished: true, variants: [{ id: '2', name: 'Standard', sku: 'DN-STD', price: { amount: 500000, currency: 'GBP' } }] },
    { id: '3', name: 'Silver Bracelet', slug: 'silver-bracelet', description: 'Classic silver bracelet', isPublished: false, variants: [{ id: '3', name: 'Medium', sku: 'SB-M', price: { amount: 120000, currency: 'GBP' } }] },
  ];

  const products = error || !data?.products?.edges
    ? mockProducts.filter(p => !searchTerm || p.name.toLowerCase().includes(searchTerm.toLowerCase()))
    : data.products.edges.map((edge: any) => edge.node);

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Product Management</h1>
            <p className="text-gray-600 mt-1">Manage jewellery products and variants</p>
          </div>
          <button
            onClick={() => setShowForm(true)}
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
                          <button className="text-blue-600 hover:text-blue-900 mr-4">
                            <PencilIcon className="h-5 w-5 inline" />
                          </button>
                          <button className="text-red-600 hover:text-red-900">
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
      </div>
    </div>
  );
}

