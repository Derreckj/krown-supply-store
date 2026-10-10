"use client";

import React, { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { useCart } from '@/context/CartContext';
import './CustomCrew.css';

interface TierOption {
  id: string;
  name: string;
  qty: number;
  priceEach: number;
  total: number;
  savings?: string;
  badge?: string;
}

const TIERS: TierOption[] = [
  { id: 'single', name: 'Sample / Single', qty: 1, priceEach: 29.99, total: 29.99 },
  { id: 'crew-6', name: 'Crew Pack', qty: 6, priceEach: 27.0, total: 162.0, savings: 'Save 10%' },
  { id: 'company-12', name: 'Company Pack', qty: 12, priceEach: 25.5, total: 306.0, savings: 'Save 15%', badge: 'MOST POPULAR' },
  { id: 'fleet-24', name: 'Fleet Pack', qty: 24, priceEach: 24.0, total: 576.0, savings: 'Save 20%', badge: 'BEST VALUE' },
];

interface PatchStyle {
  id: string;
  name: string;
  desc: string;
  bg: string;
  color: string;
  stitch: string;
}

const PATCH_STYLES: PatchStyle[] = [
  { 
    id: 'caramel', 
    name: 'Caramel Cowhide', 
    desc: 'Warm rustic saddle leather with dark laser-engraved burn', 
    bg: 'linear-gradient(135deg, #b87333 0%, #c68a4c 50%, #9e5b22 100%)',
    color: '#361c0c',
    stitch: '#e0c29f',
  },
  { 
    id: 'black', 
    name: 'Obsidian Leatherette', 
    desc: 'Matte black textured leather with metallic gold laser burn', 
    bg: 'linear-gradient(135deg, #18191c 0%, #25272c 50%, #151618 100%)',
    color: '#e2b34e',
    stitch: '#50535b',
  },
  { 
    id: 'raw-tan', 
    name: 'Raw Natural Tan', 
    desc: 'Light natural saddle tan with deep walnut burn engraving', 
    bg: 'linear-gradient(135deg, #d2b48c 0%, #dfcbb5 50%, #c4a47c 100%)',
    color: '#2a1a0f',
    stitch: '#f4ebd9',
  },
];

interface PatchShape {
  id: string;
  name: string;
  clipPath?: string;
  borderRadius?: string;
  aspectRatio: string;
}

const PATCH_SHAPES: PatchShape[] = [
  { 
    id: 'hexagon', 
    name: 'Hexagon', 
    clipPath: 'polygon(50% 0%, 98% 25%, 98% 75%, 50% 100%, 2% 75%, 2% 25%)',
    aspectRatio: '1.05/1'
  },
  { 
    id: 'rectangle', 
    name: 'Rectangle', 
    borderRadius: '8px',
    aspectRatio: '1.45/1'
  },
  { 
    id: 'circle', 
    name: 'Circle', 
    borderRadius: '50%',
    aspectRatio: '1/1'
  },
  { 
    id: 'diamond', 
    name: 'Diamond', 
    clipPath: 'polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)',
    aspectRatio: '1/1'
  },
  { 
    id: 'oval', 
    name: 'Oval', 
    borderRadius: '50% / 35%',
    aspectRatio: '1.35/1'
  },
];

interface HatColorway {
  id: string;
  name: string;
  badge: string;
  image: string;
}

const HAT_COLORWAYS: HatColorway[] = [
  { 
    id: 'charcoal-black', 
    name: 'Charcoal & Black Mesh', 
    badge: 'Best Seller',
    image: '/images/products/krown-r112-custom-charcoal-black-v9.jpg'
  },
  { 
    id: 'heather-black', 
    name: 'Heather Grey & Black Mesh', 
    badge: 'Modern Pro',
    image: '/images/products/krown-r112-custom-heather-grey-v9.jpg'
  },
  { 
    id: 'stealth-black', 
    name: 'Solid Obsidian Black', 
    badge: 'Stealth',
    image: '/images/products/krown-r112-custom-obsidian-black-v9.jpg'
  },
  { 
    id: 'khaki-coffee', 
    name: 'Khaki & Coffee Mesh', 
    badge: 'Classic 112',
    image: '/images/products/krown-r112-custom-khaki-coffee-v9.jpg'
  },
];

type PatchPlacement = 'center' | 'left' | 'right';

export default function CustomCrewPage() {
  const { addItem } = useCart();

  const [selectedTier, setSelectedTier] = useState<TierOption>(TIERS[2]); // Company 12-Pack by default
  const [selectedPatch, setSelectedPatch] = useState<PatchStyle>(PATCH_STYLES[0]);
  const [selectedShape, setSelectedShape] = useState<PatchShape>(PATCH_SHAPES[0]);
  const [selectedColorway, setSelectedColorway] = useState<HatColorway>(HAT_COLORWAYS[0]);
  const [patchPlacement, setPatchPlacement] = useState<PatchPlacement>('center');
  const [xOffset, setXOffset] = useState<number>(0);
  const [yOffset, setYOffset] = useState<number>(0);
  const [patchScale, setPatchScale] = useState<number>(100);

  const [companyName, setCompanyName] = useState<string>('');
  const [subText, setSubText] = useState<string>('EST. 2026');
  const [uploadedLogoUrl, setUploadedLogoUrl] = useState<string | null>(null);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [notes, setNotes] = useState<string>('');
  const [isAdded, setIsAdded] = useState<boolean>(false);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setUploadedFileName(file.name);
      const reader = new FileReader();
      reader.onload = (event) => {
        if (event.target?.result) {
          setUploadedLogoUrl(event.target.result as string);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  // Base placement left percentage
  const baseLeft = patchPlacement === 'left' ? 38 : patchPlacement === 'right' ? 62 : 50;
  const baseTop = 50;

  const currentLeft = `calc(${baseLeft}% + ${xOffset}px)`;
  const currentTop = `calc(${baseTop}% + ${yOffset}px)`;

  const handleAddToCart = () => {
    const title = `Custom Richardson 112 Hats (${selectedTier.qty}-Pack) - ${companyName || 'Custom Crew'}`;
    addItem({
      productId: 'custom-krown-works-hat',
      name: title,
      price: selectedTier.priceEach,
      image: selectedColorway.image,
      variant: {
        color: `${selectedColorway.name} • ${selectedPatch.name} (${selectedShape.name})`,
        size: `Qty: ${selectedTier.qty} Hats • ${patchPlacement.toUpperCase()} Placement`,
      },
      quantity: selectedTier.qty,
    });

    setIsAdded(true);
    setTimeout(() => setIsAdded(false), 3500);
  };

  return (
    <div className="custom-crew-page container">
      {/* Hero Section */}
      <section className="custom-crew-hero">
        <div className="custom-crew-badge">
          <span>★</span> KrowN Works Custom Headwear Studio
        </div>
        <h1 className="custom-crew-title">Custom Richardson 112 Leather Patch Hats</h1>
        <p className="custom-crew-subtitle">
          Outfit your jobsite crew, trade company, or esports team with authentic Richardson 112 trucker snapbacks.
          Interactive real-time 3D hat configurator: switch colorways, leather finishes, patch shapes, and upload your custom logo with live draggable placement.
        </p>
      </section>

      {/* Interactive Configurator Grid */}
      <div className="custom-grid">
        {/* Left Column: Interactive Visual Hat Studio */}
        <div className="custom-preview-card">
          <div className="custom-preview-img-wrap" style={{ position: 'relative', overflow: 'hidden', background: '#0e0f12' }}>
            <span className="custom-preview-badge-overlay" style={{ zIndex: 10 }}>
              LIVE PREVIEW: {selectedColorway.name} • {selectedPatch.name}
            </span>

            {/* Base Richardson 112 Hat Image */}
            <img
              src={selectedColorway.image}
              alt="Custom Richardson 112 Trucker Hat"
              className="custom-preview-img"
              style={{ width: '100%', height: '100%', objectFit: 'contain', transition: 'all 0.25s ease' }}
            />

            {/* Real-Time Interactive Leather Patch Layer */}
            <div
              style={{
                position: 'absolute',
                top: currentTop,
                left: currentLeft,
                transform: `translate(-50%, -50%) scale(${patchScale / 100})`,
                transition: 'top 0.15s ease, left 0.15s ease, transform 0.15s ease',
                width: '128px',
                aspectRatio: selectedShape.aspectRatio,
                background: selectedPatch.bg,
                clipPath: selectedShape.clipPath,
                borderRadius: selectedShape.borderRadius,
                boxShadow: '0 8px 24px rgba(0,0,0,0.65), inset 0 0 10px rgba(0,0,0,0.4)',
                border: selectedShape.borderRadius ? `2px solid ${selectedPatch.stitch}` : 'none',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '0.45rem',
                cursor: 'move',
                zIndex: 5,
                color: selectedPatch.color,
                textAlign: 'center',
                pointerEvents: 'none',
              }}
            >
              {/* Inner simulated stitch ring for clipPath shapes */}
              {selectedShape.clipPath && (
                <div 
                  style={{
                    position: 'absolute',
                    inset: '3px',
                    clipPath: selectedShape.clipPath,
                    border: `1.5px dashed ${selectedPatch.stitch}`,
                    opacity: 0.7,
                    pointerEvents: 'none'
                  }}
                />
              )}

              {/* Uploaded Artwork or Brand Monogram */}
              {uploadedLogoUrl ? (
                <img
                  src={uploadedLogoUrl}
                  alt="Custom Company Logo"
                  style={{
                    maxWidth: '65%',
                    maxHeight: '52%',
                    objectFit: 'contain',
                    filter: selectedPatch.id === 'black' ? 'brightness(1.4) drop-shadow(0 2px 4px rgba(0,0,0,0.8))' : 'contrast(1.6) drop-shadow(0 1px 2px rgba(0,0,0,0.4))',
                    marginBottom: '0.2rem',
                    zIndex: 2,
                  }}
                />
              ) : (
                <div style={{ fontSize: '1.25rem', fontWeight: 900, marginBottom: '0.15rem', zIndex: 2 }}>
                  👑
                </div>
              )}

              {/* Live Engraved Company / Team Name */}
              <div
                style={{
                  fontSize: '0.62rem',
                  fontWeight: 900,
                  letterSpacing: '0.04em',
                  textTransform: 'uppercase',
                  lineHeight: 1.1,
                  maxWidth: '92%',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                  zIndex: 2,
                  fontFamily: 'impact, sans-serif'
                }}
              >
                {companyName.trim() || 'YOUR LOGO'}
              </div>

              {subText && (
                <div
                  style={{
                    fontSize: '0.45rem',
                    fontWeight: 700,
                    letterSpacing: '0.06em',
                    textTransform: 'uppercase',
                    opacity: 0.85,
                    zIndex: 2
                  }}
                >
                  {subText}
                </div>
              )}
            </div>
          </div>

          {/* Interactive Patch Positioning Controls */}
          <div style={{
            background: 'rgba(255, 255, 255, 0.03)',
            border: '1px solid var(--border)',
            borderRadius: '8px',
            padding: '0.85rem',
            marginTop: '0.85rem'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.65rem' }}>
              <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-main)' }}>
                📍 Patch Placement on Hat
              </span>
              <div style={{ display: 'flex', gap: '0.35rem' }}>
                {(['left', 'center', 'right'] as PatchPlacement[]).map((pos) => (
                  <button
                    key={pos}
                    type="button"
                    onClick={() => {
                      setPatchPlacement(pos);
                      setXOffset(0);
                    }}
                    style={{
                      padding: '0.25rem 0.65rem',
                      fontSize: '0.75rem',
                      fontWeight: patchPlacement === pos ? 700 : 500,
                      background: patchPlacement === pos ? 'var(--accent-gold)' : 'rgba(255, 255, 255, 0.05)',
                      color: patchPlacement === pos ? '#000' : 'var(--text-muted)',
                      border: '1px solid rgba(255, 255, 255, 0.1)',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      textTransform: 'capitalize'
                    }}
                  >
                    {pos}
                  </button>
                ))}
              </div>
            </div>

            {/* Fine Position Sliders */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', fontSize: '0.75rem' }}>
              <div>
                <label style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', marginBottom: '0.2rem' }}>
                  <span>Horizontal Nudge</span>
                  <span>{xOffset}px</span>
                </label>
                <input
                  type="range"
                  min="-30"
                  max="30"
                  value={xOffset}
                  onChange={(e) => setXOffset(parseInt(e.target.value))}
                  style={{ width: '100%', accentColor: 'var(--accent-gold)' }}
                />
              </div>

              <div>
                <label style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', marginBottom: '0.2rem' }}>
                  <span>Vertical Height</span>
                  <span>{yOffset}px</span>
                </label>
                <input
                  type="range"
                  min="-25"
                  max="25"
                  value={yOffset}
                  onChange={(e) => setYOffset(parseInt(e.target.value))}
                  style={{ width: '100%', accentColor: 'var(--accent-gold)' }}
                />
              </div>
            </div>
          </div>

          <div style={{
            background: 'rgba(212, 175, 55, 0.08)',
            border: '1px solid rgba(212, 175, 55, 0.25)',
            borderRadius: '6px',
            padding: '0.65rem 0.85rem',
            marginTop: '0.75rem',
            fontSize: '0.8rem',
            color: 'var(--text-muted)'
          }}>
            <strong style={{ color: 'var(--accent-gold)' }}>★ Lifetime Durability:</strong> All patches are precision laser-engraved onto 100% genuine saddle leather or weather-grade leatherette, then heavy-stitched to authentic Richardson 112 crowns.
          </div>

          <div style={{ marginTop: '1.25rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.65rem' }}>
              Why Contractors &amp; Teams Choose KrowN Custom Hats:
            </h3>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                <span style={{ color: 'var(--accent-gold)', fontWeight: 'bold' }}>✓</span>
                <strong>Authentic Richardson 112:</strong> Mid-pro structured crown, pre-curved visor, breathable mesh.
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                <span style={{ color: 'var(--accent-gold)', fontWeight: 'bold' }}>✓</span>
                <strong>Perimeter Saddle Stitching:</strong> Heavy bonded thread around the perimeter—never glued.
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                <span style={{ color: 'var(--accent-gold)', fontWeight: 'bold' }}>✓</span>
                <strong>Free Digital Proof:</strong> 3D photorealistic mockups sent to your email prior to production.
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                <span style={{ color: 'var(--accent-gold)', fontWeight: 'bold' }}>✓</span>
                <strong>Fast 3-5 Day Production:</strong> Direct US fulfillment with tracked ground shipping.
              </li>
            </ul>
          </div>
        </div>

        {/* Right Column: Interactive Order Builder */}
        <div className="custom-form-card">
          <h2>Configure Your Custom Hat Order</h2>
          <p className="custom-form-desc">
            Select your volume tier, choose your hat colorway, leather patch material, and patch shape.
          </p>

          {/* Step 1: Volume Tier */}
          <div className="form-step">
            <div className="form-step-title">
              <span className="form-step-num">1</span>
              <span>Select Volume Tier (Quantity)</span>
            </div>
            <div className="tier-selector">
              {TIERS.map((tier) => (
                <div
                  key={tier.id}
                  className={`tier-option ${selectedTier.id === tier.id ? 'active' : ''}`}
                  onClick={() => setSelectedTier(tier)}
                  role="button"
                  tabIndex={0}
                >
                  <div className="tier-name">{tier.name}</div>
                  <div className="tier-qty">{tier.qty} {tier.qty === 1 ? 'Hat' : 'Hats'}</div>
                  <div className="tier-price-each">${tier.priceEach.toFixed(2)}/ea</div>
                  {tier.badge && <span className="tier-badge">{tier.badge}</span>}
                  {tier.savings && !tier.badge && (
                    <span style={{ display: 'block', fontSize: '0.65rem', color: '#d4af37', marginTop: '0.25rem' }}>
                      {tier.savings}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Step 2: Select Richardson 112 Colorway */}
          <div className="form-step">
            <div className="form-step-title">
              <span className="form-step-num">2</span>
              <span>Select Richardson 112 Colorway</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.65rem' }}>
              {HAT_COLORWAYS.map((c) => (
                <div
                  key={c.id}
                  className={`patch-option ${selectedColorway.id === c.id ? 'active' : ''}`}
                  onClick={() => setSelectedColorway(c)}
                  role="button"
                  tabIndex={0}
                  style={{
                    padding: '0.65rem 0.8rem',
                    border: selectedColorway.id === c.id ? '2px solid var(--accent-gold)' : '1px solid var(--border)',
                    background: selectedColorway.id === c.id ? 'rgba(212, 175, 55, 0.12)' : 'var(--background)',
                    borderRadius: '8px',
                    cursor: 'pointer'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ fontWeight: 700, fontSize: '0.85rem' }}>{c.name}</div>
                    <span style={{ fontSize: '0.65rem', color: 'var(--accent-gold)', fontWeight: 600 }}>{c.badge}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Step 3: Choose Leather Patch Style */}
          <div className="form-step">
            <div className="form-step-title">
              <span className="form-step-num">3</span>
              <span>Choose Leather Patch Material</span>
            </div>
            <div className="patch-selector">
              {PATCH_STYLES.map((patch) => (
                <div
                  key={patch.id}
                  className={`patch-option ${selectedPatch.id === patch.id ? 'active' : ''}`}
                  onClick={() => setSelectedPatch(patch)}
                  role="button"
                  tabIndex={0}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.2rem' }}>
                    <span style={{ width: '14px', height: '14px', borderRadius: '50%', background: patch.bg, display: 'inline-block', border: '1px solid #000' }} />
                    <div style={{ fontWeight: 700 }}>{patch.name}</div>
                  </div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', lineHeight: 1.3 }}>{patch.desc}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Step 4: Patch Shape */}
          <div className="form-step">
            <div className="form-step-title">
              <span className="form-step-num">4</span>
              <span>Select Patch Shape</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '0.5rem' }}>
              {PATCH_SHAPES.map((shape) => (
                <div
                  key={shape.id}
                  onClick={() => setSelectedShape(shape)}
                  role="button"
                  tabIndex={0}
                  style={{
                    padding: '0.6rem 0.35rem',
                    textAlign: 'center',
                    border: selectedShape.id === shape.id ? '2px solid var(--accent-gold)' : '1px solid var(--border)',
                    background: selectedShape.id === shape.id ? 'rgba(212, 175, 55, 0.15)' : 'var(--background)',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontSize: '0.75rem',
                    fontWeight: selectedShape.id === shape.id ? 700 : 500,
                    color: selectedShape.id === shape.id ? 'var(--accent-gold)' : 'var(--text-main)'
                  }}
                >
                  <div style={{
                    width: '28px',
                    height: '24px',
                    margin: '0 auto 0.35rem',
                    background: selectedPatch.bg,
                    clipPath: shape.clipPath,
                    borderRadius: shape.borderRadius,
                    border: shape.borderRadius ? '1px solid rgba(255,255,255,0.4)' : 'none'
                  }} />
                  {shape.name}
                </div>
              ))}
            </div>
          </div>

          {/* Step 5: Custom Artwork & Text */}
          <div className="form-step">
            <div className="form-step-title">
              <span className="form-step-num">5</span>
              <span>Company / Team Name &amp; Artwork</span>
            </div>

            <div className="form-group" style={{ marginBottom: '0.85rem' }}>
              <label htmlFor="company-name" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Primary Name (Live Patch Engraving):
              </label>
              <input
                type="text"
                id="company-name"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value.slice(0, 24))}
                placeholder="e.g. Apex Electrical, Ironwood Framers"
                className="form-input"
              />
            </div>

            <div className="form-group" style={{ marginBottom: '0.85rem' }}>
              <label htmlFor="sub-text" style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Secondary Subtitle / Year / City:
              </label>
              <input
                type="text"
                id="sub-text"
                value={subText}
                onChange={(e) => setSubText(e.target.value.slice(0, 20))}
                placeholder="e.g. EST. 2018 or AUSTIN, TX"
                className="form-input"
              />
            </div>

            {/* File Upload */}
            <div className="file-upload-box">
              <input
                type="file"
                id="logo-upload"
                accept="image/png, image/jpeg, image/svg+xml"
                onChange={handleFileUpload}
                style={{ display: 'none' }}
              />
              <label htmlFor="logo-upload" style={{ cursor: 'pointer', display: 'block' }}>
                <span className="upload-icon">📁</span>
                <p style={{ fontWeight: 600, marginBottom: '0.25rem', fontSize: '0.85rem' }}>
                  {uploadedFileName ? `Attached: ${uploadedFileName}` : 'Upload Logo (.PNG, .JPG, .SVG)'}
                </p>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Drag &amp; drop or click to browse. Transparent background recommended.
                </p>
              </label>
            </div>
          </div>

          {/* Pricing & Add to Cart */}
          <div className="order-summary-box">
            <div className="summary-row">
              <span className="summary-label">Quantity:</span>
              <span className="summary-val">{selectedTier.qty} {selectedTier.qty === 1 ? 'Hat' : 'Hats'} ({selectedTier.name})</span>
            </div>
            <div className="summary-row">
              <span className="summary-label">Colorway:</span>
              <span className="summary-val">{selectedColorway.name}</span>
            </div>
            <div className="summary-row">
              <span className="summary-label">Patch:</span>
              <span className="summary-val">{selectedPatch.name} • {selectedShape.name} ({patchPlacement.toUpperCase()})</span>
            </div>
            <div className="summary-row">
              <span className="summary-label">Price Per Hat:</span>
              <span className="summary-val">${selectedTier.priceEach.toFixed(2)}</span>
            </div>
            <div className="summary-total-row">
              <span className="summary-total-label">Total Crew Investment:</span>
              <span className="summary-total-val">${selectedTier.total.toFixed(2)}</span>
            </div>

            <button
              type="button"
              className="btn-primary custom-order-btn"
              onClick={handleAddToCart}
              style={{ width: '100%', marginTop: '1rem', padding: '0.9rem', fontSize: '1rem', fontWeight: 800 }}
            >
              {isAdded ? '✓ Added Custom Pack to Cart!' : `Add to Cart — $${selectedTier.total.toFixed(2)}`}
            </button>

            {isAdded && (
              <div style={{ marginTop: '0.75rem', textAlign: 'center' }}>
                <Link href="/cart" style={{ color: 'var(--accent-gold)', fontSize: '0.875rem', textDecoration: 'underline' }}>
                  Proceed to Checkout &rarr;
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
