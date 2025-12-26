'use client';

import Link from 'next/link';
import { TrashIcon } from '@heroicons/react/24/outline';

export default function WishlistPage() {
  // Mock wishlist data - replace with GraphQL query
  const wishlistItems: any[] = [];

  return (
    <div className="bg-white rounded-lg shadow-md p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">My Wishlist</h1>

      {wishlistItems.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 mb-4">Your wishlist is empty</p>
          <Link
            href="/products"
            className="inline-block px-6 py-3 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700"
          >
            Start Shopping
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {wishlistItems.map((item) => (
            <div key={item.id} className="border border-gray-200 rounded-lg overflow-hidden">
              <div className="aspect-square bg-gray-100">
                {item.image && (
                  <img src={item.image} alt={item.name} className="w-full h-full object-cover" />
                )}
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-gray-900 mb-2">{item.name}</h3>
                <div className="flex items-center justify-between">
                  <span className="text-lg font-bold text-yellow-600">{item.price}</span>
                  <button className="text-red-600 hover:text-red-700">
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>
                <Link
                  href={`/products/${item.slug}`}
                  className="block mt-4 text-center px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700"
                >
                  View Product
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}


