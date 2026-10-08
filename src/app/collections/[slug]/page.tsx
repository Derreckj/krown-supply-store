import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import ProductCard from '@/components/product/ProductCard';
import { printifyService } from '@/services/printify';
import './CollectionPage.css';

export const dynamic = 'force-static';

export async function generateStaticParams() {
  return [
    { slug: 'all' },
    { slug: 'supply' },
    { slug: 'core' },
    { slug: 'gaming' },
    { slug: 'axiom' },
    { slug: 'construction' },
    { slug: 'workwear' },
    { slug: 'accessories' },
  ];
}

export default async function CollectionPage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params;
  const allProducts = await printifyService.getProducts();

  // Filter products based on collection slug with strict brand separation
  const filteredProducts = allProducts.filter((product) => {
    if (slug === 'all') return true;
    if (slug === 'supply' || slug === 'core') return product.collection === 'KrowN Supply Co.';
    if (slug === 'gaming' || slug === 'axiom') return product.collection === 'AXA / Axiom Allegiance' || product.collection === 'KrowN Gaming';
    if (slug === 'construction' || slug === 'workwear') return product.collection === 'KrowN Construction';
    if (slug === 'accessories') return product.collection === 'Accessories' || product.id.includes('sticker');
    return true;
  });

  const metaBySlug: Record<string, { title: string; subtitle: string; banner?: string; badge?: string }> = {
    all: { 
      title: 'The Vault // Complete Catalog', 
      subtitle: 'Explore the complete catalog across all divisions: KrowN Supply Co. luxury streetwear, AXA Axiom Allegiance pro esports, and KrowN Construction LLC workwear.' 
    },
    supply: { 
      title: 'KrowN Supply Co. — Luxury Streetwear', 
      subtitle: 'WEAR THE KROWN. The signature streetwear line: 480 GSM French terry hoodies, tailored sweatpants, kintsugi gold tracksuits, Comfort Colors 1717 tees, and custom Richardson 112 sample headwear.',
      banner: '/images/branding/krown-definitive-logo.png',
      badge: '👑 KrowN Supply Co. • WEAR THE KROWN'
    },
    core: { 
      title: 'KrowN Supply Co. — Luxury Streetwear', 
      subtitle: 'WEAR THE KROWN. The signature streetwear line: 480 GSM French terry hoodies, tailored sweatpants, kintsugi gold tracksuits, Comfort Colors 1717 tees, and custom Richardson 112 sample headwear.',
      banner: '/images/branding/krown-definitive-logo.png',
      badge: '👑 KrowN Supply Co. • WEAR THE KROWN'
    },
    gaming: { 
      title: 'AXA / Axiom Allegiance & KrowN Gaming', 
      subtitle: 'PLAY TO REIGN. The official competitive esports division. Pro league cut-and-sew sublimated jerseys (Home, Away, Championship, Stealth) with custom gamertags, 24oz vibrant gaming shakers, split compression arm sleeves, and panoramic desk mats.',
      banner: '/images/branding/gaming/axiom-owl-display.png',
      badge: '⚡ AXA Esports • PLAY TO REIGN'
    },
    axiom: { 
      title: 'AXA / Axiom Allegiance Esports', 
      subtitle: 'PLAY TO REIGN. The official competitive esports division. Pro league cut-and-sew sublimated jerseys (Home, Away, Championship, Stealth) with custom gamertags, 24oz vibrant gaming shakers, split compression arm sleeves, and panoramic desk mats.',
      banner: '/images/branding/gaming/axiom-owl-display.png',
      badge: '⚡ AXA Esports • PLAY TO REIGN'
    },
    construction: { 
      title: 'KROWN CONSTRUCTION LLC', 
      subtitle: 'BUILT TO REIGN. Authentic jobsite gear: Richardson 112 leather patch snapbacks, 20oz and 32oz vacuum jobsite tumblers, heavy ribbed beanies, work shirts, and weatherproof hardhat decals.',
      banner: '/images/branding/construction/KC.jpg',
      badge: '🔨 KROWN CONSTRUCTION LLC • BUILT TO REIGN'
    },
    workwear: { 
      title: 'KROWN CONSTRUCTION LLC WORKWEAR', 
      subtitle: 'BUILT TO REIGN. Authentic jobsite workwear engineered for endurance, safety, and high mobility on the jobsite.',
      banner: '/images/branding/construction/KC.jpg',
      badge: '🔨 KROWN CONSTRUCTION LLC • BUILT TO REIGN'
    },
    accessories: { 
      title: 'Accessories & Weatherproof Decals', 
      subtitle: 'Heavyweight UV-laminated vinyl stickers, gear, and everyday carry across the KrowN divisions.',
      badge: '★ Accessories & Everyday Carry'
    },
  };

  const currentMeta = metaBySlug[slug] || {
    title: slug.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase()),
    subtitle: 'WEAR THE KROWN. BUILT TO REIGN. PLAY TO REIGN.',
  };

  return (
    <div className="collection-page container">
      {currentMeta.banner && (
        <div className="collection-banner-container">
          <div className="collection-banner-wrap">
            <Image 
              src={currentMeta.banner} 
              alt={currentMeta.title} 
              width={1008} 
              height={576}
              priority
              className="collection-banner-img"
              sizes="(max-width: 640px) 100vw, (max-width: 1152px) 95vw, 1152px"
            />
          </div>
        </div>
      )}

      <header className="collection-header">
        {currentMeta.badge && <span className="collection-badge">{currentMeta.badge}</span>}
        <h1>{currentMeta.title}</h1>
        <p className="collection-subtitle">{currentMeta.subtitle}</p>
      </header>

      <div className="collection-filters">
        <div className="collection-tabs">
          <Link href="/collections/all" className={`collection-tab ${slug === 'all' ? 'active' : ''}`}>The Vault // All</Link>
          <Link href="/collections/supply" className={`collection-tab ${slug === 'supply' || slug === 'core' ? 'active' : ''}`}>KrowN Supply Co.</Link>
          <Link href="/collections/gaming" className={`collection-tab ${slug === 'gaming' || slug === 'axiom' ? 'active' : ''}`}>AXA Esports</Link>
          <Link href="/collections/construction" className={`collection-tab ${slug === 'construction' || slug === 'workwear' ? 'active' : ''}`}>KrowN Construction</Link>
          <Link href="/collections/accessories" className={`collection-tab ${slug === 'accessories' ? 'active' : ''}`}>Accessories</Link>
        </div>
        <span className="text-muted" style={{ fontSize: '0.875rem', marginTop: '1rem', display: 'block' }}>
          Showing {filteredProducts.length} {filteredProducts.length === 1 ? 'item' : 'items'}
        </span>
      </div>

      {filteredProducts.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '3rem 0' }}>
          <p className="text-muted">No items in this collection at the moment. Check back soon for the next drop.</p>
        </div>
      ) : (
        <div className="product-grid">
          {filteredProducts.map((product) => (
            <ProductCard
              key={product.id}
              id={product.id}
              name={product.name}
              price={product.price}
              collection={product.collection}
              image={product.images[0] || ''}
              hoverImage={product.images[1] || ''}
              isNew={product.isNew}
              isLimited={product.isLimited}
              customBadge={product.customBadge}
            />
          ))}
        </div>
      )}
    </div>
  );
}
