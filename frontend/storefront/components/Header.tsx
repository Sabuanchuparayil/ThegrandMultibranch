'use client';

import Link from 'next/link';
import { useState } from 'react';
import { MagnifyingGlassIcon, ShoppingCartIcon, UserCircleIcon, Bars3Icon } from '@heroicons/react/24/outline';

export default function Header() {
  const [searchOpen, setSearchOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="text-2xl font-bold text-yellow-600">
            Grand Gold
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link href="/products" className="text-gray-700 hover:text-yellow-600 font-medium">
              Products
            </Link>
            <Link href="/collections" className="text-gray-700 hover:text-yellow-600 font-medium">
              Collections
            </Link>
            <Link href="/about" className="text-gray-700 hover:text-yellow-600 font-medium">
              About
            </Link>
          </nav>

          {/* Actions */}
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setSearchOpen(!searchOpen)}
              className="text-gray-700 hover:text-yellow-600"
            >
              <MagnifyingGlassIcon className="h-6 w-6" />
            </button>
            <Link href="/cart" className="text-gray-700 hover:text-yellow-600 relative">
              <ShoppingCartIcon className="h-6 w-6" />
              <span className="absolute -top-2 -right-2 bg-yellow-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                0
              </span>
            </Link>
            <Link href="/account" className="text-gray-700 hover:text-yellow-600">
              <UserCircleIcon className="h-6 w-6" />
            </Link>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden text-gray-700 hover:text-yellow-600"
            >
              <Bars3Icon className="h-6 w-6" />
            </button>
          </div>
        </div>

        {/* Search Bar */}
        {searchOpen && (
          <div className="pb-4">
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search products..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-yellow-500"
                autoFocus
              />
            </div>
          </div>
        )}

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t border-gray-200">
            <nav className="space-y-2">
              <Link href="/products" className="block px-4 py-2 text-gray-700 hover:bg-gray-50">
                Products
              </Link>
              <Link href="/collections" className="block px-4 py-2 text-gray-700 hover:bg-gray-50">
                Collections
              </Link>
              <Link href="/about" className="block px-4 py-2 text-gray-700 hover:bg-gray-50">
                About
              </Link>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
}


