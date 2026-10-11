"use client";

import React, { useState, useEffect } from 'react';
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

interface LeatherFinish {
  id: string;
  name: string;
  desc: string;
  swatchBg: string;
  gradient: string;
  engraveColor: string;
  stitchColor: string;
  engraveBlend: 'multiply' | 'screen' | 'normal';
  engraveFilter: string;
}

const LEATHER_FINISHES: LeatherFinish[] = [
  {
    id: 'caramel-cowhide',
    name: 'Caramel / Cognac Cowhide',
    desc: 'Rich warm amber/brown with authentic cowhide pore grain & dark charred laser burn',
    swatchBg: 'linear-gradient(135deg, #b87333 0%, #c68642 100%)',
    gradient: 'linear-gradient(135deg, #c47c38 0%, #b87333 45%, #9b5a20 100%)',
    engraveColor: '#281406',
    stitchColor: '#2E1B0E',
    engraveBlend: 'multiply',
    engraveFilter: 'grayscale(100%) contrast(240%) brightness(0.68) sepia(55%) hue-rotate(330deg)',
  },
  {
    id: 'natural-saddle-tan',
    name: 'Natural Saddle Tan',
    desc: 'Classic light vegetable-tanned hide with fine-pore grain & deep walnut laser engraving',
    swatchBg: 'linear-gradient(135deg, #d2b55b 0%, #c19a6b 100%)',
    gradient: 'linear-gradient(135deg, #dbbe68 0%, #d2b55b 45%, #b8915e 100%)',
    engraveColor: '#241408',
    stitchColor: '#3a2010',
    engraveBlend: 'multiply',
    engraveFilter: 'grayscale(100%) contrast(250%) brightness(0.62) sepia(60%) hue-rotate(335deg)',
  },
  {
    id: 'dark-rustic-walnut',
    name: 'Dark Rustic Walnut',
    desc: 'Deep espresso hide with high-contrast warm chocolate laser engraving',
    swatchBg: 'linear-gradient(135deg, #3d2314 0%, #4a2e1b 100%)',
    gradient: 'linear-gradient(135deg, #4f331f 0%, #3d2314 50%, #2a160a 100%)',
    engraveColor: '#120803',
    stitchColor: '#1c0c04',
    engraveBlend: 'multiply',
    engraveFilter: 'grayscale(100%) contrast(260%) brightness(0.55) sepia(70%) hue-rotate(320deg)',
  },
  {
    id: 'matte-black-hide',
    name: 'Matte Black / Charcoal Hide',
    desc: 'Stealth blackout leatherette with subtle charcoal undertone & laser-etched contrast',
    swatchBg: 'linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%)',
    gradient: 'linear-gradient(135deg, #2b2b2b 0%, #1e1e1e 50%, #141414 100%)',
    engraveColor: '#d6b160',
    stitchColor: '#3d3d3d',
    engraveBlend: 'screen',
    engraveFilter: 'grayscale(100%) contrast(200%) brightness(1.7) sepia(50%) hue-rotate(5deg)',
  },
];

interface PatchShape {
  id: string;
  name: string;
  clipPath?: string;
  borderRadius?: string;
  aspectRatio: string;
  widthPx: number;
}

const PATCH_SHAPES: PatchShape[] = [
  {
    id: 'hexagon',
    name: 'Hexagon',
    clipPath: 'polygon(50% 0%, 98% 25%, 98% 75%, 50% 100%, 2% 75%, 2% 25%)',
    aspectRatio: '1.05 / 1',
    widthPx: 124,
  },
  {
    id: 'rounded-rectangle',
    name: 'Rounded Rectangle',
    borderRadius: '10px',
    aspectRatio: '1.45 / 1',
    widthPx: 134,
  },
  {
    id: 'circle',
    name: 'Circle',
    borderRadius: '50%',
    aspectRatio: '1 / 1',
    widthPx: 118,
  },
  {
    id: 'diamond',
    name: 'Diamond',
    clipPath: 'polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)',
    aspectRatio: '1 / 1',
    widthPx: 120,
  },
  {
    id: 'oval',
    name: 'Oval',
    borderRadius: '50% / 35%',
    aspectRatio: '1.38 / 1',
    widthPx: 130,
  },
];

