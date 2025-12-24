'use client';

import { useState } from 'react';
import Link from 'next/link';
import { TrashIcon, PlusIcon, MinusIcon } from '@heroicons/react/24/outline';

// Mock cart data - replace with actual cart state/context
const mockCartItems = [
  {
    id: '1',
    variantId: 'v1',
    name: '18K Gold Ring',
    variant: 'Size 6',
    price: 85000,
    currency: 'GBP',
    quantity: 1,
    image: '/placeholder-ring.jpg',
  },
];

export default function CartPage() {
  const [cartItems, setCartItems] = useState(mockCartItems);

  const updateQuantity = (id: string, delta: number) => {
    setCartItems((items) =>
      items.map((item) =>
        item.id === id
          ? { ...item, quantity: Math.max(1, item.quantity + delta) }
          : item
      )
    );
  };

  const removeItem = (id: string) => {
    setCartItems((items) => items.filter((item) => item.id !== id));
  };

  const subtotal = cartItems.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );
  const tax = subtotal * 0.2; // 20% VAT
  const total = subtotal + tax;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Shopping Cart</h1>

        {cartItems.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <p className="text-gray-500 mb-4">Your cart is empty</p>
            <Link
              href="/products"
              className="inline-block px-6 py-3 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700"
            >
              Continue Shopping
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow-md overflow-hidden">
                <div className="divide-y divide-gray-200">
                  {cartItems.map((item) => (
                    <div key={item.id} className="p-6 flex gap-4">
                      <div className="w-24 h-24 bg-gray-100 rounded-lg flex-shrink-0">
                        {item.image && (
                          <img
                            src={item.image}
                            alt={item.name}
                            className="w-full h-full object-cover rounded-lg"
                          />
                        )}
                      </div>
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-900 mb-1">{item.name}</h3>
                        {item.variant && (
                          <p className="text-sm text-gray-500 mb-2">{item.variant}</p>
                        )}
                        <div className="flex items-center justify-between">
                          <div className="flex items-center border border-gray-300 rounded-lg">
                            <button
                              onClick={() => updateQuantity(item.id, -1)}
                              className="p-1 hover:bg-gray-100"
                            >
                              <MinusIcon className="h-4 w-4" />
                            </button>
                            <span className="px-4 py-1 text-sm">{item.quantity}</span>
                            <button
                              onClick={() => updateQuantity(item.id, 1)}
                              className="p-1 hover:bg-gray-100"
                            >
                              <PlusIcon className="h-4 w-4" />
                            </button>
                          </div>
                          <div className="text-right">
                            <div className="font-semibold text-gray-900">
                              {new Intl.NumberFormat('en-GB', {
                                style: 'currency',
                                currency: item.currency,
                              }).format(item.price * item.quantity / 100)}
                            </div>
                          </div>
                        </div>
                      </div>
                      <button
                        onClick={() => removeItem(item.id)}
                        className="text-red-600 hover:text-red-700"
                      >
                        <TrashIcon className="h-5 w-5" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Order Summary */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-md p-6 sticky top-4">
                <h2 className="text-xl font-bold text-gray-900 mb-4">Order Summary</h2>
                <div className="space-y-3 mb-6">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Subtotal</span>
                    <span className="text-gray-900">
                      {new Intl.NumberFormat('en-GB', {
                        style: 'currency',
                        currency: 'GBP',
                      }).format(subtotal / 100)}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">VAT (20%)</span>
                    <span className="text-gray-900">
                      {new Intl.NumberFormat('en-GB', {
                        style: 'currency',
                        currency: 'GBP',
                      }).format(tax / 100)}
                    </span>
                  </div>
                  <div className="border-t border-gray-200 pt-3 flex justify-between font-bold">
                    <span className="text-gray-900">Total</span>
                    <span className="text-gray-900">
                      {new Intl.NumberFormat('en-GB', {
                        style: 'currency',
                        currency: 'GBP',
                      }).format(total / 100)}
                    </span>
                  </div>
                </div>
                <Link
                  href="/checkout"
                  className="block w-full text-center px-6 py-3 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 font-semibold"
                >
                  Proceed to Checkout
                </Link>
                <Link
                  href="/products"
                  className="block w-full text-center mt-3 text-gray-600 hover:text-gray-900"
                >
                  Continue Shopping
                </Link>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

