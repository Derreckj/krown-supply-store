import React from 'react';
import Link from 'next/link';
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { printifyService } from '@/services/printify';
import AddToCartForm from '@/components/product/AddToCartForm';
import ProductImageGallery from '@/components/product/ProductImageGallery';
import ProductCard from '@/components/product/ProductCard';
import { getCatalogPurchaseHold } from '@/config/catalog-holds';
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
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://www.krownsupplyco.com';
  const fullImageUrl = primaryImage.startsWith('http') ? primaryImage : `${siteUrl}${primaryImage}`;
  const description = getCatalogPurchaseHold(product.id)
    ? 'Design reference — ordering paused. Supplier materials, colours, sizes and print placement are being verified before this product can be ordered.'
    : product.description;

  return {
    title: `${product.name} | KrowN Supply Co.`,
    description: description.slice(0, 160),
    openGraph: {
      title: `${product.name} | KrowN Supply Co.`,
      description: description.slice(0, 200),
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
      description: description.slice(0, 200),
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

  const purchaseHold = getCatalogPurchaseHold(product.id);

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

          {purchaseHold && (
            <div className="trust-badges" role="note">
              <div>
                <strong>Design reference — production review</strong>
                <p>These images show the intended design. Supplier materials, colours, sizes and print placement still need verification. Ordering is paused until the finished product can be confirmed.</p>
              </div>
            </div>
          )}
          <div className="product-description" style={{ marginTop: '1.5rem' }}>
            <h3>{purchaseHold ? 'Intended Design & Details' : 'Craftsmanship & Details'}</h3>
            <p>{product.description}</p>
            {product.material && (
              <p style={{ marginTop: '0.5rem' }}><strong>{purchaseHold ? 'Proposed Material:' : 'Material:'}</strong> {product.material}</p>
            )}
            {product.fit && (
              <p style={{ marginTop: '0.25rem' }}><strong>{purchaseHold ? 'Proposed Fit & Sizing:' : 'Fit & Sizing:'}</strong> {product.fit}</p>
            )}
          </div>
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
