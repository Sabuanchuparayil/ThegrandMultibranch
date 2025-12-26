import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <h3 className="text-white font-bold text-lg mb-4">Grand Gold & Diamonds</h3>
            <p className="text-sm">
              Premium jewellery for every occasion. Quality craftsmanship, exceptional design.
            </p>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Shop</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/products" className="hover:text-yellow-400">All Products</Link></li>
              <li><Link href="/products?category=rings" className="hover:text-yellow-400">Rings</Link></li>
              <li><Link href="/products?category=necklaces" className="hover:text-yellow-400">Necklaces</Link></li>
              <li><Link href="/products?category=earrings" className="hover:text-yellow-400">Earrings</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Customer Service</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/contact" className="hover:text-yellow-400">Contact Us</Link></li>
              <li><Link href="/shipping" className="hover:text-yellow-400">Shipping</Link></li>
              <li><Link href="/returns" className="hover:text-yellow-400">Returns</Link></li>
              <li><Link href="/faq" className="hover:text-yellow-400">FAQ</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Account</h4>
            <ul className="space-y-2 text-sm">
              <li><Link href="/account" className="hover:text-yellow-400">My Account</Link></li>
              <li><Link href="/account/orders" className="hover:text-yellow-400">Order History</Link></li>
              <li><Link href="/account/wishlist" className="hover:text-yellow-400">Wishlist</Link></li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
          <p>&copy; {new Date().getFullYear()} Grand Gold & Diamonds. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}


