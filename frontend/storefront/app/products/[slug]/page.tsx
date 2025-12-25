'use client';

import { useQuery, gql } from '@apollo/client';
import { useParams } from 'next/navigation';
import { useState } from 'react';
import Link from 'next/link';
import { ShoppingCartIcon, HeartIcon } from '@heroicons/react/24/outline';

const GET_PRODUCT = gql`
  query GetProduct($slug: String!) {
    product(slug: $slug) {
      id
      name
      description
      descriptionJson
      images {
        id
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
        attributes {
          attribute {
            name
          }
          values {
            name
          }
        }
      }
      category {
        name
      }
      collections {
        name
      }
    }
  }
`;

export default function ProductDetailPage() {
  const params = useParams();
  const slug = params.slug as string;
  const [selectedVariant, setSelectedVariant] = useState<string | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);

  const { data, loading, error } = useQuery(GET_PRODUCT, {
    variables: { slug },
    fetchPolicy: 'cache-first',
  });

  const product = data?.product;

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-600 mx-auto"></div>
          <p className="mt-4 text-gray-500">Loading product...</p>
        </div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-4">Product not found</p>
          <Link href="/products" className="text-yellow-600 hover:underline">
            Back to Products
          </Link>
        </div>
      </div>
    );
  }

  const defaultVariant = product.variants?.[0];
  const currentVariant = selectedVariant
    ? product.variants?.find((v: any) => v.id === selectedVariant)
    : defaultVariant;

  const price = currentVariant?.price?.amount
    ? parseFloat(currentVariant.price.amount) / 100
    : 0;
  const currency = currentVariant?.price?.currency || 'GBP';

  const handleAddToCart = () => {
    // Implement add to cart logic
    console.log('Add to cart:', {
      variantId: currentVariant?.id,
      quantity,
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Breadcrumb */}
        <nav className="mb-8 text-sm text-gray-500">
          <Link href="/" className="hover:text-yellow-600">Home</Link>
          <span className="mx-2">/</span>
          <Link href="/products" className="hover:text-yellow-600">Products</Link>
          <span className="mx-2">/</span>
          <span className="text-gray-900">{product.name}</span>
        </nav>

        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 p-8">
            {/* Product Images */}
            <div>
              <div className="aspect-square bg-gray-100 rounded-lg mb-4 relative overflow-hidden">
                {product.images && product.images.length > 0 ? (
                  <img
                    src={product.images[selectedImage]?.url}
                    alt={product.images[selectedImage]?.alt || product.name}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-gray-400">
                    No Image Available
                  </div>
                )}
              </div>
              {product.images && product.images.length > 1 && (
                <div className="flex gap-2 overflow-x-auto">
                  {product.images.map((image: any, index: number) => (
                    <button
                      key={image.id}
                      onClick={() => setSelectedImage(index)}
                      className={`flex-shrink-0 w-20 h-20 rounded-lg overflow-hidden border-2 ${
                        selectedImage === index ? 'border-yellow-600' : 'border-gray-200'
                      }`}
                    >
                      <img
                        src={image.url}
                        alt={image.alt || `${product.name} ${index + 1}`}
                        className="w-full h-full object-cover"
                      />
                    </button>
                  ))}
                </div>
              )}
            </div>

            {/* Product Info */}
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-4">{product.name}</h1>
              
              {product.category && (
                <p className="text-sm text-gray-500 mb-4">Category: {product.category.name}</p>
              )}

              <div className="mb-6">
                <div className="text-3xl font-bold text-yellow-600 mb-2">
                  {new Intl.NumberFormat('en-GB', {
                    style: 'currency',
                    currency: currency,
                  }).format(price)}
                </div>
                {currentVariant?.sku && (
                  <p className="text-sm text-gray-500">SKU: {currentVariant.sku}</p>
                )}
              </div>

              <div className="mb-6">
                <p className="text-gray-700 whitespace-pre-line">
                  {product.description || 'No description available'}
                </p>
              </div>

              {/* Variant Selection */}
              {product.variants && product.variants.length > 1 && (
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Select Variant
                  </label>
                  <div className="grid grid-cols-2 gap-2">
                    {product.variants.map((variant: any) => (
                      <button
                        key={variant.id}
                        onClick={() => setSelectedVariant(variant.id)}
                        className={`px-4 py-2 border-2 rounded-lg text-sm font-medium ${
                          selectedVariant === variant.id || (!selectedVariant && variant.id === defaultVariant?.id)
                            ? 'border-yellow-600 bg-yellow-50 text-yellow-900'
                            : 'border-gray-200 text-gray-700 hover:border-gray-300'
                        }`}
                      >
                        {variant.name}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Quantity */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">Quantity</label>
                <div className="flex items-center">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="px-3 py-2 border border-gray-300 rounded-l-lg hover:bg-gray-50"
                  >
                    -
                  </button>
                  <input
                    type="number"
                    min="1"
                    value={quantity}
                    onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                    className="w-16 px-4 py-2 border-t border-b border-gray-300 text-center focus:outline-none focus:ring-2 focus:ring-yellow-500"
                  />
                  <button
                    onClick={() => setQuantity(quantity + 1)}
                    className="px-3 py-2 border border-gray-300 rounded-r-lg hover:bg-gray-50"
                  >
                    +
                  </button>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-4 mb-6">
                <button
                  onClick={handleAddToCart}
                  className="flex-1 flex items-center justify-center px-6 py-3 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 font-semibold"
                >
                  <ShoppingCartIcon className="h-5 w-5 mr-2" />
                  Add to Cart
                </button>
                <button className="px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50">
                  <HeartIcon className="h-5 w-5" />
                </button>
              </div>

              {/* Product Attributes */}
              {currentVariant?.attributes && currentVariant.attributes.length > 0 && (
                <div className="border-t border-gray-200 pt-6">
                  <h3 className="text-sm font-medium text-gray-900 mb-4">Product Details</h3>
                  <dl className="space-y-2">
                    {currentVariant.attributes.map((attr: any, index: number) => (
                      <div key={index} className="flex">
                        <dt className="text-sm text-gray-500 w-32">{attr.attribute.name}:</dt>
                        <dd className="text-sm text-gray-900">
                          {attr.values.map((v: any) => v.name).join(', ')}
                        </dd>
                      </div>
                    ))}
                  </dl>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

