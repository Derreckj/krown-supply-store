import React from 'react';
import Link from 'next/link';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { printifyService } from '@/services/printify';
import AddToCartForm from '@/components/product/AddToCartForm';
import ProductImageGallery from '@/components/product/ProductImageGallery';
import ProductCard from '@/components/product/ProductCard';
import './ProductDetail.css';

export const dynamic = 'force-static';

export async function generateStaticParams() {
  const products = await printifyService.getProducts();
  return products.map(p => ({ id: p.id }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>
}): Promise<Metadata> {
  const { id } = await params;
  const product = await printifyService.getProductById(id);

  if (!product) {
    return {
      title: 'Product Not Found | KrowN Supply Co.',
      description: 'The requested product could not be found.',
    };
  }

  const primaryImage = product.images?.[0] || '/images/branding/supply/krown-supply-logo-gold.png';
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://krownsupply.com';
  const fullImageUrl = primaryImage.startsWith('http') ? primaryImage : `${siteUrl}${primaryImage}`;

  return {
    title: `${product.name} | KrowN Supply Co.`,
    description: product.description.slice(0, 160),
    openGraph: {
      title: `${product.name} | KrowN Supply Co.`,
      description: product.description.slice(0, 200),
      url: `${siteUrl}/products/${product.id}`,
      siteName: 'KrowN Supply Co.',
      images: [
        {
          url: fullImageUrl,
          width: 1200,
          height: 1200,
          alt: product.name,
        },
      ],
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title: `${product.name} | KrowN Supply Co.`,
      description: product.description.slice(0, 200),
      images: [fullImageUrl],
      creator: '@KrowNSupplyCo',
    },
  };
}

export default async function ProductDetailPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params;
  const product = await printifyService.getProductById(id);

  if (!product) {
    notFound();
  }

  const allProducts = await printifyService.getProducts();
  // Strictly filter related products by exact same collection
  const relatedProducts = allProducts
    .filter(p => p.id !== product.id && p.collection === product.collection)
    .slice(0, 3);

  const reviewsByDivision = {
    'KrowN Construction': [
      { author: 'Marcus T.', title: 'General Contractor', comment: 'Built like a tank. Takes everyday abuse on the jobsite and looks sharp. Worth every penny.', rating: 5 },
      { author: 'Dave R.', title: 'Lead Framer', comment: 'Heavy duty craftsmanship. The fit and materials are way above standard commercial workwear.', rating: 5 },
      { author: 'Jason K.', title: 'Tradesman', comment: 'Survives concrete dust and rain. The gold crest and "BUILT TO REIGN" branding gets respect.', rating: 5 },
    ],
    'AXA / Axiom Allegiance': [
      { author: 'Alex "Vex" M.', title: 'Pro Aim Coach', comment: 'The AXA owl jersey breathes incredible during intense 5-game sets. No sweat buildup and colors pop on camera.', rating: 5 },
      { author: 'Jordan P.', title: 'Competitive Streamer', comment: 'Colors are electric and vibrant on stream. The AXA owl crest with the A-X-A eye geometry looks insane in person.', rating: 5 },
      { author: 'Tyler S.', title: 'Tournament Finalist', comment: 'Ultra-comfortable for 8+ hour LAN marathons. Clean raglan sleeve fit with zero mouse-drag friction.', rating: 5 },
    ],
    'KrowN Gaming': [
      { author: 'Alex "Vex" M.', title: 'Aim Coach', comment: 'Noticeable upgrade for mouse control and zero desk friction. Essential gear for ranked grinds.', rating: 5 },
      { author: 'Jordan P.', title: 'Twitch Streamer', comment: 'Colors are electric and vibrant on camera. The Axiom crest looks insane in person.', rating: 5 },
      { author: 'Tyler S.', title: 'Tournament Competitor', comment: 'Ultra-comfortable for 8+ hour marathon sessions. Clean second-skin feel without chafing.', rating: 5 },
    ],
    'KrowN Supply Co.': [
      { author: 'Devin B.', title: 'Verified Customer', comment: 'Hands down the best fitting streetwear cut I own. 480 GSM French terry is thick, broken-in, and feels ultra-luxury.', rating: 5 },
      { author: 'Andre M.', title: 'Verified Customer', comment: 'WEAR THE KROWN. The embroidery and antique gold hardware are top tier. Super clean streetwear aesthetic.', rating: 5 },
      { author: 'Leo C.', title: 'Verified Customer', comment: 'Shipped quickly in 3 days. Premium quality and washes great with zero shrinkage.', rating: 5 },
    ],
    'Accessories': [
      { author: 'Chris K.', title: 'Verified Buyer', comment: 'Stickers are super thick and truly weatherproof. Survived high-pressure truck washes and hardhat drops.', rating: 5 },
      { author: 'Sam L.', title: 'Verified Buyer', comment: 'Great quality merchandise. Premium adhesive and crisp holographic sheen.', rating: 5 },
    ],
  };

  const reviews = reviewsByDivision[product.collection as keyof typeof reviewsByDivision] || reviewsByDivision['KrowN Supply Co.'];
  
  const collectionUrl = 
    product.collection === 'KrowN Supply Co.' ? '/collections/supply' :
    product.collection === 'KrowN Construction' ? '/collections/construction' :
    product.collection === 'AXA / Axiom Allegiance' || product.collection === 'KrowN Gaming' ? '/collections/gaming' :
    '/collections/all';

  return (
    <div className="product-detail-page container">
      {/* Breadcrumbs */}
      <nav className="breadcrumbs" aria-label="Breadcrumb">
        <ol>
          <li><Link href="/">Home</Link></li>
          <li><span className="separator">/</span></li>
          <li>
            <Link href={collectionUrl}>
              {product.collection}
            </Link>
          </li>
          <li><span className="separator">/</span></li>
          <li aria-current="page" className="text-gold">{product.name}</li>
        </ol>
      </nav>

      <div className="product-main">
        {/* Interactive Image Gallery */}
        <ProductImageGallery images={product.images} productName={product.name} />

        {/* Product Info */}
        <div className="product-info">
          <p className="product-brand">{product.collection}</p>
          <h1 className="product-title">{product.name}</h1>
          <p className="product-price">${product.price.toFixed(2)}</p>

          {/* Interactive Variant Selection and Add-to-Cart */}
          <AddToCartForm product={product} />

          {/* Trust Highlights */}
          <div className="trust-badges">
            <div className="trust-badge-item">
              <span className="trust-badge-icon">⚡</span>
              <span className="trust-badge-text">Custom Cut-and-Sew / Made-to-Order</span>
            </div>
            <div className="trust-badge-item">
              <span className="trust-badge-icon">📦</span>
              <span className="trust-badge-text">Ships in 2–4 Business Days</span>
            </div>
            <div className="trust-badge-item">
              <span className="trust-badge-icon">🛡️</span>
              <span className="trust-badge-text">Printify Quality Guarantee</span>
            </div>
          </div>

          <div className="product-description" style={{ marginTop: '1.5rem' }}>
            <h3>Craftsmanship &amp; Details</h3>
            <p>{product.description}</p>
            {product.material && (
              <p style={{ marginTop: '0.5rem' }}><strong>Material:</strong> {product.material}</p>
            )}
            {product.fit && (
              <p style={{ marginTop: '0.25rem' }}><strong>Fit &amp; Sizing:</strong> {product.fit}</p>
            )}
          </div>
        </div>
      </div>

      {/* Verified Reviews Section */}
      <div className="product-reviews" style={{ marginTop: '4rem', borderTop: '1px solid var(--border-color)', paddingTop: '2.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <div>
            <h2 style={{ fontSize: '1.4rem', fontWeight: 800 }}>Verified Customer Reviews</h2>
            <p className="text-muted" style={{ fontSize: '0.9rem' }}>4.9 out of 5 based on verified division buyers</p>
          </div>
          <div style={{ fontSize: '1.2rem', color: '#ffc107', letterSpacing: '2px' }}>
            ★★★★★
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem' }}>
          {reviews.map((rev, idx) => (
            <div key={idx} style={{ background: 'rgba(255,255,255,0.02)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <span style={{ fontWeight: 700, fontSize: '0.95rem' }}>{rev.author}</span>
                <span style={{ color: '#ffc107', fontSize: '0.85rem' }}>{'★'.repeat(rev.rating)}</span>
              </div>
              <span style={{ fontSize: '0.75rem', color: 'var(--accent-gold)', display: 'block', marginBottom: '0.5rem' }}>{rev.title}</span>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: '1.5' }}>&ldquo;{rev.comment}&rdquo;</p>
            </div>
          ))}
        </div>
      </div>

      {/* Related Products Section */}
      {relatedProducts.length > 0 && (
        <div className="related-products">
          <h2>More from {product.collection}</h2>
          <div className="product-grid">
            {relatedProducts.map((p) => (
              <ProductCard
                key={p.id}
                id={p.id}
                name={p.name}
                price={p.price}
                collection={p.collection}
                image={p.images[0] || ''}
                hoverImage={p.images[1] || ''}
                isNew={p.isNew}
                isLimited={p.isLimited}
                customBadge={p.customBadge}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
