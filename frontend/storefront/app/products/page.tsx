'use client';

import { useState } from 'react';
import { useQuery, gql } from '@apollo/client';
import Link from 'next/link';
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline';

const GET_PRODUCTS = gql`
  query GetProducts($first: Int, $filter: ProductFilterInput, $sortBy: ProductOrder) {
    products(first: $first, filter: $filter, sortBy: $sortBy) {
      edges {
        node {
          id
          name
          slug
          description
          thumbnail {
            url
            alt
          }
          variants {
            id
            name
            sku
            price {
              amount
              currency
            }
          }
          category {
            name
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

export default function ProductsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState('PRICE');
  const [showFilters, setShowFilters] = useState(false);

  const { data, loading, error } = useQuery(GET_PRODUCTS, {
    variables: {
      first: 24,
      filter: {
        search: searchTerm || null,
        categories: selectedCategory ? [selectedCategory] : null,
      },
      sortBy: sortBy,
    },
    fetchPolicy: 'cache-first',
  });

  const products = data?.products?.edges?.map((edge: any) => edge.node) || [];

  const categories = ['Rings', 'Necklaces', 'Earrings', 'Bracelets'];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Product Catalog</h1>
          
          {/* Search and Filters */}
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search products..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
              />
            </div>
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              <FunnelIcon className="h-5 w-5 mr-2" />
              Filters
            </button>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
            >
              <option value="PRICE">Price: Low to High</option>
              <option value="-PRICE">Price: High to Low</option>
              <option value="NAME">Name: A to Z</option>
              <option value="-NAME">Name: Z to A</option>
              <option value="CREATED_AT">Newest First</option>
            </select>
          </div>

          {/* Category Filters */}
          {showFilters && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="flex flex-wrap gap-2">
                <button
                  onClick={() => setSelectedCategory(null)}
                  className={`px-4 py-2 rounded-lg ${
                    !selectedCategory
                      ? 'bg-yellow-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  All
                </button>
                {categories.map((category) => (
                  <button
                    key={category}
                    onClick={() => setSelectedCategory(category)}
                    className={`px-4 py-2 rounded-lg ${
                      selectedCategory === category
                        ? 'bg-yellow-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Products Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-600 mx-auto"></div>
            <p className="mt-4 text-gray-500">Loading products...</p>
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <p className="text-red-500">Error loading products. Please try again.</p>
          </div>
        ) : products.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">No products found.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map((product: any) => {
              const variant = product.variants?.[0];
              const price = variant?.price?.amount
                ? parseFloat(variant.price.amount) / 100
                : 0;
              const currency = variant?.price?.currency || 'GBP';

              return (
                <Link
                  key={product.id}
                  href={`/products/${product.slug}`}
                  className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow"
                >
                  <div className="aspect-square bg-gray-100 relative">
                    {product.thumbnail ? (
                      <img
                        src={product.thumbnail.url}
                        alt={product.thumbnail.alt || product.name}
                        className="w-full h-full object-cover"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-400">
                        No Image
                      </div>
                    )}
                  </div>
                  <div className="p-4">
                    <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2">{product.name}</h3>
                    <p className="text-sm text-gray-500 mb-2 line-clamp-2">
                      {product.description || 'Beautiful jewellery piece'}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-lg font-bold text-yellow-600">
                        {new Intl.NumberFormat('en-GB', {
                          style: 'currency',
                          currency: currency,
                        }).format(price)}
                      </span>
                      {variant?.sku && (
                        <span className="text-xs text-gray-400">SKU: {variant.sku}</span>
                      )}
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>
        )}

        {/* Pagination */}
        {data?.products?.pageInfo?.hasNextPage && (
          <div className="mt-8 text-center">
            <button className="px-6 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700">
              Load More
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