interface HatColorway {
  id: string;
  name: string;
  subtitle: string;
  badge?: string;
  image: string;
  swatchFront: string;
  swatchMesh: string;
}

const PRINTIFY_COLORWAYS: HatColorway[] = [
  {
    id: 'charcoal-black',
    name: 'Charcoal / Black Mesh',
    subtitle: 'Best Seller / Industrial Neutral',
    badge: 'Best Seller',
    image: '/images/custom-crew/r112-blank-charcoal-black.jpg',
    swatchFront: '#3a3a3c',
    swatchMesh: '#161616',
  },
  {
    id: 'heather-black',
    name: 'Heather Grey / Black Mesh',
    subtitle: 'Modern Classic Contrast',
    badge: 'Popular',
    image: '/images/custom-crew/r112-blank-heather-black.jpg',
    swatchFront: '#757579',
    swatchMesh: '#161616',
  },
  {
    id: 'solid-black',
    name: 'Solid Black',
    subtitle: 'Black buckram / Black mesh / Stealth',
    badge: 'Stealth',
    image: '/images/custom-crew/r112-blank-solid-black.jpg',
    swatchFront: '#1a1a1a',
    swatchMesh: '#141414',
  },
  {
    id: 'khaki-coffee',
    name: 'Khaki / Coffee Mesh',
    subtitle: 'Heritage Earth Tone / Outdoor',
    image: '/images/custom-crew/r112-blank-khaki-coffee.jpg',
    swatchFront: '#a89474',
    swatchMesh: '#3a271b',
  },
  {
    id: 'heather-navy',
    name: 'Heather Grey / Navy Mesh',
    subtitle: 'Collegiate Navy Contrast',
    image: '/images/custom-crew/r112-blank-heather-navy.jpg',
    swatchFront: '#757579',
    swatchMesh: '#192841',
  },
  {
    id: 'loden-black',
    name: 'Loden / Black Mesh',
    subtitle: 'Tactical Olive / Dark Mesh',
    image: '/images/custom-crew/r112-blank-loden-black.jpg',
    swatchFront: '#4a5340',
    swatchMesh: '#161616',
  },
  {
    id: 'white-black',
    name: 'White / Black Mesh',
    subtitle: 'High-Contrast Monochrome',
    image: '/images/custom-crew/r112-blank-white-black.jpg',
    swatchFront: '#3a3a3c',
    swatchMesh: '#f0f0f2',
  },
];

type PatchPlacement = 'center' | 'left';

