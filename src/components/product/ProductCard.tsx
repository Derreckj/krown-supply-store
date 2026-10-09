'use client';

import { useState } from 'react';
import Link from 'next/link';
import './ProductCard.css';

interface ProductCardProps {
  id: string;
  name: string;
  price: number;
  collection: string;
  image: string;
  hoverImage?: string;
  isNew?: boolean;
  isLimited?: boolean;
  customBadge?: string;
}

export default function ProductCard({
  id,
  name,
  price,
  collection,
  image,
  hoverImage,
  isNew,
  isLimited,
  customBadge
}: ProductCardProps) {
  const fallback = '/images/branding/krown-definitive-logo.png';
  const [imgSrc, setImgSrc] = useState<string>(image || fallback);
  const [hoverSrc, setHoverSrc] = useState<string | undefined>(hoverImage);

  return (
    <Link href={`/products/${id}`} className="product-card group">
      <div className="product-image-container">
        {imgSrc ? (
          <>
            <img 
              src={imgSrc} 
              alt={name} 
              className={`product-image-img ${hoverSrc ? 'primary-img' : ''}`}
              onError={() => {
                if (imgSrc !== fallback) {
                  setImgSrc(fallback);
                }
              }}
            />
            {hoverSrc && (
              <img 
                src={hoverSrc} 
                alt={`${name} alternate`} 
                className="product-image-img hover-img" 
                onError={() => {
                  setHoverSrc(undefined);
                }}
              />
            )}
          </>
        ) : (
          <div className="product-image-placeholder">
            <span className="text-muted">KrowN Supply</span>
          </div>
        )}
        
        <div className="product-badges">
          {customBadge ? (
            <span className="badge badge-custom">{customBadge}</span>
          ) : (
            <>
              {isNew && <span className="badge badge-new">New</span>}
              {isLimited && <span className="badge badge-limited">Limited Drop</span>}
            </>
          )}
        </div>
      </div>
      
      <div className="product-details">
        <p className="product-collection">{collection}</p>
        <h3 className="product-name">{name}</h3>
        <p className="product-price">${price.toFixed(2)}</p>
      </div>
    </Link>
  );
}
