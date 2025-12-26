'use client';

import { useParams, useRouter } from 'next/navigation';
import { useQuery, gql } from '@apollo/client';
import { ArrowLeftIcon, TruckIcon, CalendarIcon, CreditCardIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';

const GET_ORDER = gql`
  query GetOrder($number: String!) {
    orderByNumber(number: $number) {
      id
      number
      status
      created
      total {
        gross {
          amount
          currency
        }
        net {
          amount
          currency
        }
        tax {
          amount
          currency
        }
      }
      lines {
        id
        productName
        variantName
        quantity
        unitPrice {
          gross {
            amount
            currency
          }
        }
        totalPrice {
          gross {
            amount
            currency
          }
        }
        thumbnail {
          url
          alt
        }
      }
      shippingAddress {
        firstName
        lastName
        streetAddress1
        streetAddress2
        city
        postalCode
        country {
          country
        }
      }
      billingAddress {
        firstName
        lastName
        streetAddress1
        streetAddress2
        city
        postalCode
        country {
          country
        }
      }
      paymentStatus
      fulfillmentStatus
    }
  }
`;

export default function OrderDetailPage() {
  const params = useParams();
  const router = useRouter();
  const orderNumber = params.number as string;

  const { data, loading, error } = useQuery(GET_ORDER, {
    variables: { number: orderNumber },
    skip: !orderNumber,
  });

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg shadow-md p-8">
            <div className="animate-pulse">
              <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
              <div className="space-y-4">
                <div className="h-20 bg-gray-200 rounded"></div>
                <div className="h-20 bg-gray-200 rounded"></div>
                <div className="h-20 bg-gray-200 rounded"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg shadow-md p-8">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Error Loading Order</h2>
              <p className="text-gray-600 mb-6">{error.message}</p>
              <button
                onClick={() => router.push('/account/orders')}
                className="bg-yellow-600 text-white px-6 py-2 rounded-lg hover:bg-yellow-700"
              >
                Back to Orders
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const order = data?.orderByNumber;

  if (!order) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg shadow-md p-8">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900 mb-4">Order Not Found</h2>
              <p className="text-gray-600 mb-6">The order you're looking for doesn't exist.</p>
              <button
                onClick={() => router.push('/account/orders')}
                className="bg-yellow-600 text-white px-6 py-2 rounded-lg hover:bg-yellow-700"
              >
                Back to Orders
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  const formatCurrency = (amount: number, currency: string) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency || 'GBP',
    }).format(amount / 100);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const getStatusColor = (status: string) => {
    const statusMap: Record<string, string> = {
      FULFILLED: 'bg-green-100 text-green-800',
      UNFULFILLED: 'bg-yellow-100 text-yellow-800',
      PARTIALLY_FULFILLED: 'bg-blue-100 text-blue-800',
      CANCELED: 'bg-red-100 text-red-800',
      RETURNED: 'bg-gray-100 text-gray-800',
    };
    return statusMap[status] || 'bg-gray-100 text-gray-800';
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => router.back()}
            className="flex items-center text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeftIcon className="h-5 w-5 mr-2" />
            Back to Orders
          </button>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Order #{order.number}</h1>
              <p className="text-gray-600 mt-1">Placed on {formatDate(order.created)}</p>
            </div>
            <span className={`px-4 py-2 rounded-full text-sm font-medium ${getStatusColor(order.status)}`}>
              {order.status.replace('_', ' ')}
            </span>
          </div>
        </div>

        {/* Order Items */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Order Items</h2>
          <div className="space-y-4">
            {order.lines?.map((line: any) => (
              <div key={line.id} className="flex items-center space-x-4 border-b border-gray-200 pb-4 last:border-0">
                {line.thumbnail && (
                  <img
                    src={line.thumbnail.url}
                    alt={line.thumbnail.alt || line.productName}
                    className="w-20 h-20 object-cover rounded"
                  />
                )}
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900">{line.productName}</h3>
                  {line.variantName && (
                    <p className="text-sm text-gray-600">Variant: {line.variantName}</p>
                  )}
                  <p className="text-sm text-gray-600">Quantity: {line.quantity}</p>
                </div>
                <div className="text-right">
                  <p className="font-semibold text-gray-900">
                    {formatCurrency(line.totalPrice.gross.amount, line.totalPrice.gross.currency)}
                  </p>
                  <p className="text-sm text-gray-600">
                    {formatCurrency(line.unitPrice.gross.amount, line.unitPrice.gross.currency)} each
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Order Summary */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Shipping Address */}
          {order.shippingAddress && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <TruckIcon className="h-5 w-5 mr-2" />
                Shipping Address
              </h3>
              <div className="text-gray-600">
                <p>{order.shippingAddress.firstName} {order.shippingAddress.lastName}</p>
                <p>{order.shippingAddress.streetAddress1}</p>
                {order.shippingAddress.streetAddress2 && (
                  <p>{order.shippingAddress.streetAddress2}</p>
                )}
                <p>
                  {order.shippingAddress.city}, {order.shippingAddress.postalCode}
                </p>
                <p>{order.shippingAddress.country?.country}</p>
              </div>
            </div>
          )}

          {/* Billing Address */}
          {order.billingAddress && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <CreditCardIcon className="h-5 w-5 mr-2" />
                Billing Address
              </h3>
              <div className="text-gray-600">
                <p>{order.billingAddress.firstName} {order.billingAddress.lastName}</p>
                <p>{order.billingAddress.streetAddress1}</p>
                {order.billingAddress.streetAddress2 && (
                  <p>{order.billingAddress.streetAddress2}</p>
                )}
                <p>
                  {order.billingAddress.city}, {order.billingAddress.postalCode}
                </p>
                <p>{order.billingAddress.country?.country}</p>
              </div>
            </div>
          )}
        </div>

        {/* Order Totals */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Order Summary</h3>
          <div className="space-y-2">
            <div className="flex justify-between text-gray-600">
              <span>Subtotal</span>
              <span>{formatCurrency(order.total.net.amount, order.total.net.currency)}</span>
            </div>
            {order.total.tax && order.total.tax.amount > 0 && (
              <div className="flex justify-between text-gray-600">
                <span>Tax</span>
                <span>{formatCurrency(order.total.tax.amount, order.total.tax.currency)}</span>
              </div>
            )}
            <div className="border-t border-gray-200 pt-2 mt-2">
              <div className="flex justify-between text-lg font-bold text-gray-900">
                <span>Total</span>
                <span>{formatCurrency(order.total.gross.amount, order.total.gross.currency)}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}