export default function CustomCrewPage() {
  const { addItem } = useCart();

  const [selectedTier, setSelectedTier] = useState<TierOption>(TIERS[2]); // Company 12-Pack by default
  const [selectedColorway, setSelectedColorway] = useState<HatColorway>(PRINTIFY_COLORWAYS[0]);
  const [selectedFinish, setSelectedFinish] = useState<LeatherFinish>(LEATHER_FINISHES[0]);
  const [selectedShape, setSelectedShape] = useState<PatchShape>(PATCH_SHAPES[0]);
  const [patchPlacement, setPatchPlacement] = useState<PatchPlacement>('center');
  const [xOffset, setXOffset] = useState<number>(0);
  const [yOffset, setYOffset] = useState<number>(0);
  const [patchScale, setPatchScale] = useState<number>(100);

  const [companyName, setCompanyName] = useState<string>('');
  const [subText, setSubText] = useState<string>('EST. 2026');
  const [uploadedLogoUrl, setUploadedLogoUrl] = useState<string | null>(null);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [isAdded, setIsAdded] = useState<boolean>(false);

  // Preload all 7 blanks on mount for instantaneous, zero-flicker switching
  useEffect(() => {
    PRINTIFY_COLORWAYS.forEach((colorway) => {
      const img = new window.Image();
      img.src = colorway.image;
    });
  }, []);

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

  // Base placement calibrated to Richardson 112 crown perspective
  const baseLeft = patchPlacement === 'left' ? 34.5 : 42.0;
  const baseTop = patchPlacement === 'left' ? 44.5 : 42.5;

  const currentLeft = `calc(${baseLeft}% + ${xOffset}px)`;
  const currentTop = `calc(${baseTop}% + ${yOffset}px)`;

  const handleAddToCart = () => {
    const title = `Custom Richardson 112 Hats (${selectedTier.qty}-Pack) - ${companyName.trim() || 'Custom Crew'}`;
    addItem({
      productId: 'custom-krown-works-hat',
      name: title,
      price: selectedTier.priceEach,
      image: selectedColorway.image,
      variant: {
        color: `${selectedColorway.name} • ${selectedFinish.name} (${selectedShape.name})`,
        size: `Printify 1743/99 • Qty: ${selectedTier.qty} • ${patchPlacement.toUpperCase()} Panel`,
      },
      quantity: selectedTier.qty,
      personalization: {
        edition: `Printify Blueprint 1743 / Provider 99 • ${selectedFinish.name} • ${selectedShape.name}`,
        notes: `Placement: ${patchPlacement.toUpperCase()} | Company: "${companyName.trim() || 'N/A'}" | Subtext: "${subText.trim() || 'N/A'}" | Logo: ${uploadedFileName || 'Crown Monogram'}`,
      },
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
          Outfit your jobsite crew, trade company, or brand with genuine Richardson 112 trucker snapbacks (Printify Blueprint 1743).
          Real-time photorealistic configurator with authentic leather finishes, custom laser engraving, and perimeter saddle stitching.
        </p>
      </section>

      {/* Interactive Configurator Grid */}
      <div className="custom-grid">
        {/* Left Column: Interactive Visual Hat Studio */}
        <div className="custom-preview-card">
          <div className="custom-preview-img-wrap" style={{ position: 'relative', overflow: 'hidden', background: '#0e0f12' }}>
            <span className="custom-preview-badge-overlay" style={{ zIndex: 20 }}>
              LIVE PREVIEW: {selectedColorway.name} • {selectedFinish.name}
            </span>

            {/* Base Richardson 112 Hat Image */}
            <img
              src={selectedColorway.image}
              alt="Custom Richardson 112 Trucker Hat"
              className="custom-preview-img"
              style={{ width: '100%', height: '100%', objectFit: 'contain', transition: 'opacity 0.2s ease' }}
            />

            {/* Real-Time Interactive Leather Patch Layer with 3D Perspective */}
            <div
              className="photoreal-patch-container"
              style={{
                position: 'absolute',
                top: currentTop,
                left: currentLeft,
                transform: `perspective(900px) rotate(-1.5deg) rotateY(4deg) skewY(-1deg) translate(-50%, -50%) scale(${patchScale / 100})`,
                transition: 'top 0.15s ease, left 0.15s ease, transform 0.15s ease',
                width: `${selectedShape.widthPx}px`,
                aspectRatio: selectedShape.aspectRatio,
                background: selectedFinish.gradient,
                clipPath: selectedShape.clipPath,
                borderRadius: selectedShape.borderRadius,
                filter: 'drop-shadow(0 6px 8px rgba(0,0,0,0.65)) drop-shadow(0 2px 3px rgba(0,0,0,0.45))',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                padding: '0.65rem 0.5rem',
                zIndex: 10,
                color: selectedFinish.engraveColor,
                textAlign: 'center',
                pointerEvents: 'none',
              }}
            >
              {/* Natural Leather Grain & Texture Shading Overlay */}
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  clipPath: selectedShape.clipPath,
                  borderRadius: selectedShape.borderRadius,
                  backgroundImage: `radial-gradient(ellipse at 35% 30%, rgba(255,255,255,0.18) 0%, rgba(0,0,0,0.22) 100%)`,
                  pointerEvents: 'none',
                }}
              />

              {/* Perimeter Embossed Saddle Stitching Ring */}
              <svg
                style={{
                  position: 'absolute',
                  inset: 0,
                  width: '100%',
                  height: '100%',
                  pointerEvents: 'none',
                  zIndex: 2,
                }}
              >
                {selectedShape.id === 'hexagon' && (
                  <polygon
                    points="50 4, 95 27, 95 73, 50 96, 5 73, 5 27"
                    viewBox="0 0 100 100"
                    fill="none"
                    stroke={selectedFinish.stitchColor}
                    strokeWidth="1.5"
                    strokeDasharray="4 3"
                    opacity="0.85"
                  />
                )}
                {selectedShape.id === 'rounded-rectangle' && (
                  <rect
                    x="5%"
                    y="6%"
                    width="90%"
                    height="88%"
                    rx="8"
                    ry="8"
                    fill="none"
                    stroke={selectedFinish.stitchColor}
                    strokeWidth="1.5"
                    strokeDasharray="4 3"
                    opacity="0.85"
                  />
                )}
                {selectedShape.id === 'circle' && (
                  <circle
                    cx="50%"
                    cy="50%"
                    r="44%"
                    fill="none"
                    stroke={selectedFinish.stitchColor}
                    strokeWidth="1.5"
                    strokeDasharray="4 3"
                    opacity="0.85"
                  />
                )}
                {selectedShape.id === 'diamond' && (
                  <polygon
                    points="50 5, 95 50, 50 95, 5 50"
                    fill="none"
                    stroke={selectedFinish.stitchColor}
                    strokeWidth="1.5"
                    strokeDasharray="4 3"
                    opacity="0.85"
                  />
                )}
                {selectedShape.id === 'oval' && (
                  <ellipse
                    cx="50%"
                    cy="50%"
                    rx="44%"
                    ry="38%"
                    fill="none"
                    stroke={selectedFinish.stitchColor}
                    strokeWidth="1.5"
                    strokeDasharray="4 3"
                    opacity="0.85"
                  />
                )}
              </svg>

              {/* Uploaded Artwork or Brand Monogram with Genuine Laser-Burn Blending */}
              {uploadedLogoUrl ? (
                <div
                  style={{
                    maxWidth: '68%',
                    maxHeight: '52%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: '0.2rem',
                    zIndex: 3,
                    mixBlendMode: selectedFinish.engraveBlend,
                    filter: selectedFinish.engraveFilter,
                  }}
                >
                  <img
                    src={uploadedLogoUrl}
                    alt="Custom Company Logo"
                    style={{
                      maxWidth: '100%',
                      maxHeight: '100%',
                      objectFit: 'contain',
                      filter: 'drop-shadow(0 1px 1px rgba(255, 255, 255, 0.2)) drop-shadow(0 -1px 1px rgba(0, 0, 0, 0.85))',
                    }}
                  />
                </div>
              ) : (
                <div
                  style={{
                    fontSize: '1.35rem',
                    fontWeight: 900,
                    marginBottom: '0.15rem',
                    zIndex: 3,
                    color: selectedFinish.engraveColor,
                    filter: 'drop-shadow(0 1px 1px rgba(255, 255, 255, 0.25)) drop-shadow(0 -1px 1px rgba(0, 0, 0, 0.85))',
                  }}
                >
                  👑
                </div>
              )}

              {/* Live Debossed Company / Team Name */}
              <div
                style={{
                  fontSize: '0.62rem',
                  fontWeight: 900,
                  letterSpacing: '0.04em',
                  textTransform: 'uppercase',
                  lineHeight: 1.15,
                  maxWidth: '92%',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                  zIndex: 3,
                  fontFamily: 'impact, sans-serif',
                  color: selectedFinish.engraveColor,
                  filter: 'drop-shadow(0 1px 1px rgba(255, 255, 255, 0.2)) drop-shadow(0 -1px 1px rgba(0, 0, 0, 0.85))',
                }}
              >
                {companyName.trim() || 'YOUR LOGO'}
              </div>

              {subText && (
                <div
                  style={{
                    fontSize: '0.45rem',
                    fontWeight: 800,
                    letterSpacing: '0.06em',
                    textTransform: 'uppercase',
                    opacity: 0.9,
                    zIndex: 3,
                    color: selectedFinish.engraveColor,
                    filter: 'drop-shadow(0 1px 0.5px rgba(255, 255, 255, 0.2)) drop-shadow(0 -0.5px 0.5px rgba(0, 0, 0, 0.85))',
                  }}
                >
                  {subText}
                </div>
              )}
            </div>
          </div>

          {/* Interactive Patch Positioning Controls */}
          <div
            style={{
              background: 'rgba(255, 255, 255, 0.03)',
              border: '1px solid var(--border)',
              borderRadius: '8px',
              padding: '0.85rem',
              marginTop: '0.85rem',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.65rem' }}>
              <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-main)' }}>
                📍 Patch Placement on Hat
              </span>
              <div style={{ display: 'flex', gap: '0.35rem' }}>
                {(['center', 'left'] as PatchPlacement[]).map((pos) => (
                  <button
                    key={pos}
                    type="button"
                    onClick={() => {
                      setPatchPlacement(pos);
                      setXOffset(0);
                      setYOffset(0);
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
                      textTransform: 'capitalize',
                    }}
                  >
                    {pos === 'center' ? 'Center Crown' : 'Left Panel'}
                  </button>
                ))}
              </div>
            </div>

            {/* Fine Position Sliders */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.65rem', fontSize: '0.75rem' }}>
              <div>
                <label style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', marginBottom: '0.2rem' }}>
                  <span>Scale</span>
                  <span>{patchScale}%</span>
                </label>
                <input
                  type="range"
                  min="80"
                  max="125"
                  value={patchScale}
                  onChange={(e) => setPatchScale(parseInt(e.target.value))}
                  style={{ width: '100%', accentColor: 'var(--accent-gold)' }}
                />
              </div>

              <div>
                <label style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', marginBottom: '0.2rem' }}>
                  <span>Horizontal</span>
                  <span>{xOffset}px</span>
                </label>
                <input
                  type="range"
                  min="-25"
                  max="25"
                  value={xOffset}
                  onChange={(e) => setXOffset(parseInt(e.target.value))}
                  style={{ width: '100%', accentColor: 'var(--accent-gold)' }}
                />
              </div>

              <div>
                <label style={{ display: 'flex', justifyContent: 'space-between', color: 'var(--text-muted)', marginBottom: '0.2rem' }}>
                  <span>Vertical</span>
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

          <div
            style={{
              background: 'rgba(212, 175, 55, 0.08)',
              border: '1px solid rgba(212, 175, 55, 0.25)',
              borderRadius: '6px',
              padding: '0.65rem 0.85rem',
              marginTop: '0.75rem',
              fontSize: '0.8rem',
              color: 'var(--text-muted)',
            }}
          >
            <strong style={{ color: 'var(--accent-gold)' }}>★ Printify Blueprint 1743:</strong> Verified authentic Richardson 112 trucker snapbacks with precision laser-etched genuine leatherette patches &amp; perimeter saddle stitching.
          </div>

          <div style={{ marginTop: '1.25rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '0.65rem' }}>
              Why Companies &amp; Contractors Choose KrowN Custom Hats:
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
            Select your volume tier, choose your Printify-verified colorway, leather patch material, and patch shape.
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

          {/* Step 2: Select Printify Richardson 112 Colorway */}
          <div className="form-step">
            <div className="form-step-title">
              <span className="form-step-num">2</span>
              <span>Select Richardson 112 Colorway (Blueprint 1743)</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(1, 1fr)', gap: '0.5rem' }}>
              {PRINTIFY_COLORWAYS.map((c) => (
                <div
                  key={c.id}
                  className={`patch-option ${selectedColorway.id === c.id ? 'active' : ''}`}
                  onClick={() => setSelectedColorway(c)}
                  role="button"
                  tabIndex={0}
                  style={{
                    padding: '0.65rem 0.85rem',
                    border: selectedColorway.id === c.id ? '2px solid var(--accent-gold)' : '1px solid var(--border)',
                    background: selectedColorway.id === c.id ? 'rgba(212, 175, 55, 0.12)' : 'var(--background)',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                    <div style={{ display: 'flex', width: '24px', height: '24px', borderRadius: '50%', overflow: 'hidden', border: '1px solid rgba(255,255,255,0.2)' }}>
                      <span style={{ width: '50%', height: '100%', background: c.swatchFront }} />
                      <span style={{ width: '50%', height: '100%', background: c.swatchMesh }} />
                    </div>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: '0.85rem', textAlign: 'left' }}>{c.name}</div>
                      <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textAlign: 'left' }}>{c.subtitle}</div>
                    </div>
                  </div>
                  {c.badge && (
                    <span style={{ fontSize: '0.65rem', color: 'var(--accent-gold)', fontWeight: 700, background: 'rgba(212,175,55,0.15)', padding: '2px 6px', borderRadius: '4px' }}>
                      {c.badge}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Step 3: Choose Printify-Supported Leather Finish */}
          <div className="form-step">
            <div className="form-step-title">
              <span className="form-step-num">3</span>
              <span>Choose Leather Patch Material</span>
            </div>
            <div className="patch-selector" style={{ gridTemplateColumns: 'repeat(2, 1fr)' }}>
              {LEATHER_FINISHES.map((patch) => (
                <div
                  key={patch.id}
                  className={`patch-option ${selectedFinish.id === patch.id ? 'active' : ''}`}
                  onClick={() => setSelectedFinish(patch)}
                  role="button"
                  tabIndex={0}
                  style={{
                    border: selectedFinish.id === patch.id ? '2px solid var(--accent-gold)' : '1px solid var(--border)',
                    background: selectedFinish.id === patch.id ? 'rgba(212, 175, 55, 0.12)' : 'var(--background)',
                    textAlign: 'left',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                    <span style={{ width: '16px', height: '16px', borderRadius: '50%', background: patch.swatchBg, display: 'inline-block', border: '1px solid rgba(0,0,0,0.6)', flexShrink: 0 }} />
                    <div style={{ fontWeight: 700, fontSize: '0.82rem' }}>{patch.name}</div>
                  </div>
                  <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', lineHeight: 1.3 }}>{patch.desc}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Step 4: Patch Shape */}
          <div className="form-step">
            <div className="form-step-title">
              <span className="form-step-num">4</span>
              <span>Select Patch Shape (Laser-Cut Dies)</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '0.5rem' }}>
              {PATCH_SHAPES.map((shape) => (
                <div
                  key={shape.id}
                  onClick={() => setSelectedShape(shape)}
                  role="button"
                  tabIndex={0}
                  style={{
                    padding: '0.6rem 0.25rem',
                    textAlign: 'center',
                    border: selectedShape.id === shape.id ? '2px solid var(--accent-gold)' : '1px solid var(--border)',
                    background: selectedShape.id === shape.id ? 'rgba(212, 175, 55, 0.15)' : 'var(--background)',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontSize: '0.72rem',
                    fontWeight: selectedShape.id === shape.id ? 700 : 500,
                    color: selectedShape.id === shape.id ? 'var(--accent-gold)' : 'var(--text-main)',
                  }}
                >
                  <div
                    style={{
                      width: '28px',
                      height: '24px',
                      margin: '0 auto 0.35rem',
                      background: selectedFinish.gradient,
                      clipPath: shape.clipPath,
                      borderRadius: shape.borderRadius,
                      border: shape.borderRadius ? `1px solid ${selectedFinish.stitchColor}` : 'none',
                    }}
                  />
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
                accept="image/png, image/jpeg, image/svg+xml, image/webp"
                onChange={handleFileUpload}
                style={{ display: 'none' }}
              />
              <label htmlFor="logo-upload" style={{ cursor: 'pointer', display: 'block' }}>
                <span className="upload-icon">📁</span>
                <p style={{ fontWeight: 600, marginBottom: '0.25rem', fontSize: '0.85rem' }}>
                  {uploadedFileName ? `Attached: ${uploadedFileName}` : 'Upload Logo (.PNG, .JPG, .SVG, .WebP)'}
                </p>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Laser burn blend will automatically embed your logo into the leather grain.
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
              <span className="summary-label">Leather Finish:</span>
              <span className="summary-val">{selectedFinish.name} • {selectedShape.name}</span>
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
              style={{ width: '100%', marginTop: '1rem', padding: '0.95rem', fontSize: '1.05rem', fontWeight: 800 }}
            >
              {isAdded ? '✓ Added Custom Pack to Cart!' : `ADD ${selectedTier.qty} ${selectedTier.qty === 1 ? 'HAT' : 'HATS'} TO CART — $${selectedTier.total.toFixed(2)}`}
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
