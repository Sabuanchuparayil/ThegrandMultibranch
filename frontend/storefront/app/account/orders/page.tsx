'use client';

import { useQuery, gql } from '@apollo/client';
import Link from 'next/link';
import { EyeIcon } from '@heroicons/react/24/outline';

const GET_USER_ORDERS = gql`
  query GetUserOrders($first: Int) {
    me {
      orders(first: $first) {
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
            created
            lines {
              id
              productName
              quantity
            }
          }
        }
      }
    }
  }
`;

const statusColors: Record<string, string> = {
  FULFILLED: 'bg-green-100 text-green-800',
  UNFULFILLED: 'bg-yellow-100 text-yellow-800',
  PARTIALLY_FULFILLED: 'bg-blue-100 text-blue-800',
  CANCELED: 'bg-red-100 text-red-800',
};

export default function OrdersPage() {
  const { data, loading, error } = useQuery(GET_USER_ORDERS, {
    variables: { first: 20 },
    fetchPolicy: 'cache-first',
  });

  const orders = data?.me?.orders?.edges?.map((edge: any) => edge.node) || [];

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">My Orders</h1>

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-600 mx-auto"></div>
          <p className="mt-4 text-gray-500">Loading orders...</p>
        </div>
      ) : error ? (
        <div className="text-center py-12">
          <p className="text-red-500">Error loading orders. Please try again.</p>
        </div>
      ) : orders.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">You haven't placed any orders yet.</p>
          <Link
            href="/products"
            className="inline-block px-6 py-3 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700"
          >
            Start Shopping
          </Link>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Order #</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Items</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {orders.map((order: any) => (
                <tr key={order.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    #{order.number}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(order.created).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {order.lines?.length || 0} item{order.lines?.length !== 1 ? 's' : ''}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {new Intl.NumberFormat('en-GB', {
                      style: 'currency',
                      currency: order.total.gross.currency,
                    }).format(parseFloat(order.total.gross.amount) / 100)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span
                      className={`px-2 py-1 text-xs font-semibold rounded-full ${
                        statusColors[order.status] || statusColors.UNFULFILLED
                      }`}
                    >
                      {order.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <Link
                      href={`/account/orders/${order.number}`}
                      className="text-yellow-600 hover:text-yellow-700"
                    >
                      <EyeIcon className="h-5 w-5 inline" />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

