import React from 'react';
import { ShoppingCart, Search, User, Menu } from 'lucide-react';

export function Navbar() {
  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex-shrink-0">
            <h1 className="text-2xl font-bold text-gray-900">StepWiseMart</h1>
          </div>
          
          <div className="hidden md:block flex-1 px-8">
            <div className="relative">
              <input
                type="text"
                placeholder="Search products..."
                className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <Search className="absolute right-3 top-2.5 h-5 w-5 text-gray-400" />
            </div>
          </div>

          <div className="hidden md:flex items-center space-x-6">
            <a href="/cart" className="text-gray-600 hover:text-gray-900">
              <ShoppingCart className="h-6 w-6" />
            </a>
            <a href="/account" className="text-gray-600 hover:text-gray-900">
              <User className="h-6 w-6" />
            </a>
          </div>

          <div className="md:hidden">
            <Menu className="h-6 w-6 text-gray-600" />
          </div>
        </div>
      </div>
    </nav>
  );
}