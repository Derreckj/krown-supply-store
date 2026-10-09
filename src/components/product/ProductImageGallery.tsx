"use client";

import React, { useState } from 'react';

interface ProductImageGalleryProps {
  images: string[];
  productName: string;
}

export default function ProductImageGallery({ images, productName }: ProductImageGalleryProps) {
  const fallback = '/images/branding/krown-definitive-logo.png';
  const [selectedImage, setSelectedImage] = useState<string>(images[0] || fallback);

  return (
    <div className="product-gallery">
      <div className="main-image-placeholder">
        {selectedImage ? (
          <img 
            src={selectedImage} 
            alt={productName} 
            className="product-detail-hero-img" 
            onError={() => {
              if (selectedImage !== fallback) setSelectedImage(fallback);
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
                onError={(e) => {
                  (e.target as HTMLImageElement).src = fallback;
                }}
              />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
