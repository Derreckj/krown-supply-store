"use client";

import React, { useState, useEffect } from 'react';

interface ProductImageGalleryProps {
  images: string[];
  productName: string;
}

export default function ProductImageGallery({ images, productName }: ProductImageGalleryProps) {
  const [selectedImage, setSelectedImage] = useState<string>(images[0] || '');

  useEffect(() => {
    setSelectedImage(images[0] || '');
  }, [images]);

  useEffect(() => {
    const handleVariantSync = (colorStr: string, sizeStr: string = '') => {
      const color = colorStr.toLowerCase();
      const size = sizeStr.toLowerCase();

      // Shaker specific precision matching
      const hasSteel = size.includes('steel') || size.includes('insulated');
      const isStealth = color.includes('stealth');
      const isSignature = color.includes('signature') || color.includes('lime') || color.includes('purple');

      if (isStealth && hasSteel) {
        const img = images.find(i => i.includes('stealth-steel'));
        if (img) { setSelectedImage(img); return; }
      } else if (isStealth && (size.includes('tritan') || size.includes('24'))) {
        const img = images.find(i => i.includes('stealth-tritan'));
        if (img) { setSelectedImage(img); return; }
      } else if (isSignature && hasSteel) {
        const img = images.find(i => i.includes('signature-steel'));
        if (img) { setSelectedImage(img); return; }
      } else if (isSignature && (size.includes('tritan') || size.includes('24'))) {
        const img = images.find(i => i.includes('signature-tritan'));
        if (img) { setSelectedImage(img); return; }
      }

      // Headwear specific matching
      if (color.includes('charcoal')) {
        const charcoalImg = images.find(img => img.includes('charcoal'));
        if (charcoalImg) { setSelectedImage(charcoalImg); return; }
      } else if (color.includes('purple')) {
        const purpleImg = images.find(img => img.includes('purple'));
        if (purpleImg) { setSelectedImage(purpleImg); return; }
      } else if (color.includes('lime') || color.includes('green')) {
        const limeImg = images.find(img => img.includes('lime'));
        if (limeImg) { setSelectedImage(limeImg); return; }
      } else if (color.includes('solid') || color.includes('black')) {
        const blackImg = images.find(img => img.includes('black'));
        if (blackImg) { setSelectedImage(blackImg); return; }
      }

      // General color mappings
      if (color.includes('banner')) {
        const bannerImg = images.find(img => img.includes('display') || img.includes('banner'));
        if (bannerImg) setSelectedImage(bannerImg);
      } else if (color.includes('volcanic') || color.includes('battlestation')) {
        const volcanicImg = images.find(img => img.includes('quote-frame') || img.includes('photorealistic') || img.includes('face-desk-mat'));
        if (volcanicImg) setSelectedImage(volcanicImg);
      } else if (color.includes('away') || color.includes('white')) {
        const awayImg = images.find(img => img.includes('away'));
        if (awayImg) setSelectedImage(awayImg);
      } else if (color.includes('home') || color.includes('electric')) {
        const homeImg = images.find(img => img.includes('home'));
        if (homeImg) setSelectedImage(homeImg);
      } else if (color.includes('stealth') || color.includes('obsidian')) {
        const stealthImg = images.find(img => img.includes('stealth'));
        if (stealthImg) setSelectedImage(stealthImg);
      } else if (color.includes('signature') || color.includes('lime')) {
        const sigImg = images.find(img => img.includes('signature'));
        if (sigImg) setSelectedImage(sigImg);
      }
    };

    const handleColorEvent = (e: Event) => {
      const customEvent = e as CustomEvent<{ color: string }>;
      handleVariantSync(customEvent.detail?.color || '');
    };

    const handleVariantEvent = (e: Event) => {
      const customEvent = e as CustomEvent<{ color: string; size: string }>;
      handleVariantSync(customEvent.detail?.color || '', customEvent.detail?.size || '');
    };

    window.addEventListener('krown:color-changed', handleColorEvent);
    window.addEventListener('krown:variant-changed', handleVariantEvent);
    return () => {
      window.removeEventListener('krown:color-changed', handleColorEvent);
      window.removeEventListener('krown:variant-changed', handleVariantEvent);
    };
  }, [images]);

  return (
    <div className="product-gallery">
      <div className="main-image-placeholder">
        {selectedImage ? (
          <img 
            src={selectedImage} 
            alt={productName} 
            className="product-detail-hero-img" 
            loading="eager"
            onError={() => {
              if (selectedImage !== images[0] && images[0]) {
                setSelectedImage(images[0]);
              }
            }}
          />
        ) : (
          <span className="text-muted" style={{ textAlign: 'center', padding: '1rem' }}>
            👑 {productName}
          </span>
        )}
      </div>

      {images.length > 1 && (
        <div className="thumbnail-list">
          {images.map((img, idx) => (
            <button
              type="button"
              key={idx}
              className={`thumbnail-placeholder ${selectedImage === img ? 'thumbnail-active' : ''}`}
              onClick={() => setSelectedImage(img)}
              style={{ padding: '0.25rem', overflow: 'hidden' }}
              aria-label={`View image ${idx + 1}`}
            >
              <img 
                src={img} 
                alt={`${productName} thumbnail ${idx + 1}`} 
                style={{ width: '100%', height: '100%', objectFit: 'contain' }}
                loading="eager"
                onError={(e) => {
                  const parent = (e.target as HTMLElement).parentElement;
                  if (parent) parent.style.display = 'none';
                }}
              />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
