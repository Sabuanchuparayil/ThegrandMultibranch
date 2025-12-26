'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  UserCircleIcon,
  ShoppingBagIcon,
  HeartIcon,
  Cog6ToothIcon,
} from '@heroicons/react/24/outline';

const accountMenuItems = [
  { href: '/account', label: 'Account Overview', icon: UserCircleIcon },
  { href: '/account/orders', label: 'My Orders', icon: ShoppingBagIcon },
  { href: '/account/wishlist', label: 'Wishlist', icon: HeartIcon },
  { href: '/account/settings', label: 'Settings', icon: Cog6ToothIcon },
];

export default function AccountLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">My Account</h2>
              <nav className="space-y-2">
                {accountMenuItems.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname === item.href || pathname?.startsWith(item.href + '/');
                  
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={`flex items-center px-4 py-3 rounded-lg transition-colors ${
                        isActive
                          ? 'bg-yellow-50 text-yellow-700 border-l-4 border-yellow-600'
                          : 'text-gray-700 hover:bg-gray-50'
                      }`}
                    >
                      <Icon className="h-5 w-5 mr-3" />
                      {item.label}
                    </Link>
                  );
                })}
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">{children}</div>
        </div>
      </div>
    </div>
  );
}


