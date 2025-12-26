/**
 * Admin Layout
 * Main layout for all admin modules with navigation sidebar
 */

'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  BuildingStorefrontIcon,
  CubeIcon,
  ShoppingBagIcon,
  UserGroupIcon,
  CurrencyDollarIcon,
  ReceiptPercentIcon,
  TruckIcon,
  ArrowPathIcon,
  TagIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  HomeIcon,
  PresentationChartLineIcon,
} from '@heroicons/react/24/outline';

const modules = [
  { href: '/admin', label: 'Dashboard', icon: HomeIcon },
  { href: '/admin/dashboard', label: 'Analytics Dashboards', icon: PresentationChartLineIcon },
  { href: '/admin/modules/branches', label: 'Branches', icon: BuildingStorefrontIcon },
  { href: '/admin/modules/inventory', label: 'Inventory', icon: CubeIcon },
  { href: '/admin/modules/products', label: 'Products', icon: ShoppingBagIcon },
  { href: '/admin/modules/orders', label: 'Orders', icon: ShoppingBagIcon },
  { href: '/admin/modules/customers', label: 'Customers', icon: UserGroupIcon },
  { href: '/admin/modules/pricing', label: 'Pricing', icon: CurrencyDollarIcon },
  { href: '/admin/modules/taxes', label: 'Taxes', icon: ReceiptPercentIcon },
  { href: '/admin/modules/fulfillment', label: 'Fulfillment', icon: TruckIcon },
  { href: '/admin/modules/returns', label: 'Returns', icon: ArrowPathIcon },
  { href: '/admin/modules/promotions', label: 'Promotions', icon: TagIcon },
  { href: '/admin/modules/reports', label: 'Reports', icon: ChartBarIcon },
  { href: '/admin/modules/settings', label: 'Settings', icon: Cog6ToothIcon },
];

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    window.location.href = '/login';
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white shadow-lg fixed h-full">
        <div className="p-6 border-b border-gray-200">
          <h1 className="text-xl font-bold text-gray-900">Grand Gold Admin</h1>
          <p className="text-sm text-gray-500 mt-1">Management System</p>
        </div>
        
        {/* Logout Button */}
        <div className="p-4 border-b border-gray-200">
          <button
            onClick={handleLogout}
            className="w-full flex items-center justify-center px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors"
          >
            <svg
              className="h-5 w-5 mr-2"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
              />
            </svg>
            Logout
          </button>
        </div>
        
        <nav className="p-4 space-y-1 overflow-y-auto h-[calc(100vh-120px)]">
          {modules.map((module) => {
            const Icon = module.icon;
            const isActive = pathname === module.href || pathname?.startsWith(module.href + '/');
            
            return (
              <Link
                key={module.href}
                href={module.href}
                className={`flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                  isActive
                    ? 'bg-blue-50 text-blue-700 border-l-4 border-blue-700'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                <Icon className="h-5 w-5 mr-3" />
                {module.label}
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 ml-64">
        {children}
      </main>
    </div>
  );
}

