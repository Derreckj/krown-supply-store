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
    const handleVariantSync = (colorStr: string, sizeStr: string = '', explicitImg?: string) => {
      if (explicitImg) {
        setSelectedImage(explicitImg);
        return;
      }

      const color = colorStr.toLowerCase();
      const size = sizeStr.toLowerCase();

      // Richardson 112 Hat Matching
      if (color.includes('charcoal')) {
        const charcoalImg = images.find(img => img.includes('charcoal'));
        if (charcoalImg) { setSelectedImage(charcoalImg); return; }
      }
      if (color.includes('heather') || (color.includes('grey') && color.includes('black'))) {
        const greyImg = images.find(img => img.includes('heather-grey') || (img.includes('grey') && img.includes('112')));
        if (greyImg) { setSelectedImage(greyImg); return; }
      }
      if (color.includes('obsidian') && color.includes('black')) {
        const obsImg = images.find(img => img.includes('obsidian-black') || img.includes('raw-black'));
        if (obsImg) { setSelectedImage(obsImg); return; }
      }

      // Work Shirt Matching
      if (color.includes('heather') || color.includes('steel grey')) {
        const greyFront = images.find(img => img.includes('grey-front'));
        if (greyFront) { setSelectedImage(greyFront); return; }
      }
      if (color.includes('obsidian') && (color.includes('black') || color.includes('crest'))) {
        const blkFront = images.find(img => img.includes('black-front'));
        if (blkFront) { setSelectedImage(blkFront); return; }
      }
      if (color.includes('charcoal') || color.includes('purple & lime')) {
        const chrBack = images.find(img => img.includes('charcoal-back'));
        if (chrBack) { setSelectedImage(chrBack); return; }
      }

      // Shakers Matching
      const isSteel = size.includes('steel') || size.includes('insulated');
      if (color.includes('high-vis') || color.includes('safety gold')) {
        const img = images.find(i => i.includes(isSteel ? 'highvis-steel' : 'highvis-tritan'));
        if (img) { setSelectedImage(img); return; }
      }
      if (color.includes('steel core') || color.includes('concrete')) {
        const img = images.find(i => i.includes(isSteel ? 'steelcore-steel' : 'steelcore-tritan'));
        if (img) { setSelectedImage(img); return; }
      }
      if (color.includes('jobsite lime')) {
        const img = images.find(i => i.includes(isSteel ? 'jobsite-steel' : 'jobsite-tritan'));
        if (img) { setSelectedImage(img); return; }
      }
      if (color.includes('obsidian') && color.includes('gold')) {
        const img = images.find(i => i.includes(isSteel ? 'krown-shaker-obsidian-steel' : 'krown-shaker-obsidian-tritan'));
        if (img) { setSelectedImage(img); return; }
      }
      if (color.includes('smoke') || color.includes('frosted smoke')) {
        const img = images.find(i => i.includes(isSteel ? 'smoke-steel' : 'smoke-tritan'));
        if (img) { setSelectedImage(img); return; }
      }
      if (color.includes('brushed') || color.includes('raw brushed')) {
        const img = images.find(i => i.includes(isSteel ? 'brushed-steel' : 'brushed-tritan'));
        if (img) { setSelectedImage(img); return; }
      }

      // Axiom Shaker specific precision matching
      const isStealth = color.includes('stealth');
      const isSignature = color.includes('signature') || color.includes('lime') || color.includes('purple');

      if (isStealth && isSteel) {
        const img = images.find(i => i.includes('stealth-steel'));
        if (img) { setSelectedImage(img); return; }
      } else if (isStealth) {
        const img = images.find(i => i.includes('stealth-tritan'));
        if (img) { setSelectedImage(img); return; }
      } else if (isSignature && isSteel) {
        const img = images.find(i => i.includes('signature-steel'));
        if (img) { setSelectedImage(img); return; }
      } else if (isSignature) {
        const img = images.find(i => i.includes('signature-tritan'));
        if (img) { setSelectedImage(img); return; }
      }

      // General color mappings
      if (color.includes('away') || color.includes('white')) {
        const awayImg = images.find(img => img.includes('away'));
        if (awayImg) { setSelectedImage(awayImg); return; }
      } else if (color.includes('home') || color.includes('electric')) {
        const homeImg = images.find(img => img.includes('home'));
        if (homeImg) { setSelectedImage(homeImg); return; }
      } else if (color.includes('charcoal')) {
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
    };

    const handleColorEvent = (e: Event) => {
      const customEvent = e as CustomEvent<{ color: string; image?: string }>;
      handleVariantSync(customEvent.detail?.color || '', '', customEvent.detail?.image);
    };

    const handleVariantEvent = (e: Event) => {
      const customEvent = e as CustomEvent<{ color: string; size: string; image?: string }>;
      handleVariantSync(customEvent.detail?.color || '', customEvent.detail?.size || '', customEvent.detail?.image);
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
