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

const PATCH_STYLES = [
  { id: 'caramel', name: 'Caramel Cowhide', desc: 'Warm rustic saddle leather, dark engraved burn' },
  { id: 'black', name: 'Obsidian Leatherette', desc: 'Matte black leather with metallic silver/gold burn' },
  { id: 'raw-tan', name: 'Raw Natural Tan', desc: 'High-contrast light tan with deep walnut burn' },
];

const HAT_COLORWAYS = [
  { id: 'khaki-coffee', name: 'Khaki / Coffee Mesh', badge: 'Authentic 112' },
  { id: 'stealth-black', name: 'Solid Black / Black Mesh', badge: 'Stealth' },
  { id: 'heather-black', name: 'Heather Grey / Black Mesh', badge: 'Modern' },
  { id: 'navy-white', name: 'Navy / White Mesh', badge: 'Classic' },
];

export default function CustomCrewPage() {
  const { addItem } = useCart();

  const [selectedTier, setSelectedTier] = useState<TierOption>(TIERS[2]); // Company 12-Pack by default
  const [selectedPatch, setSelectedPatch] = useState(PATCH_STYLES[0]);
  const [selectedColorway, setSelectedColorway] = useState(HAT_COLORWAYS[0]);
  const [companyName, setCompanyName] = useState('');
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);
  const [notes, setNotes] = useState('');
  const [isAdded, setIsAdded] = useState(false);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setUploadedFileName(e.target.files[0].name);
    }
  };

  const handleAddToCart = () => {
    const title = `Custom Richardson 112 Hats (${selectedTier.qty}-Pack) - ${companyName || 'Custom Crew'}`;
    addItem({
      productId: 'custom-krown-works-hat',
      name: title,
      price: selectedTier.priceEach,
      image: '/images/products/krown-r112-custom-supply-sample.jpg',
      variant: {
        color: `${selectedColorway.name} • ${selectedPatch.name}`,
        size: `Qty: ${selectedTier.qty} Hats (OSFM Snapback)`,
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
          <span>★</span> KrowN Works B2B / Custom Division
        </div>
        <h1 className="custom-crew-title">Custom Richardson 112 Leather Patch Hats</h1>
        <p className="custom-crew-subtitle">
          Outfit your jobsite crew, trade company, or gaming team with authentic Richardson 112 trucker snapbacks.
          Laser-engraved genuine leather patches saddle-stitched for lifetime durability.
        </p>
      </section>

      {/* Interactive Configurator Grid */}
      <div className="custom-grid">
        {/* Left Column: Visual Preview & Specs */}
        <div className="custom-preview-card">
          <div className="custom-preview-img-wrap">
            <span className="custom-preview-badge-overlay">
              DISPLAY DEMO: KrowN Supply Co. • {selectedColorway.name}
            </span>
            <Image
              src="/images/products/krown-r112-custom-supply-sample.jpg"
              alt="Custom Richardson 112 Leather Patch Trucker Hat Preview"
              width={600}
              height={600}
              priority
              className="custom-preview-img"
            />
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
            <strong style={{ color: 'var(--accent-gold)' }}>★ Display Demonstration:</strong> This hat is shown with our official <strong>KrowN Supply Co.</strong> leather patch as a finished production sample. Your crew order will be custom-engraved with your own uploaded company, trade crew, or team logo.
          </div>

          <div style={{ marginTop: '1.5rem' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.75rem' }}>
              Why Contractors & Teams Choose KrowN Custom Hats:
            </h3>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                <span style={{ color: 'var(--accent-gold)', fontWeight: 'bold' }}>✓</span>
                <strong>Authentic Richardson 112:</strong> Mid-pro structured crown, pre-curved visor, breathable mesh.
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                <span style={{ color: 'var(--accent-gold)', fontWeight: 'bold' }}>✓</span>
                <strong>Genuine Saddle Leather:</strong> 100% vegetable-tanned cowhide or ultra-durable matte leatherette.
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                <span style={{ color: 'var(--accent-gold)', fontWeight: 'bold' }}>✓</span>
                <strong>Heavy Stitch Attachment:</strong> Stitched around the perimeter—never heat-pressed or glued.
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                <span style={{ color: 'var(--accent-gold)', fontWeight: 'bold' }}>✓</span>
                <strong>Free Digital Proof:</strong> 3D photorealistic mockups sent to your email prior to production.
              </li>
              <li style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                <span style={{ color: 'var(--accent-gold)', fontWeight: 'bold' }}>✓</span>
                <strong>Fast 5-7 Day Turnaround:</strong> Direct US fulfillment with tracked shipping.
              </li>
            </ul>
          </div>
        </div>

        {/* Right Column: Interactive Order Builder */}
        <div className="custom-form-card">
          <h2>Configure Your Crew Order</h2>
          <p className="custom-form-desc">
            Select your volume tier, choose your patch finish, and upload your vector logo or sketch.
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

          {/* Step 2: Patch Style */}
          <div className="form-step">
            <div className="form-step-title">
              <span className="form-step-num">2</span>
              <span>Choose Leather Patch Style</span>
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
                  <div style={{ fontWeight: 700, marginBottom: '0.2rem' }}>{patch.name}</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', lineHeight: 1.3 }}>{patch.desc}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Step 3: Hat Colorway */}
          <div className="form-step">
            <div className="form-step-title">
              <span className="form-step-num">3</span>
              <span>Select Richardson 112 Colorway</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.75rem' }}>
              {HAT_COLORWAYS.map((c) => (
                <div
                  key={c.id}
                  className={`patch-option ${selectedColorway.id === c.id ? 'active' : ''}`}
                  onClick={() => setSelectedColorway(c)}
                  role="button"
                  tabIndex={0}
                >
                  <div style={{ fontWeight: 700, fontSize: '0.85rem' }}>{c.name}</div>
                  <span style={{ fontSize: '0.7rem', color: 'var(--accent-gold)' }}>{c.badge}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Step 4: Company Name & Logo */}
          <div className="form-step">
            <div className="form-step-title">
              <span className="form-step-num">4</span>
              <span>Company / Team Name & Artwork</span>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.35rem' }}>
                Business, Crew, or Team Name:
              </label>
              <input
                type="text"
                value={companyName}
                onChange={(e) => setCompanyName(e.target.value)}
                placeholder="e.g. Apex Electric / KrowN Esports"
                style={{
                  width: '100%',
                  padding: '0.75rem 1rem',
                  borderRadius: '8px',
                  border: '1px solid var(--border)',
                  backgroundColor: 'var(--background)',
                  color: '#fff',
                  fontSize: '0.95rem',
                }}
              />
            </div>

            <label htmlFor="logo-upload" className="upload-dropzone">
              <input
                id="logo-upload"
                type="file"
                accept=".png,.jpg,.jpeg,.svg,.pdf,.ai,.eps"
                onChange={handleFileUpload}
                style={{ display: 'none' }}
              />
              <div className="upload-icon">📁</div>
              <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>
                {uploadedFileName ? 'Change Logo File' : 'Click to Upload Your Logo or Sketch'}
              </div>
              <div className="upload-hint">Accepts AI, EPS, SVG, PDF, PNG, JPG (High Res Recommended)</div>
            </label>

            {uploadedFileName && (
              <div className="file-preview">
                <span style={{ fontWeight: 600 }}>📎 {uploadedFileName}</span>
                <span style={{ color: '#39ff14', fontSize: '0.75rem', fontWeight: 700 }}>Ready for Laser Engraving</span>
              </div>
            )}

            <div style={{ marginTop: '1rem' }}>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '0.35rem' }}>
                Placement or Slogan Notes (Optional):
              </label>
              <textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="e.g. Center circular patch, add est. 2024 underneath, or oval patch shape."
                rows={2}
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '8px',
                  border: '1px solid var(--border)',
                  backgroundColor: 'var(--background)',
                  color: '#fff',
                  fontSize: '0.85rem',
                  resize: 'vertical',
                }}
              />
            </div>
          </div>

          {/* Total Summary */}
          <div className="total-summary-card">
            <div className="summary-row">
              <span>Quantity ({selectedTier.qty} hats @ ${selectedTier.priceEach.toFixed(2)}):</span>
              <span>${selectedTier.total.toFixed(2)}</span>
            </div>
            <div className="summary-row">
              <span>Digital 3D Laser Proof:</span>
              <span style={{ color: '#39ff14', fontWeight: 700 }}>FREE ($50 Value)</span>
            </div>
            <div className="summary-row">
              <span>US Continental Shipping:</span>
              <span style={{ color: '#39ff14', fontWeight: 700 }}>
                {selectedTier.total >= 75 ? 'FREE (Orders $75+)' : '$5.99'}
              </span>
            </div>
            <div className="summary-row total-row">
              <span>Order Total:</span>
              <span style={{ color: 'var(--accent-gold)' }}>${selectedTier.total.toFixed(2)}</span>
            </div>

            <button
              onClick={handleAddToCart}
              className="btn btn-primary"
              style={{
                width: '100%',
                padding: '1rem',
                fontSize: '1.05rem',
                fontWeight: 800,
                marginTop: '1rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
              }}
            >
              {isAdded ? (
                <>✓ Added {selectedTier.qty} Hats to Cart!</>
              ) : (
                <>Add {selectedTier.qty} Custom Hats to Cart • ${selectedTier.total.toFixed(2)}</>
              )}
            </button>

            {isAdded && (
              <div style={{ marginTop: '0.75rem', textAlign: 'center' }}>
                <Link
                  href="/cart"
                  style={{
                    color: 'var(--accent-gold)',
                    fontWeight: 700,
                    textDecoration: 'underline',
                    fontSize: '0.9rem',
                  }}
                >
                  View Cart & Proceed to Checkout →
                </Link>
              </div>
            )}

            <p className="proof-notice">
              🛡️ <strong>Risk-Free Guarantee:</strong> You will receive a photorealistic PDF/PNG proof to review before laser cutting begins. If you are not completely satisfied with the mockup, your order will be refunded 100% immediately.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
