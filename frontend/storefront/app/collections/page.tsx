import Link from 'next/link';

export default function CollectionsPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Collections</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            { name: 'Wedding Collection', href: '/products?collection=wedding', description: 'Elegant pieces for your special day' },
            { name: 'Engagement Rings', href: '/products?category=rings&collection=engagement', description: 'Symbols of eternal love' },
            { name: 'Luxury Collection', href: '/products?collection=luxury', description: 'Premium designs for the discerning' },
            { name: 'Everyday Elegance', href: '/products?collection=everyday', description: 'Timeless pieces for daily wear' },
            { name: 'Vintage Collection', href: '/products?collection=vintage', description: 'Classic designs with modern appeal' },
            { name: 'Custom Designs', href: '/products?collection=custom', description: 'Bespoke jewellery crafted for you' },
          ].map((collection) => (
            <Link
              key={collection.name}
              href={collection.href}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
            >
              <h2 className="text-xl font-semibold text-gray-900 mb-2">{collection.name}</h2>
              <p className="text-gray-600">{collection.description}</p>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}


