import React from 'react';
import { Navbar } from './components/layout/Navbar';
import { Hero } from './components/home/Hero';
import { ProductGrid } from './components/products/ProductGrid';

// Mock data - replace with actual API calls
const mockProducts = [
  {
    id: '1',
    name: 'Classic Aviator Sunglasses',
    description: 'Timeless aviator design with UV protection',
    price: 129.99,
    category: 'Sunglasses',
    images: ['https://images.unsplash.com/photo-1572635196237-14b3f281503f?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80'],
    rating: 4.5,
    reviews: [],
    inStock: true
  },
  {
    id: '2',
    name: 'Designer Optical Frames',
    description: 'Modern optical frames for everyday wear',
    price: 199.99,
    category: 'Eyewear',
    images: ['https://images.unsplash.com/photo-1574258495973-f010dfbb5371?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80'],
    rating: 4.8,
    reviews: [],
    inStock: true
  }
];

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <Hero />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-8">Featured Products</h2>
          <ProductGrid products={mockProducts} />
        </section>
      </main>
    </div>
  );
}

export default App;