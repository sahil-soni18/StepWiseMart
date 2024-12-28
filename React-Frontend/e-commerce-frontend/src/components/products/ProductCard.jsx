import React from 'react';
import { Star, ShoppingCart } from 'lucide-react';

export function ProductCard({ product }) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      <div className="relative pb-[100%]">
        <img
          src={product.images[0]}
          alt={product.name}
          className="absolute inset-0 w-full h-full object-cover"
        />
      </div>
      <div className="p-4">
        <h3 className="text-lg font-semibold mb-2">{product.name}</h3>
        <div className="flex items-center mb-2">
          <Star className="h-4 w-4 text-yellow-400 fill-current" />
          <span className="ml-1 text-sm text-gray-600">{product.rating}</span>
        </div>
        <div className="flex items-center justify-between">
          <span className="text-xl font-bold">${product.price}</span>
          <button className="bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700">
            <ShoppingCart className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  );
}
