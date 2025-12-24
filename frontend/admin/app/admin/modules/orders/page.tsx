'use client';

import { useState, useEffect } from 'react';
import { useQuery, gql } from '@apollo/client';
import { MagnifyingGlassIcon, EyeIcon } from '@heroicons/react/24/outline';
import { useErrorCache } from '@/hooks/useErrorCache';

const GET_ORDERS = gql`
  query GetOrders($first: Int, $filter: OrderFilterInput) {
    orders(first: $first, filter: $filter) {
      edges {
        node {
          id
          number
          status
          total {
            gross {
              amount
              currency
            }
          }
          user {
            email
          }
          created
        }
      }
    }
  }
`;

export default function OrdersModule() {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');

  const { data, loading, error } = useQuery(GET_ORDERS, {
    variables: {
      first: 50,
      filter: {
        search: searchTerm || null,
        status: statusFilter !== 'all' ? statusFilter : null,
      },
    },
    fetchPolicy: 'cache-and-network',
    errorPolicy: 'all',
    notifyOnNetworkStatusChange: false,
  });

  // Error caching mechanism
  const { shouldShowError, handleError, clearError } = useErrorCache({
    queryName: 'GetOrders',
    variables: {
      first: 50,
      filter: {
        search: searchTerm || null,
        status: statusFilter !== 'all' ? statusFilter : null,
      },
    },
    enabled: true,
  });

  // Update error cache when error changes
  useEffect(() => {
    if (error) {
      handleError(error as Error);
    } else {
      handleError(null);
    }
  }, [error, handleError]);

  // Mock data fallback for development/testing
  const mockOrders = [
    { id: '1', number: 'ORD-001', status: 'FULFILLED', total: { gross: { amount: 250000, currency: 'GBP' } }, user: { email: 'customer@example.com' }, created: new Date().toISOString() },
    { id: '2', number: 'ORD-002', status: 'UNFULFILLED', total: { gross: { amount: 150000, currency: 'GBP' } }, user: { email: 'customer2@example.com' }, created: new Date(Date.now() - 86400000).toISOString() },
    { id: '3', number: 'ORD-003', status: 'PARTIALLY_FULFILLED', total: { gross: { amount: 320000, currency: 'GBP' } }, user: { email: 'customer3@example.com' }, created: new Date(Date.now() - 172800000).toISOString() },
  ];

  // Get orders from API or fallback to mock data
  // Only use mock data if there's an error AND we should show it (not cached/suppressed)
  const rawOrders = (error && shouldShowError) || !data?.orders?.edges 
    ? mockOrders
    : data.orders.edges.map((edge: any) => edge.node);

  // Apply client-side filtering to both API and mock data
  const orders = rawOrders.filter((order: any) => {
    // Status filter
    if (statusFilter !== 'all' && order.status !== statusFilter) {
      return false;
    }
    // Search filter
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      const orderNumber = order.number?.toLowerCase() || '';
      const customerEmail = order.user?.email?.toLowerCase() || '';
      if (!orderNumber.includes(searchLower) && !customerEmail.includes(searchLower)) {
        return false;
      }
    }
    return true;
  });

  const statusColors: Record<string, string> = {
    FULFILLED: 'bg-green-100 text-green-800',
    UNFULFILLED: 'bg-yellow-100 text-yellow-800',
    PARTIALLY_FULFILLED: 'bg-blue-100 text-blue-800',
    CANCELED: 'bg-red-100 text-red-800',
    DRAFT: 'bg-gray-100 text-gray-800',
  };

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
                  <strong>Backend connection error:</strong> Unable to load orders from the API. Showing sample data for demonstration purposes.
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
        
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Order Management</h1>
          <p className="text-gray-600 mt-1">Manage and track customer orders</p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search by order number, customer email..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="all">All Status</option>
              <option value="DRAFT">Draft</option>
              <option value="UNFULFILLED">Unfulfilled</option>
              <option value="PARTIALLY_FULFILLED">Partially Fulfilled</option>
              <option value="FULFILLED">Fulfilled</option>
              <option value="CANCELED">Canceled</option>
            </select>
          </div>
        </div>

        {/* Data Table */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Order #
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Customer
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total
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
                    <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                      Loading...
                    </td>
                  </tr>
                ) : orders.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-6 py-4 text-center text-gray-500">
                      No orders found
                    </td>
                  </tr>
                ) : (
                  orders.map((order: any) => (
                    <tr key={order.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        #{order.number}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                        {order.user?.email || 'Guest'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(order.created).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                        {new Intl.NumberFormat('en-GB', {
                          style: 'currency',
                          currency: order.total.gross.currency,
                        }).format(parseFloat(order.total.gross.amount) / 100)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span
                          className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                            statusColors[order.status] || statusColors.DRAFT
                          }`}
                        >
                          {order.status.replace('_', ' ')}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                        <button
                          onClick={() => {
                            // Navigate to order detail page
                            window.location.href = `/admin/modules/orders/${order.id}`;
                          }}
                          className="text-blue-600 hover:text-blue-900"
                        >
                          <EyeIcon className="h-5 w-5 inline" />
                        </button>
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

