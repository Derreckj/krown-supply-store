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
    const handleColorEvent = (e: Event) => {
      const customEvent = e as CustomEvent<{ color: string }>;
      const color = (customEvent.detail?.color || '').toLowerCase();
      if (!color) return;

      if (color.includes('banner')) {
        const bannerImg = images.find(img => img.includes('display') || img.includes('banner'));
        if (bannerImg) setSelectedImage(bannerImg);
      } else if (color.includes('volcanic') || color.includes('obsidian') || color.includes('battlestation')) {
        const volcanicImg = images.find(img => img.includes('quote-frame') || img.includes('photorealistic') || img.includes('face-desk-mat'));
        if (volcanicImg) setSelectedImage(volcanicImg);
      } else if (color.includes('away') || color.includes('white')) {
        const awayImg = images.find(img => img.includes('away'));
        if (awayImg) setSelectedImage(awayImg);
      } else if (color.includes('home') || color.includes('electric')) {
        const homeImg = images.find(img => img.includes('home'));
        if (homeImg) setSelectedImage(homeImg);
      } else if (color.includes('stealth') || color.includes('black')) {
        const stealthImg = images.find(img => img.includes('stealth'));
        if (stealthImg) setSelectedImage(stealthImg);
      }
    };

    window.addEventListener('krown:color-changed', handleColorEvent);
    return () => window.removeEventListener('krown:color-changed', handleColorEvent);
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
