'use client';

import Link from 'next/link';
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
} from '@heroicons/react/24/outline';

const modules = [
  { href: '/admin/modules/branches', label: 'Branches', icon: BuildingStorefrontIcon, color: 'blue', count: 12 },
  { href: '/admin/modules/inventory', label: 'Inventory', icon: CubeIcon, color: 'green', count: '1,245' },
  { href: '/admin/modules/products', label: 'Products', icon: ShoppingBagIcon, color: 'purple', count: 856 },
  { href: '/admin/modules/orders', label: 'Orders', icon: ShoppingBagIcon, color: 'orange', count: 342 },
  { href: '/admin/modules/customers', label: 'Customers', icon: UserGroupIcon, color: 'indigo', count: '3,421' },
  { href: '/admin/modules/pricing', label: 'Pricing', icon: CurrencyDollarIcon, color: 'yellow', count: 'Active' },
  { href: '/admin/modules/taxes', label: 'Taxes', icon: ReceiptPercentIcon, color: 'red', count: 3 },
  { href: '/admin/modules/fulfillment', label: 'Fulfillment', icon: TruckIcon, color: 'teal', count: 128 },
  { href: '/admin/modules/returns', label: 'Returns', icon: ArrowPathIcon, color: 'pink', count: 24 },
  { href: '/admin/modules/promotions', label: 'Promotions', icon: TagIcon, color: 'cyan', count: 15 },
  { href: '/admin/modules/reports', label: 'Reports', icon: ChartBarIcon, color: 'gray', count: 'View' },
  { href: '/admin/modules/settings', label: 'Settings', icon: Cog6ToothIcon, color: 'slate', count: 'Manage' },
];

const colorClasses = {
  blue: 'bg-blue-500',
  green: 'bg-green-500',
  purple: 'bg-purple-500',
  orange: 'bg-orange-500',
  indigo: 'bg-indigo-500',
  yellow: 'bg-yellow-500',
  red: 'bg-red-500',
  teal: 'bg-teal-500',
  pink: 'bg-pink-500',
  cyan: 'bg-cyan-500',
  gray: 'bg-gray-500',
  slate: 'bg-slate-500',
};

export default function AdminDashboard() {
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-1">Manage all aspects of your jewellery business</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {modules.map((module) => {
            const Icon = module.icon;
            const bgColor = colorClasses[module.color as keyof typeof colorClasses] || colorClasses.blue;
            
            return (
              <Link
                key={module.href}
                href={module.href}
                className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow group"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className={`${bgColor} p-3 rounded-lg group-hover:scale-110 transition-transform`}>
                    <Icon className="h-8 w-8 text-white" />
                  </div>
                  <span className="text-sm font-medium text-gray-500">{module.count}</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                  {module.label}
                </h3>
                <p className="text-sm text-gray-500 mt-2">Manage {module.label.toLowerCase()}</p>
              </Link>
            );
          })}
        </div>
      </div>
    </div>
  );
}

