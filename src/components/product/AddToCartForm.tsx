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
  const [casingOption, setCasingOption] = useState<'exact' | 'uppercase'>('exact');
  const [playerNumber, setPlayerNumber] = useState<string>('');
  const [frontWordmarkOption, setFrontWordmarkOption] = useState<'clean' | 'standard' | 'stylized'>('clean');
  const [underTagOption, setUnderTagOption] = useState<'number' | 'wordmark_stylized' | 'wordmark_standard' | 'both_wordmark_number' | 'creed_motto'>('number');
  const [hasSleeveBadges, setHasSleeveBadges] = useState<boolean>(false);
  const [hasHemCreed, setHasHemCreed] = useState<boolean>(false);
  const [addedMessage, setAddedMessage] = useState<boolean>(false);
  const [isSizeGuideOpen, setIsSizeGuideOpen] = useState<boolean>(false);

  // Find exact matching variant
  const currentVariant = product.variants.find(
    v => v.color === selectedColor && v.size === selectedSize
  ) || product.variants[0];

  const isOutOfStock = currentVariant ? !currentVariant.isAvailable : false;
  const isJersey = product.id.startsWith('axiom-jersey');
  const isSweatshirt = product.id === 'axiom-sweatshirt-01';
  const isWorkShirt = product.id === 'krown-work-01';
  const isPersonalizable = isJersey || isSweatshirt || isWorkShirt;

  const [sweatshirtSleeveOption, setSweatshirtSleeveOption] = useState<'left' | 'right' | 'both'>('left');
  const [workShirtBadgePlacement, setWorkShirtBadgePlacement] = useState<'left' | 'right'>('left');

  React.useEffect(() => {
    if (typeof window !== 'undefined' && currentVariant?.image) {
      window.dispatchEvent(new CustomEvent('krown:variant-changed', {
        detail: { color: selectedColor, size: selectedSize, image: currentVariant.image }
      }));
    }
  }, []);

  // Calculate dynamic upcharges
  let addOnsPrice = 0;
  if (isJersey) {
    if (frontWordmarkOption === 'stylized') {
      addOnsPrice += 4.99;
    }
    if (underTagOption === 'wordmark_stylized' || underTagOption === 'wordmark_standard' || underTagOption === 'creed_motto') {
      addOnsPrice += 4.99;
    } else if (underTagOption === 'both_wordmark_number') {
      addOnsPrice += 6.99;
    }
    if (hasSleeveBadges) {
      addOnsPrice += 5.00;
    }
    if (hasHemCreed) {
      addOnsPrice += 3.99;
    }
  } else if (isSweatshirt) {
    if (sweatshirtSleeveOption === 'both') {
      addOnsPrice += 4.99;
    }
  }

  const baseUnitPrice = currentVariant?.price || product.price;
  const finalUnitPrice = baseUnitPrice + addOnsPrice;

  const handleAddToCart = () => {
    if (isOutOfStock) return;

    const trimmedTag = gamertag.trim().slice(0, 16);
    const sanitizedTag = casingOption === 'uppercase' ? trimmedTag.toUpperCase() : trimmedTag;
    const sanitizedNum = playerNumber.trim().replace(/\D/g, '').slice(0, 2);

    const addOnsSummary: string[] = [];
    if (isJersey) {
      if (frontWordmarkOption === 'clean') addOnsSummary.push('Front: Crest Only (Clean)');
      if (frontWordmarkOption === 'standard') addOnsSummary.push('Front: Standard "AXIOM ALLEGIANCE"');
      if (frontWordmarkOption === 'stylized') addOnsSummary.push('Front: Stylized "Aχισм Aℓℓєgιαηcє" (+$4.99)');
      if (underTagOption === 'wordmark_stylized') addOnsSummary.push('Wordmark: Aχισм Aℓℓєgιαηcє (+$4.99)');
      if (underTagOption === 'wordmark_standard') addOnsSummary.push('Wordmark: AXIOM ALLEGIANCE (+$4.99)');
      if (underTagOption === 'both_wordmark_number') addOnsSummary.push(`Aχισм Aℓℓєgιαηcє + #${sanitizedNum || '00'} (+$6.99)`);
      if (underTagOption === 'creed_motto') addOnsSummary.push('Creed Motto Under Tag (+$4.99)');
      if (hasSleeveBadges) addOnsSummary.push('Dual Sleeve Owl Badges (+$5.00)');
      if (hasHemCreed) addOnsSummary.push('Hem Creed Print (+$3.99)');
    } else if (isSweatshirt) {
      if (sweatshirtSleeveOption === 'left') addOnsSummary.push('Gothic Sleeve Print: Left Sleeve (Standard)');
      if (sweatshirtSleeveOption === 'right') addOnsSummary.push('Gothic Sleeve Print: Right Sleeve');
      if (sweatshirtSleeveOption === 'both') addOnsSummary.push('Gothic Sleeve Print: Both Sleeves (+$4.99)');
    } else if (isWorkShirt) {
      addOnsSummary.push(workShirtBadgePlacement === 'left' ? 'Badge: Left Chest (Standard)' : 'Badge: Right Chest');
    }

    const customSnippetParts: string[] = [];
    if (sanitizedTag) customSnippetParts.push(`Tag: ${sanitizedTag}`);
    if (sanitizedNum && (underTagOption === 'number' || underTagOption === 'both_wordmark_number')) {
      customSnippetParts.push(`#${sanitizedNum}`);
    }
    if (addOnsSummary.length > 0) {
      customSnippetParts.push(...addOnsSummary);
    }

    const customSnippet = (isPersonalizable && customSnippetParts.length > 0)
      ? ` [${customSnippetParts.join(' | ')}]` 
      : '';

    addItem({
      productId: product.id,
      name: `${product.name}${customSnippet}`,
      price: finalUnitPrice,
      image: product.images[0] || '',
      variant: {
        color: selectedColor,
        size: selectedSize,
      },
      quantity,
      personalization: isPersonalizable && (sanitizedTag || sanitizedNum || addOnsSummary.length > 0) ? {
        gamertag: sanitizedTag,
        playerNumber: (underTagOption === 'number' || underTagOption === 'both_wordmark_number') ? sanitizedNum : '',
        edition: selectedColor,
        notes: addOnsSummary.join(' | '),
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
              const nextSize = newSizes.length > 0 ? (newSizes.includes(selectedSize) ? selectedSize : newSizes[0]) : selectedSize;
              if (newSizes.length > 0 && !newSizes.includes(selectedSize)) setSelectedSize(newSizes[0]);
              const matchingVariant = product.variants.find(v => v.color === newColor && v.size === nextSize) || product.variants.find(v => v.color === newColor);
              if (typeof window !== 'undefined') {
                window.dispatchEvent(new CustomEvent('krown:color-changed', { detail: { color: newColor, image: matchingVariant?.image } }));
                window.dispatchEvent(new CustomEvent('krown:variant-changed', { detail: { color: newColor, size: nextSize, image: matchingVariant?.image } }));
              }
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
            onChange={(e) => {
              const newSize = e.target.value;
              setSelectedSize(newSize);
              const matchingVariant = product.variants.find(v => v.color === selectedColor && v.size === newSize);
              if (typeof window !== 'undefined') {
                window.dispatchEvent(new CustomEvent('krown:variant-changed', { detail: { color: selectedColor, size: newSize, image: matchingVariant?.image } }));
              }
            }}
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

      {/* Sweatshirt Customizable Sleeve Placement */}
      {isSweatshirt && (
        <div style={{
          background: 'rgba(98, 0, 238, 0.08)',
          border: '1px solid rgba(57, 255, 20, 0.35)',
          borderRadius: '8px',
          padding: '1.1rem',
          marginBottom: '1.25rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.65rem' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: 800, color: '#39FF14', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
              ⚡ Custom Sleeve Lettering Placement
            </span>
            {sweatshirtSleeveOption === 'both' && (
              <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#39FF14', background: 'rgba(57, 255, 20, 0.15)', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>
                +$4.99 Dual Sleeve
              </span>
            )}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.65rem' }}>
            Choose where to place the Gothic two-tone &ldquo;Axiom Allegiance&rdquo; lettering down your sweatshirt arm:
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.5rem' }}>
            <button
              type="button"
              onClick={() => setSweatshirtSleeveOption('left')}
              style={{
                padding: '0.55rem 0.4rem',
                fontSize: '0.75rem',
                fontWeight: sweatshirtSleeveOption === 'left' ? 700 : 500,
                background: sweatshirtSleeveOption === 'left' ? 'rgba(57, 255, 20, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                border: sweatshirtSleeveOption === 'left' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.15)',
                color: sweatshirtSleeveOption === 'left' ? '#39FF14' : 'var(--text-muted)',
                borderRadius: '4px',
                cursor: 'pointer',
                textAlign: 'center',
              }}
            >
              Left Sleeve (Std)
            </button>
            <button
              type="button"
              onClick={() => setSweatshirtSleeveOption('right')}
              style={{
                padding: '0.55rem 0.4rem',
                fontSize: '0.75rem',
                fontWeight: sweatshirtSleeveOption === 'right' ? 700 : 500,
                background: sweatshirtSleeveOption === 'right' ? 'rgba(57, 255, 20, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                border: sweatshirtSleeveOption === 'right' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.15)',
                color: sweatshirtSleeveOption === 'right' ? '#39FF14' : 'var(--text-muted)',
                borderRadius: '4px',
                cursor: 'pointer',
                textAlign: 'center',
              }}
            >
              Right Sleeve
            </button>
            <button
              type="button"
              onClick={() => setSweatshirtSleeveOption('both')}
              style={{
                padding: '0.55rem 0.4rem',
                fontSize: '0.75rem',
                fontWeight: sweatshirtSleeveOption === 'both' ? 700 : 500,
                background: sweatshirtSleeveOption === 'both' ? 'rgba(57, 255, 20, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                border: sweatshirtSleeveOption === 'both' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.15)',
                color: sweatshirtSleeveOption === 'both' ? '#39FF14' : 'var(--text-muted)',
                borderRadius: '4px',
                cursor: 'pointer',
                textAlign: 'center',
              }}
            >
              Both Sleeves (+$4.99)
            </button>
          </div>
        </div>
      )}

      {isJersey && (
        <div style={{
          background: 'rgba(98, 0, 238, 0.08)',
          border: '1px solid rgba(57, 255, 20, 0.35)',
          borderRadius: '8px',
          padding: '1.1rem',
          marginBottom: '1.25rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.65rem' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: 800, color: '#39FF14', letterSpacing: '0.08em', textTransform: 'uppercase' }}>
              ⚡ Pro Player Customization & Add-Ons
            </span>
            {addOnsPrice > 0 && (
              <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#39FF14', background: 'rgba(57, 255, 20, 0.15)', padding: '0.2rem 0.5rem', borderRadius: '4px' }}>
                +${addOnsPrice.toFixed(2)} Add-Ons Selected
              </span>
            )}
          </div>

          {/* Front Chest Crest & Wordmark Styling */}
          <div style={{ marginBottom: '0.85rem' }}>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.35rem' }}>
              Front Chest Crest &amp; Wordmark Styling:
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '0.4rem' }}>
              <button
                type="button"
                onClick={() => setFrontWordmarkOption('clean')}
                style={{
                  padding: '0.45rem 0.65rem',
                  fontSize: '0.78rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  fontWeight: frontWordmarkOption === 'clean' ? 700 : 400,
                  background: frontWordmarkOption === 'clean' ? 'rgba(57, 255, 20, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                  border: frontWordmarkOption === 'clean' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.12)',
                  color: frontWordmarkOption === 'clean' ? '#39FF14' : 'var(--text-main)',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  textAlign: 'left'
                }}
              >
                <span>Crest Only (Clean Pro Look)</span>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Included</span>
              </button>
              <button
                type="button"
                onClick={() => setFrontWordmarkOption('standard')}
                style={{
                  padding: '0.45rem 0.65rem',
                  fontSize: '0.78rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  fontWeight: frontWordmarkOption === 'standard' ? 700 : 400,
                  background: frontWordmarkOption === 'standard' ? 'rgba(57, 255, 20, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                  border: frontWordmarkOption === 'standard' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.12)',
                  color: frontWordmarkOption === 'standard' ? '#39FF14' : 'var(--text-main)',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  textAlign: 'left'
                }}
              >
                <span>Standard Wordmark: &ldquo;AXIOM ALLEGIANCE&rdquo; (Under Crest)</span>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Included</span>
              </button>
              <button
                type="button"
                onClick={() => setFrontWordmarkOption('stylized')}
                style={{
                  padding: '0.45rem 0.65rem',
                  fontSize: '0.78rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  fontWeight: frontWordmarkOption === 'stylized' ? 700 : 400,
                  background: frontWordmarkOption === 'stylized' ? 'rgba(57, 255, 20, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                  border: frontWordmarkOption === 'stylized' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.12)',
                  color: frontWordmarkOption === 'stylized' ? '#39FF14' : 'var(--text-main)',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  textAlign: 'left'
                }}
              >
                <span>Stylized Gothic: &ldquo;Aχισм Aℓℓєgιαηcє&rdquo; (Under Crest)</span>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#39FF14' }}>+$4.99</span>
              </button>
            </div>
          </div>

          {/* Casing Style Option */}
          <div style={{ marginBottom: '0.75rem' }}>
            <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.35rem' }}>
              Gamertag Casing Style:
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
              <button
                type="button"
                onClick={() => setCasingOption('exact')}
                style={{
                  padding: '0.45rem 0.5rem',
                  fontSize: '0.75rem',
                  fontWeight: casingOption === 'exact' ? 700 : 500,
                  background: casingOption === 'exact' ? 'rgba(57, 255, 20, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                  border: casingOption === 'exact' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.15)',
                  color: casingOption === 'exact' ? '#39FF14' : 'var(--text-muted)',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                  textAlign: 'center',
                }}
              >
                Exact Case (e.g. &ldquo;KrowN&rdquo;)
              </button>
              <button
                type="button"
                onClick={() => {
                  setCasingOption('uppercase');
                  if (gamertag) setGamertag(gamertag.toUpperCase());
                }}
                style={{
                  padding: '0.45rem 0.5rem',
                  fontSize: '0.75rem',
                  fontWeight: casingOption === 'uppercase' ? 700 : 500,
                  background: casingOption === 'uppercase' ? 'rgba(57, 255, 20, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                  border: casingOption === 'uppercase' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.15)',
                  color: casingOption === 'uppercase' ? '#39FF14' : 'var(--text-muted)',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                  textAlign: 'center',
                }}
              >
                ALL CAPS (e.g. &ldquo;KROWN&rdquo;)
              </button>
            </div>
          </div>

          {/* Gamertag Input */}
          <div className="form-group" style={{ marginBottom: '0.85rem' }}>
            <label htmlFor="gamertag-input" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
              Gamertag / Player Name (Max 16 Chars):
            </label>
            <input
              type="text"
              id="gamertag-input"
              value={gamertag}
              onChange={(e) => {
                const val = e.target.value.slice(0, 16);
                setGamertag(casingOption === 'uppercase' ? val.toUpperCase() : val);
              }}
              placeholder={casingOption === 'exact' ? 'e.g. KrowN' : 'e.g. KROWN'}
              className="form-input"
              style={{
                textTransform: casingOption === 'uppercase' ? 'uppercase' : 'none',
                letterSpacing: casingOption === 'uppercase' ? '0.08em' : '0.04em'
              }}
              autoComplete="off"
              spellCheck={false}
            />
          </div>

          {/* Under Gamertag Placement Options (Only for Jerseys) */}
          {isJersey && (
            <div style={{ marginBottom: '0.9rem' }}>
              <label style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginBottom: '0.4rem' }}>
                Back Placement Under Gamertag:
              </label>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '0.4rem' }}>
                <button
                  type="button"
                  onClick={() => setUnderTagOption('number')}
                  style={{
                    padding: '0.45rem 0.65rem',
                    fontSize: '0.78rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    fontWeight: underTagOption === 'number' ? 700 : 400,
                    background: underTagOption === 'number' ? 'rgba(57, 255, 20, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                    border: underTagOption === 'number' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.12)',
                    color: underTagOption === 'number' ? '#39FF14' : 'var(--text-main)',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    textAlign: 'left'
                  }}
                >
                  <span>Squad Number Only (e.g. #07)</span>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Included</span>
                </button>

                <button
                  type="button"
                  onClick={() => setUnderTagOption('wordmark_stylized')}
                  style={{
                    padding: '0.45rem 0.65rem',
                    fontSize: '0.78rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    fontWeight: underTagOption === 'wordmark_stylized' ? 700 : 400,
                    background: underTagOption === 'wordmark_stylized' ? 'rgba(57, 255, 20, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                    border: underTagOption === 'wordmark_stylized' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.12)',
                    color: underTagOption === 'wordmark_stylized' ? '#39FF14' : 'var(--text-main)',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    textAlign: 'left'
                  }}
                >
                  <span>Stylized Font: &ldquo;Aχισм Aℓℓєgιαηcє&rdquo;</span>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#39FF14' }}>+$4.99</span>
                </button>

                <button
                  type="button"
                  onClick={() => setUnderTagOption('wordmark_standard')}
                  style={{
                    padding: '0.45rem 0.65rem',
                    fontSize: '0.78rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    fontWeight: underTagOption === 'wordmark_standard' ? 700 : 400,
                    background: underTagOption === 'wordmark_standard' ? 'rgba(57, 255, 20, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                    border: underTagOption === 'wordmark_standard' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.12)',
                    color: underTagOption === 'wordmark_standard' ? '#39FF14' : 'var(--text-main)',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    textAlign: 'left'
                  }}
                >
                  <span>Athletic Bold: &ldquo;AXIOM ALLEGIANCE&rdquo;</span>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#39FF14' }}>+$4.99</span>
                </button>

                <button
                  type="button"
                  onClick={() => setUnderTagOption('both_wordmark_number')}
                  style={{
                    padding: '0.45rem 0.65rem',
                    fontSize: '0.78rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    fontWeight: underTagOption === 'both_wordmark_number' ? 700 : 400,
                    background: underTagOption === 'both_wordmark_number' ? 'rgba(57, 255, 20, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                    border: underTagOption === 'both_wordmark_number' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.12)',
                    color: underTagOption === 'both_wordmark_number' ? '#39FF14' : 'var(--text-main)',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    textAlign: 'left'
                  }}
                >
                  <span>Stylized &ldquo;Aχισм Aℓℓєgιαηcє&rdquo; + Squad Number</span>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#39FF14' }}>+$6.99</span>
                </button>

                <button
                  type="button"
                  onClick={() => setUnderTagOption('creed_motto')}
                  style={{
                    padding: '0.45rem 0.65rem',
                    fontSize: '0.78rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    fontWeight: underTagOption === 'creed_motto' ? 700 : 400,
                    background: underTagOption === 'creed_motto' ? 'rgba(57, 255, 20, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                    border: underTagOption === 'creed_motto' ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.12)',
                    color: underTagOption === 'creed_motto' ? '#39FF14' : 'var(--text-main)',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    textAlign: 'left'
                  }}
                >
                  <span>Official Team Creed Motto (Under Tag)</span>
                  <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#39FF14' }}>+$4.99</span>
                </button>
              </div>
            </div>
          )}

          {/* Squad Number input (shown when number is chosen) */}
          {(underTagOption === 'number' || underTagOption === 'both_wordmark_number' || !isJersey) && (
            <div className="form-group" style={{ marginBottom: '0.85rem' }}>
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
          )}

          {/* Pro Team Add-Ons (Sleeve Badges & Hem Creed) */}
          {isJersey && (
            <div style={{ marginTop: '0.85rem', paddingTop: '0.85rem', borderTop: '1px solid rgba(255, 255, 255, 0.08)' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
                Pro Jersey Add-On Upgrades:
              </div>

              {/* Sleeve Crests */}
              <label style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '0.55rem 0.65rem',
                borderRadius: '4px',
                background: hasSleeveBadges ? 'rgba(57, 255, 20, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                border: hasSleeveBadges ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.1)',
                cursor: 'pointer',
                marginBottom: '0.45rem',
                fontSize: '0.78rem'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.55rem' }}>
                  <input
                    type="checkbox"
                    checked={hasSleeveBadges}
                    onChange={(e) => setHasSleeveBadges(e.target.checked)}
                    style={{ accentColor: '#39FF14', width: '15px', height: '15px' }}
                  />
                  <span>Dual Sleeve Axiom Owl Crest Badges</span>
                </div>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#39FF14' }}>+$5.00</span>
              </label>

              {/* Hem Motto Print */}
              <label style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '0.55rem 0.65rem',
                borderRadius: '4px',
                background: hasHemCreed ? 'rgba(57, 255, 20, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                border: hasHemCreed ? '1px solid #39FF14' : '1px solid rgba(255, 255, 255, 0.1)',
                cursor: 'pointer',
                fontSize: '0.78rem'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.55rem' }}>
                  <input
                    type="checkbox"
                    checked={hasHemCreed}
                    onChange={(e) => setHasHemCreed(e.target.checked)}
                    style={{ accentColor: '#39FF14', width: '15px', height: '15px' }}
                  />
                  <div>
                    <div>Lower Hem Team Creed Motto Print</div>
                    <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>
                      &ldquo;YOU CANNOT BE TRULY HUMBLE...&rdquo;
                    </div>
                  </div>
                </div>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#39FF14' }}>+$3.99</span>
              </label>
            </div>
          )}

          {/* Live Back-Print Preview */}
          {(gamertag.trim() || playerNumber.trim() || hasSleeveBadges || hasHemCreed || underTagOption !== 'number') && (
            <div style={{
              marginTop: '0.95rem',
              padding: '0.65rem 0.85rem',
              background: 'rgba(0, 0, 0, 0.65)',
              border: '1px solid rgba(57, 255, 20, 0.4)',
              borderRadius: '6px',
              fontSize: '0.78rem'
            }}>
              <div style={{ color: '#39FF14', fontWeight: 700, fontSize: '0.72rem', letterSpacing: '0.08em', marginBottom: '0.4rem', textTransform: 'uppercase' }}>
                ⚡ Live Back-Print & Jersey Preview
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Player Gamertag:</span>
                  <span style={{ fontWeight: 800, color: 'var(--text-main)', fontFamily: 'monospace' }}>
                    {casingOption === 'uppercase' ? (gamertag.trim().toUpperCase() || 'YOUR TAG') : (gamertag.trim() || 'YOUR TAG')}
                  </span>
                </div>

                {isJersey && (
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Under Gamertag:</span>
                    <span style={{ fontWeight: 700, color: '#39FF14' }}>
                      {underTagOption === 'wordmark_stylized' && 'Aχισм Aℓℓєgιαηcє'}
                      {underTagOption === 'wordmark_standard' && 'AXIOM ALLEGIANCE'}
                      {underTagOption === 'both_wordmark_number' && `Aχισм Aℓℓєgιαηcє #${playerNumber.trim() || '00'}`}
                      {underTagOption === 'creed_motto' && '“YOU CANNOT BE TRULY HUMBLE...”'}
                      {underTagOption === 'number' && `#${playerNumber.trim() || '00'}`}
                    </span>
                  </div>
                )}

                {hasSleeveBadges && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', color: '#39FF14', fontSize: '0.72rem' }}>
                    <span>Sleeves:</span>
                    <span>✓ Left & Right Axiom Owl Crest Badges</span>
                  </div>
                )}

                {hasHemCreed && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', color: '#39FF14', fontSize: '0.72rem' }}>
                    <span>Lower Hem:</span>
                    <span>✓ Full Team Creed Inscription</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Work Shirt Chest Badge Placement Option */}
      {isWorkShirt && (
        <div className="form-group" style={{ marginBottom: '1.25rem', background: 'rgba(212, 175, 55, 0.05)', padding: '0.85rem', borderRadius: '6px', border: '1px solid rgba(212, 175, 55, 0.2)' }}>
          <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--accent-gold)', display: 'block', marginBottom: '0.45rem' }}>
            KrowN Construction Chest Badge Placement:
          </label>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem' }}>
            <button
              type="button"
              onClick={() => setWorkShirtBadgePlacement('left')}
              style={{
                padding: '0.5rem',
                fontSize: '0.78rem',
                fontWeight: workShirtBadgePlacement === 'left' ? 700 : 400,
                background: workShirtBadgePlacement === 'left' ? 'rgba(212, 175, 55, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                border: workShirtBadgePlacement === 'left' ? '1px solid var(--accent-gold)' : '1px solid rgba(255, 255, 255, 0.1)',
                color: workShirtBadgePlacement === 'left' ? 'var(--accent-gold)' : 'var(--text-muted)',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Left Chest (Standard)
            </button>
            <button
              type="button"
              onClick={() => setWorkShirtBadgePlacement('right')}
              style={{
                padding: '0.5rem',
                fontSize: '0.78rem',
                fontWeight: workShirtBadgePlacement === 'right' ? 700 : 400,
                background: workShirtBadgePlacement === 'right' ? 'rgba(212, 175, 55, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                border: workShirtBadgePlacement === 'right' ? '1px solid var(--accent-gold)' : '1px solid rgba(255, 255, 255, 0.1)',
                color: workShirtBadgePlacement === 'right' ? 'var(--accent-gold)' : 'var(--text-muted)',
                borderRadius: '4px',
                cursor: 'pointer',
              }}
            >
              Right Chest
            </button>
          </div>
          <p style={{ margin: '0.4rem 0 0 0', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
            Includes bold &ldquo;BUILT TO REIGN&rdquo; back statement piece &amp; &ldquo;KrowN Construction&rdquo; sleeve lettering.
          </p>
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
          {isOutOfStock ? 'Out of Stock' : addedMessage ? '✓ Added to Cart!' : `Add to Cart / Customize — $${(finalUnitPrice * quantity).toFixed(2)}`}
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
              <p className="text-muted" style={{ marginBottom: '1rem', fontSize: '0.85rem' }}>
                Official specifications for {product.name}.
              </p>

              {/* Headwear Guide */}
              {(product.id.includes('hat') || product.id.includes('beanie') || product.id.includes('snapback') || product.id.includes('112')) && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Headwear Specifications</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Style</th><th style={{ padding: '0.5rem' }}>Profile</th><th style={{ padding: '0.5rem' }}>Circumference</th><th style={{ padding: '0.5rem' }}>Closure</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>Richardson 112 Snapback</td><td style={{ padding: '0.5rem' }}>Mid-Pro Structured</td><td style={{ padding: '0.5rem' }}>7&quot; – 7 3/4&quot; (21.5&quot;–24.5&quot;)</td><td style={{ padding: '0.5rem' }}>7-Hole Snapback</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>Washed Chino Dad Hat</td><td style={{ padding: '0.5rem' }}>Low-Pro Unstructured</td><td style={{ padding: '0.5rem' }}>6 7/8&quot; – 7 5/8&quot;</td><td style={{ padding: '0.5rem' }}>Brass Slide Buckle</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>Tradesman Ribbed Beanie</td><td style={{ padding: '0.5rem' }}>Heavy Cuffed Knit</td><td style={{ padding: '0.5rem' }}>Stretch-Fit (One Size)</td><td style={{ padding: '0.5rem' }}>Cuffed Acrylic</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Drinkware Guide */}
              {(product.id.includes('shaker') || product.id.includes('mug') || product.id.includes('tumbler')) && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Drinkware &amp; Capacity Specifications</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Vessel</th><th style={{ padding: '0.5rem' }}>Capacity</th><th style={{ padding: '0.5rem' }}>Height x Base</th><th style={{ padding: '0.5rem' }}>Features</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>Standard Tritan Shaker</td><td style={{ padding: '0.5rem' }}>24 oz / 700 ml</td><td style={{ padding: '0.5rem' }}>8.8&quot; x 3.1&quot;</td><td style={{ padding: '0.5rem' }}>Shatterproof • Whisk Ball</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>Pro Insulated Steel Shaker</td><td style={{ padding: '0.5rem' }}>26 oz / 750 ml</td><td style={{ padding: '0.5rem' }}>9.2&quot; x 3.2&quot;</td><td style={{ padding: '0.5rem' }}>Double-Wall Vacuum • Lock Lid</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>Ceramic Gamer Mug</td><td style={{ padding: '0.5rem' }}>15 oz / 445 ml</td><td style={{ padding: '0.5rem' }}>4.7&quot; x 3.3&quot;</td><td style={{ padding: '0.5rem' }}>Two-Tone Glaze • Microwave Safe</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Work Shirt Guide */}
              {isWorkShirt && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>KrowN Construction Work Shirt Measurements</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Chest</th><th style={{ padding: '0.5rem' }}>Body Length</th><th style={{ padding: '0.5rem' }}>Sleeve Length</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>38&quot; – 40&quot;</td><td style={{ padding: '0.5rem' }}>30.0&quot;</td><td style={{ padding: '0.5rem' }}>33.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>42&quot; – 44&quot;</td><td style={{ padding: '0.5rem' }}>31.0&quot;</td><td style={{ padding: '0.5rem' }}>34.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>46&quot; – 48&quot;</td><td style={{ padding: '0.5rem' }}>32.0&quot;</td><td style={{ padding: '0.5rem' }}>35.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>50&quot; – 52&quot;</td><td style={{ padding: '0.5rem' }}>33.0&quot;</td><td style={{ padding: '0.5rem' }}>36.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>54&quot; – 56&quot;</td><td style={{ padding: '0.5rem' }}>34.0&quot;</td><td style={{ padding: '0.5rem' }}>37.5&quot;</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>3XL</td><td style={{ padding: '0.5rem' }}>58&quot; – 60&quot;</td><td style={{ padding: '0.5rem' }}>35.0&quot;</td><td style={{ padding: '0.5rem' }}>38.5&quot;</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Jersey Guide */}
              {isJersey && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Pro Esports Cut-and-Sew Jersey</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Chest Width</th><th style={{ padding: '0.5rem' }}>Body Length</th><th style={{ padding: '0.5rem' }}>Sleeve (Raglan)</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>19.5&quot;</td><td style={{ padding: '0.5rem' }}>27.5&quot;</td><td style={{ padding: '0.5rem' }}>14.0&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>20.5&quot;</td><td style={{ padding: '0.5rem' }}>28.5&quot;</td><td style={{ padding: '0.5rem' }}>14.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>21.5&quot;</td><td style={{ padding: '0.5rem' }}>29.5&quot;</td><td style={{ padding: '0.5rem' }}>15.0&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>22.5&quot;</td><td style={{ padding: '0.5rem' }}>30.5&quot;</td><td style={{ padding: '0.5rem' }}>15.5&quot;</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>23.5&quot;</td><td style={{ padding: '0.5rem' }}>31.5&quot;</td><td style={{ padding: '0.5rem' }}>16.0&quot;</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Compression Arm Sleeve */}
              {product.id.includes('sleeve') && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Pro Compression Sleeve Sizing</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Bicep Girth</th><th style={{ padding: '0.5rem' }}>Wrist Girth</th><th style={{ padding: '0.5rem' }}>Total Length</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S/M</td><td style={{ padding: '0.5rem' }}>10.0&quot; – 12.5&quot;</td><td style={{ padding: '0.5rem' }}>6.0&quot; – 7.5&quot;</td><td style={{ padding: '0.5rem' }}>16.5&quot;</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>L/XL</td><td style={{ padding: '0.5rem' }}>12.5&quot; – 15.5&quot;</td><td style={{ padding: '0.5rem' }}>7.5&quot; – 9.0&quot;</td><td style={{ padding: '0.5rem' }}>17.5&quot;</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Bottoms: Shorts & Joggers */}
              {(product.id.includes('short') || product.id.includes('jogger') || product.id.includes('sweatpant')) && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Bottoms (Shorts &amp; Joggers) Sizing</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Waist (Inches)</th><th style={{ padding: '0.5rem' }}>Inseam (Joggers)</th><th style={{ padding: '0.5rem' }}>Inseam (Shorts)</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>28&quot; – 30&quot;</td><td style={{ padding: '0.5rem' }}>30.0&quot;</td><td style={{ padding: '0.5rem' }}>6.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>31&quot; – 33&quot;</td><td style={{ padding: '0.5rem' }}>30.5&quot;</td><td style={{ padding: '0.5rem' }}>6.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>34&quot; – 36&quot;</td><td style={{ padding: '0.5rem' }}>31.0&quot;</td><td style={{ padding: '0.5rem' }}>7.0&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>37&quot; – 40&quot;</td><td style={{ padding: '0.5rem' }}>31.5&quot;</td><td style={{ padding: '0.5rem' }}>7.0&quot;</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>41&quot; – 44&quot;</td><td style={{ padding: '0.5rem' }}>32.0&quot;</td><td style={{ padding: '0.5rem' }}>7.5&quot;</td></tr>
                    </tbody>
                  </table>
                </div>
              )}

              {/* Hoodies & Tops Fallback */}
              {!isWorkShirt && !isJersey && !product.id.includes('hat') && !product.id.includes('beanie') && !product.id.includes('shaker') && !product.id.includes('mug') && !product.id.includes('sleeve') && !product.id.includes('short') && !product.id.includes('jogger') && !product.id.includes('sweatpant') && (
                <div>
                  <h3 style={{ marginTop: '0.5rem', marginBottom: '0.5rem', fontSize: '1rem', color: 'var(--accent-gold)' }}>Heavyweight Hoodies &amp; Streetwear Tops</h3>
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
                    <thead><tr style={{ borderBottom: '1px solid var(--border)' }}><th style={{ padding: '0.5rem' }}>Size</th><th style={{ padding: '0.5rem' }}>Chest</th><th style={{ padding: '0.5rem' }}>Length</th><th style={{ padding: '0.5rem' }}>Sleeve</th></tr></thead>
                    <tbody>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>S</td><td style={{ padding: '0.5rem' }}>22.0&quot;</td><td style={{ padding: '0.5rem' }}>28.0&quot;</td><td style={{ padding: '0.5rem' }}>34.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>M</td><td style={{ padding: '0.5rem' }}>23.0&quot;</td><td style={{ padding: '0.5rem' }}>29.0&quot;</td><td style={{ padding: '0.5rem' }}>35.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>L</td><td style={{ padding: '0.5rem' }}>24.0&quot;</td><td style={{ padding: '0.5rem' }}>30.0&quot;</td><td style={{ padding: '0.5rem' }}>36.5&quot;</td></tr>
                      <tr style={{ borderBottom: '1px solid var(--border)' }}><td style={{ padding: '0.5rem' }}>XL</td><td style={{ padding: '0.5rem' }}>25.0&quot;</td><td style={{ padding: '0.5rem' }}>31.0&quot;</td><td style={{ padding: '0.5rem' }}>37.5&quot;</td></tr>
                      <tr><td style={{ padding: '0.5rem' }}>2XL</td><td style={{ padding: '0.5rem' }}>26.0&quot;</td><td style={{ padding: '0.5rem' }}>32.0&quot;</td><td style={{ padding: '0.5rem' }}>38.5&quot;</td></tr>
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </form>
  );
}
