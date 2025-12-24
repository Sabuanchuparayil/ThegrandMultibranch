'use client';

import Link from 'next/link';
import { CheckCircleIcon } from '@heroicons/react/24/outline';

export default function CheckoutConfirmationPage() {
  // In real app, get order details from URL params or query
  const orderNumber = '12345';
  const orderTotal = '£1,032.00';

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <CheckCircleIcon className="h-16 w-16 text-green-500 mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Order Confirmed!</h1>
          <p className="text-gray-600 mb-6">
            Thank you for your order. We've sent a confirmation email with your order details.
          </p>
          <div className="bg-gray-50 rounded-lg p-6 mb-8">
            <div className="flex justify-between items-center mb-2">
              <span className="text-gray-600">Order Number:</span>
              <span className="font-semibold text-gray-900">#{orderNumber}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Total:</span>
              <span className="font-semibold text-gray-900">{orderTotal}</span>
            </div>
          </div>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/account/orders"
              className="px-6 py-3 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 font-semibold"
            >
              View Order
            </Link>
            <Link
              href="/products"
              className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-semibold"
            >
              Continue Shopping
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

