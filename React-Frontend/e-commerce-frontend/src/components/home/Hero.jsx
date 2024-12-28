import React from 'react';
import { ArrowRight } from 'lucide-react';

export function Hero() {
  return (
    <div className="relative h-[600px] bg-gray-900">
      <div 
        className="absolute inset-0 bg-cover bg-center"
        style={{
          backgroundImage: 'url("https://images.unsplash.com/photo-1483985988355-763728e1935b?ixlib=rb-1.2.1&auto=format&fit=crop&w=1950&q=80")',
          opacity: '0.7'
        }}
      />
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center">
        <div className="text-white">
          <h1 className="text-5xl font-bold mb-4">New Summer Collection</h1>
          <p className="text-xl mb-8">Discover the latest trends in fashion and eyewear</p>
          <button className="bg-white text-gray-900 px-8 py-3 rounded-lg font-semibold flex items-center hover:bg-gray-100 transition-colors">
            Shop Now
            <ArrowRight className="ml-2 h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  );
}