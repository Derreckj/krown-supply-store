"use client";

import React, { ReactNode } from 'react';
import { CartProvider } from '@/context/CartContext';

export default function ClientProviders({ children }: { children: ReactNode }) {
  return (
    <CartProvider>
      {children}
    </CartProvider>
  );
}
