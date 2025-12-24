import Link from 'next/link';
import Image from 'next/image';

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-yellow-600 to-yellow-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">Grand Gold & Diamonds</h1>
          <p className="text-xl md:text-2xl mb-8">Exquisite Jewellery for Every Occasion</p>
          <Link
            href="/products"
            className="inline-block bg-white text-yellow-800 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
          >
            Shop Now
          </Link>
        </div>
      </section>

      {/* Categories */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Shop by Category</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { name: 'Rings', href: '/products?category=rings', image: '💍' },
              { name: 'Necklaces', href: '/products?category=necklaces', image: '📿' },
              { name: 'Earrings', href: '/products?category=earrings', image: '👂' },
              { name: 'Bracelets', href: '/products?category=bracelets', image: '💎' },
            ].map((category) => (
              <Link
                key={category.name}
                href={category.href}
                className="bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow"
              >
                <div className="text-6xl mb-4">{category.image}</div>
                <h3 className="text-xl font-semibold text-gray-900">{category.name}</h3>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-12">Featured Products</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Product cards will be loaded via GraphQL */}
            <p className="col-span-full text-center text-gray-500">Loading featured products...</p>
          </div>
        </div>
      </section>
    </div>
  );
}
