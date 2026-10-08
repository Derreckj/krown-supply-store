"use client";

import React, { useState, useMemo } from 'react';
import ProductCard from '@/components/product/ProductCard';
import { CatalogProduct } from '@/services/printify';
import './SearchPage.css';

interface SearchClientProps {
  initialProducts: CatalogProduct[];
}

export default function SearchClient({ initialProducts }: SearchClientProps) {
  const [query, setQuery] = useState('');
  const [selectedDivision, setSelectedDivision] = useState('ALL');
  const [sortBy, setSortBy] = useState('featured');

  const divisions = [
    { id: 'ALL', label: 'All Divisions' },
    { id: 'KrowN Supply Co.', label: 'KrowN Supply Co.' },
    { id: 'KrowN Construction', label: 'KrowN Construction' },
    { id: 'AXA / Axiom Allegiance', label: 'AXA Esports' },
  ];

  const filteredProducts = useMemo(() => {
    let result = [...initialProducts];

    // Filter by division
    if (selectedDivision !== 'ALL') {
      result = result.filter(p => p.collection === selectedDivision);
    }

    // Filter by search query
    if (query.trim()) {
      const q = query.toLowerCase();
      result = result.filter(p => 
        p.name.toLowerCase().includes(q) ||
        p.description.toLowerCase().includes(q) ||
        p.collection.toLowerCase().includes(q) ||
        (p.material && p.material.toLowerCase().includes(q))
      );
    }

    // Sort
    if (sortBy === 'price-low') {
      result.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-high') {
      result.sort((a, b) => b.price - a.price);
    } else if (sortBy === 'name') {
      result.sort((a, b) => a.name.localeCompare(b.name));
    }

    return result;
  }, [initialProducts, selectedDivision, query, sortBy]);

  return (
    <div className="search-page container">
      <div className="search-header">
        <h1 className="search-title">Search Catalog</h1>
        <p className="search-subtitle">Search across KrowN Supply Co., KrowN Construction &amp; Axiom Gaming gear</p>
        
        <div className="search-input-wrapper">
          <svg className="search-icon" width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input
            type="text"
            className="search-input"
            placeholder="Search by product name, trade, gaming, blank (e.g. tumbler, sleeve, beanie, 1717)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
          />
          {query && (
            <button 
              type="button" 
              className="search-clear-btn"
              onClick={() => setQuery('')}
              aria-label="Clear search query"
            >
              ✕
            </button>
          )}
        </div>
      </div>

      <div className="search-filters">
        <div className="filter-pills">
          {divisions.map((div) => (
            <button
              key={div.id}
              type="button"
              className={`filter-pill ${selectedDivision === div.id ? 'active' : ''}`}
              onClick={() => setSelectedDivision(div.id)}
            >
              {div.label}
            </button>
          ))}
        </div>

        <div className="search-sort">
          <select 
            value={sortBy} 
            onChange={(e) => setSortBy(e.target.value)}
            aria-label="Sort products"
          >
            <option value="featured">Sort: Featured</option>
            <option value="price-low">Price: Low to High</option>
            <option value="price-high">Price: High to Low</option>
            <option value="name">Alphabetical (A–Z)</option>
          </select>
        </div>
      </div>

      <div className="search-results-info">
        <span>Showing <strong>{filteredProducts.length}</strong> {filteredProducts.length === 1 ? 'product' : 'products'}</span>
      </div>

      {filteredProducts.length > 0 ? (
        <div className="product-grid">
          {filteredProducts.map((product) => (
            <ProductCard
              key={product.id}
              id={product.id}
              name={product.name}
              price={product.price}
              collection={product.collection}
              image={product.images[0] || ''}
              hoverImage={product.images[1] || ''}
              isNew={product.isNew}
              isLimited={product.isLimited}
            />
          ))}
        </div>
      ) : (
        <div className="search-empty">
          <h3>No matching gear found</h3>
          <p className="text-muted">Try adjusting your search terms or clearing division filters.</p>
          <button 
            type="button" 
            className="btn-primary" 
            style={{ marginTop: '1.5rem' }}
            onClick={() => { setQuery(''); setSelectedDivision('ALL'); }}
          >
            Reset Filters
          </button>
        </div>
      )}
    </div>
  );
}
