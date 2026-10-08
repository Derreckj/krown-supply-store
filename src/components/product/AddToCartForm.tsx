"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { useCart } from '@/context/CartContext';
import { CatalogProduct } from '@/services/printify';

export default function AddToCartForm({ product }: { product: CatalogProduct }) {
  const { addItem } = useCart();
  
  // Extract unique colors and sizes
  const colors = Array.from(new Set(product.variants.map(v => v.color)));
  const [selectedColor, setSelectedColor] = useState<string>(colors[0] || 'Default');

  // Available sizes for currently selected color
  const availableVariantsForColor = product.variants.filter(v => v.color === selectedColor);
  const sizes = Array.from(new Set(availableVariantsForColor.map(v => v.size)));
  const [selectedSize, setSelectedSize] = useState<string>(sizes[0] || 'One Size');
  const [quantity, setQuantity] = useState<number>(1);
  const [gamertag, setGamertag] = useState<string>('');
  const [playerNumber, setPlayerNumber] = useState<string>('');
  const [addedMessage, setAddedMessage] = useState<boolean>(false);
  const [isSizeGuideOpen, setIsSizeGuideOpen] = useState<boolean>(false);

  // Find exact matching variant
  const currentVariant = product.variants.find(
    v => v.color === selectedColor && v.size === selectedSize
  ) || product.variants[0];

  const isOutOfStock = currentVariant ? !currentVariant.isAvailable : false;
  const isPersonalizable = selectedColor.toLowerCase().includes('custom') || product.id.startsWith('axiom-jersey') || product.id === 'custom-krown-works-hat';

  const handleAddToCart = () => {
    if (isOutOfStock) return;

    const sanitizedTag = gamertag.trim().toUpperCase().slice(0, 16);
    const sanitizedNum = playerNumber.trim().replace(/\D/g, '').slice(0, 2);

    const customSnippet = isPersonalizable && sanitizedTag 
      ? ` [Tag: ${sanitizedTag}${sanitizedNum ? ` #${sanitizedNum}` : ''}]` 
      : '';

    addItem({
      productId: product.id,
      name: `${product.name}${customSnippet}`,
      price: currentVariant?.price || product.price,
      image: product.images[0] || '',
      variant: {
        color: selectedColor,
        size: selectedSize,
      },
      quantity,
      personalization: isPersonalizable && (sanitizedTag || sanitizedNum) ? {
        gamertag: sanitizedTag,
        playerNumber: sanitizedNum,
        edition: selectedColor,
      } : undefined,
    });

    setAddedMessage(true);
    setTimeout(() => setAddedMessage(false), 2500);
  };

  return (
    <form className="product-form" onSubmit={(e) => { e.preventDefault(); handleAddToCart(); }}>
      {colors.length > 0 && (
        <div className="form-group">
          <label htmlFor="color-select">Colorway</label>
          <select 
            id="color-select" 
            className="form-select"
            value={selectedColor}
            onChange={(e) => {
              const newColor = e.target.value;
              setSelectedColor(newColor);
              const newSizes = product.variants.filter(v => v.color === newColor).map(v => v.size);
              if (newSizes.length > 0) setSelectedSize(newSizes[0]);
            }}
          >
            {colors.map((c, i) => (
              <option key={i} value={c}>{c}</option>
            ))}
          </select>
        </div>
      )}

      {sizes.length > 0 && (
        <div className="form-group">
          <div className="label-row">
            <label htmlFor="size-select">Size</label>
            <button type="button" className="size-guide-link" onClick={() => setIsSizeGuideOpen(true)} style={{ background: 'none', border: 'none', color: 'var(--text-muted)', textDecoration: 'underline', cursor: 'pointer', padding: 0, fontSize: '0.8rem' }}>Size Guide</button>
          </div>
          <select 
            id="size-select" 
            className="form-select"
            value={selectedSize}
            onChange={(e) => setSelectedSize(e.target.value)}
          >
            {sizes.map((s, i) => {
              const v = product.variants.find(item => item.color === selectedColor && item.size === s);
              const isAvailable = v ? v.isAvailable : true;
              return (
                <option key={i} value={s} disabled={!isAvailable}>
                  {s} {!isAvailable ? '(Out of Stock)' : ''}
                </option>
              );
            })}
          </select>
        </div>
      )}

      {isPersonalizable && (
        <div style={{
          background: 'rgba(98, 0, 238, 0.08)',
          border: '1px solid rgba(57, 255, 20, 0.35)',
          borderRadius: '8px',
          padding: '1rem',
          marginBottom: '1.25rem'
        }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 800, color: '#39FF14', letterSpacing: '0.08em', marginBottom: '0.65rem', textTransform: 'uppercase' }}>
            ⚡ Pro Player Gamertag Personalization
          </div>
          <div className="form-group" style={{ marginBottom: '0.75rem' }}>
            <label htmlFor="gamertag-input" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Gamertag / Player Name (Max 16 Chars, All Caps):
            </label>
            <input
              type="text"
              id="gamertag-input"
              value={gamertag}
              onChange={(e) => setGamertag(e.target.value.toUpperCase().slice(0, 16))}
              placeholder="e.g. VIPER"
              className="form-input"
              style={{ textTransform: 'uppercase', letterSpacing: '0.08em' }}
            />
          </div>
          <div className="form-group" style={{ marginBottom: 0 }}>
            <label htmlFor="number-input" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Squad Number (00-99, Optional):
            </label>
            <input
              type="text"
              id="number-input"
              value={playerNumber}
              onChange={(e) => setPlayerNumber(e.target.value.replace(/\D/g, '').slice(0, 2))}
              placeholder="e.g. 07"
              className="form-input"
            />
          </div>
        </div>
      )}

      <div className="form-group">
        <label htmlFor="quantity">Quantity</label>
        <input 
          type="number" 
          id="quantity" 
          value={quantity} 
          min={1} 
          max={10} 
          className="form-input"
          onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
        />
      </div>

      <div className="sticky-mobile-cart-bar">
        <button 
          type="submit" 
          className="btn-primary add-to-cart-btn"
          disabled={isOutOfStock}
          style={{ width: '100%', opacity: isOutOfStock ? 0.5 : 1, cursor: isOutOfStock ? 'not-allowed' : 'pointer' }}
        >
          {isOutOfStock ? 'Out of Stock' : addedMessage ? '✓ Added to Cart!' : 'Add to Cart / Customize'}
        </button>
      </div>

      {addedMessage && (
        <div style={{ marginTop: '0.75rem', textAlign: 'center' }}>
          <Link href="/cart" style={{ color: 'var(--accent-gold)', fontSize: '0.875rem', textDecoration: 'underline' }}>
            View Cart & Checkout &rarr;
          </Link>
        </div>
      )}

      {/* Size Guide Modal */}
      {isSizeGuideOpen && (
        <div className="size-guide-overlay" onClick={() => setIsSizeGuideOpen(false)}>
          <div className="size-guide-modal" onClick={e => e.stopPropagation()}>
            <div className="size-guide-header">
              <h2 style={{ margin: 0, fontSize: '1.2rem', color: 'var(--foreground)' }}>Measurement Guide</h2>
              <button className="size-guide-close" onClick={() => setIsSizeGuideOpen(false)} style={{ background: 'none', border: 'none', fontSize: '1.5rem', color: 'var(--text-muted)', cursor: 'pointer' }}>&times;</button>
            </div>
            <div className="size-guide-content" style={{ marginTop: '1rem', color: 'var(--foreground)' }}>
              <p className="text-muted" style={{ marginBottom: '1rem', fontSize: '0.85rem' }}>All measurements are in inches. Tolerance +/- 0.5&quot;.</p>
              
              <h3 style={{ marginTop: '1rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Pro Esports Jersey</h3>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', marginBottom: '1rem', fontSize: '0.9rem' }}>
                <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Chest</th><th style={{ padding: '0.5rem' }}>Length</th></tr></thead>
                <tbody>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>19.5&quot;</td><td style={{ padding: '0.5rem' }}>27.5&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>20.5&quot;</td><td style={{ padding: '0.5rem' }}>28.5&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>21.5&quot;</td><td style={{ padding: '0.5rem' }}>29.5&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>22.5&quot;</td><td style={{ padding: '0.5rem' }}>30.5&quot;</td></tr>
                  <tr><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>23.5&quot;</td><td style={{ padding: '0.5rem' }}>31.5&quot;</td></tr>
                </tbody>
              </table>

              <h3 style={{ marginTop: '1.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Heavyweight Hoodies & Tees</h3>
              <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
                <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Chest</th><th style={{ padding: '0.5rem' }}>Length</th></tr></thead>
                <tbody>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>22.0&quot;</td><td style={{ padding: '0.5rem' }}>28.0&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>23.0&quot;</td><td style={{ padding: '0.5rem' }}>29.0&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>24.0&quot;</td><td style={{ padding: '0.5rem' }}>30.0&quot;</td></tr>
                  <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>25.0&quot;</td><td style={{ padding: '0.5rem' }}>31.0&quot;</td></tr>
                  <tr><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>26.0&quot;</td><td style={{ padding: '0.5rem' }}>32.0&quot;</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </form>
  );
}
