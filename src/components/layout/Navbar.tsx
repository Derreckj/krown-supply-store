"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useCart } from '@/context/CartContext';
import './Navbar.css';

export default function Navbar() {
  const { cartCount, setIsCartOpen } = useCart();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const pathname = usePathname();

  const categories = [
    { name: 'The Vault', slug: '/collections/all', icon: '★' },
    { name: 'Streetwear', slug: '/collections/supply', icon: '👑' },
    { name: 'Construction', slug: '/collections/construction', icon: '🔨' },
    { name: 'AXA Esports', slug: '/collections/gaming', icon: '⚡' },
    { name: 'Custom Hats ★', slug: '/custom-crew', isGold: true },
    { name: 'Decals & Acc', slug: '/collections/accessories', icon: '🏷️' },
  ];

  return (
    <header className="navbar-wrapper">
      <div className="navbar">
        <div className="navbar-container container">
          <Link href="/" className="navbar-brand">
            <img 
              src="/images/branding/krown-definitive-logo.png" 
              alt="KrowN Supply Co." 
              className="navbar-logo-icon" 
            />
            <span className="navbar-brand-text">KrowN <span className="text-gold">Supply Co.</span></span>
          </Link>

          <nav className="navbar-links">
            <Link href="/collections/all" className={pathname === '/collections/all' ? 'active-link' : ''}>The Vault // All</Link>
            <Link href="/collections/supply" className={pathname === '/collections/supply' || pathname === '/collections/core' ? 'active-link' : ''}>KrowN Supply Co.</Link>
            <Link href="/collections/gaming" className={pathname === '/collections/gaming' || pathname === '/collections/axiom' ? 'active-link' : ''}>AXA Esports</Link>
            <Link href="/collections/construction" className={pathname === '/collections/construction' || pathname === '/collections/workwear' ? 'active-link' : ''}>KrowN Construction</Link>
            <Link href="/custom-crew" className={pathname === '/custom-crew' ? 'active-link custom-crew-link' : 'custom-crew-link'}>Custom Hats ★</Link>
          </nav>

          <div className="navbar-actions">
            <Link href="/search" className="navbar-action-btn" aria-label="Search Catalog">
              <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </Link>

            <button 
              className="navbar-cart-link navbar-action-btn" 
              aria-label={`View Cart (${cartCount} items)`}
              onClick={() => setIsCartOpen(true)}
            >
              <svg width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <path d="M16 10a4 4 0 0 1-8 0"></path>
              </svg>
              {cartCount > 0 && (
                <span className="navbar-cart-badge">{cartCount}</span>
              )}
            </button>

            <button 
              className="navbar-mobile-toggle"
              aria-label="Toggle Navigation Menu"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? (
                <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              ) : (
                <svg width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                  <line x1="3" y1="12" x2="21" y2="12"></line>
                  <line x1="3" y1="6" x2="21" y2="6"></line>
                  <line x1="3" y1="18" x2="21" y2="18"></line>
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>

      {/* STICKY TOP MOBILE CATEGORY BAR (DIRECTLY ACCESSIBLE AT THE TOP ON MOBILE) */}
      <div className="mobile-category-bar">
        <div className="mobile-category-scroll">
          {categories.map((cat) => {
            const isActive = pathname === cat.slug;
            return (
              <Link 
                key={cat.slug} 
                href={cat.slug} 
                className={`mobile-cat-pill ${isActive ? 'active' : ''} ${cat.isGold ? 'gold-pill' : ''}`}
              >
                {cat.icon && <span className="cat-icon">{cat.icon}</span>}
                {cat.name}
              </Link>
            );
          })}
        </div>
      </div>

      {/* FULL-FEATURED MOBILE DRAWER MENU */}
      {mobileMenuOpen && (
        <div className="mobile-menu-drawer">
          <div className="mobile-menu-content container">
            <div className="mobile-menu-section-title">Shop by Division</div>
            <div className="mobile-menu-links">
              <Link 
                href="/collections/all" 
                onClick={() => setMobileMenuOpen(false)}
                className={`mobile-menu-item ${pathname === '/collections/all' ? 'active' : ''}`}
              >
                <span className="menu-icon">★</span>
                <div>
                  <strong>The Vault // All Catalog</strong>
                  <p>Browse full 2024 luxury collection</p>
                </div>
              </Link>
              <Link 
                href="/collections/supply" 
                onClick={() => setMobileMenuOpen(false)}
                className={`mobile-menu-item ${pathname === '/collections/supply' ? 'active' : ''}`}
              >
                <span className="menu-icon">👑</span>
                <div>
                  <strong>KrowN Supply Co.</strong>
                  <p>480 GSM French Terry Streetwear</p>
                </div>
              </Link>
              <Link 
                href="/collections/construction" 
                onClick={() => setMobileMenuOpen(false)}
                className={`mobile-menu-item ${pathname === '/collections/construction' ? 'active' : ''}`}
              >
                <span className="menu-icon">🔨</span>
                <div>
                  <strong>KrowN Construction LLC</strong>
                  <p>Built to Reign Jobsite Gear &amp; Headwear</p>
                </div>
              </Link>
              <Link 
                href="/collections/gaming" 
                onClick={() => setMobileMenuOpen(false)}
                className={`mobile-menu-item ${pathname === '/collections/gaming' ? 'active' : ''}`}
              >
                <span className="menu-icon">⚡</span>
                <div>
                  <strong>AXA // Axiom Allegiance</strong>
                  <p>Pro League Sublimated Esports Gear</p>
                </div>
              </Link>
              <Link 
                href="/custom-crew" 
                onClick={() => setMobileMenuOpen(false)}
                className="mobile-menu-item mobile-menu-gold"
              >
                <span className="menu-icon">🧢</span>
                <div>
                  <strong>Custom Richardson 112 Hats ★</strong>
                  <p>Laser engraved leatherette patches</p>
                </div>
              </Link>
              <Link 
                href="/collections/accessories" 
                onClick={() => setMobileMenuOpen(false)}
                className={`mobile-menu-item ${pathname === '/collections/accessories' ? 'active' : ''}`}
              >
                <span className="menu-icon">🏷️</span>
                <div>
                  <strong>Weatherproof Decals &amp; Accessories</strong>
                  <p>Hardhat stickers, desk mats &amp; drinkware</p>
                </div>
              </Link>
            </div>

            <div className="mobile-menu-footer">
              <Link href="/search" onClick={() => setMobileMenuOpen(false)} className="mobile-menu-search-btn">
                🔍 Search All Products
              </Link>
              <div className="mobile-menu-guarantee">
                🛡️ FREE US SHIPPING OVER $75 • 100% QUALITY GUARANTEED
              </div>
            </div>
          </div>
        </div>
      )}
    </header>
  );
}
