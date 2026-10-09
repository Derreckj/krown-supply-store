"use client";

import React, { useState } from 'react';

interface ProductImageGalleryProps {
  images: string[];
  productName: string;
}

export default function ProductImageGallery({ images, productName }: ProductImageGalleryProps) {
  const [selectedImage, setSelectedImage] = useState<string>(images[0] || '');

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
