import React from 'react';
import { printifyService } from '@/services/printify';
import SearchClient from './SearchClient';

export const dynamic = 'force-static';

export const metadata = {
  title: 'Search Catalog | KrowN Supply Co.',
  description: 'Search premium streetwear, construction workwear, and Axiom Allegiance gaming gear.',
};

export default async function SearchPage() {
  const products = await printifyService.getProducts();

  return <SearchClient initialProducts={products} />;
}
