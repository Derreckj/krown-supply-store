"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { 
  calculateCartDiscount, 
  validateDiscountCode, 
  CartDiscountBreakdown, 
  DiscountCodeConfig,
  isExcludedDiscountItem
} from '@/lib/discounts';

export type CartItem = {
  id: string; // unique ID for cart line item (product + variant + personalization combo)
  productId: string;
  name: string;
  price: number;
  image: string;
  variant: {
    color: string;
    size: string;
  };
  quantity: number;
  personalization?: {
    gamertag?: string;
    playerNumber?: string;
    edition?: string;
    notes?: string;
  };
};

interface CartContextType {
  items: CartItem[];
  addItem: (item: Omit<CartItem, 'id'>) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clearCart: () => void;
  cartTotal: number;
  cartCount: number;
  isCartOpen: boolean;
  setIsCartOpen: (isOpen: boolean) => void;
  // KROWN10 Discount State & Handlers
  appliedDiscountCode: string | null;
  discountConfig: DiscountCodeConfig | null;
  discountBreakdown: CartDiscountBreakdown;
  discountError: string | null;
  applyDiscount: (code: string) => { success: boolean; error?: string };
  removeDiscount: () => void;
}

export const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isMounted, setIsMounted] = useState(false);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [appliedDiscountCode, setAppliedDiscountCode] = useState<string | null>(null);
  const [discountError, setDiscountError] = useState<string | null>(null);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setIsMounted(true);
    const savedCart = localStorage.getItem('krown_supply_cart');
    if (savedCart) {
      try {
        setItems(JSON.parse(savedCart));
      } catch {
        console.error('Failed to parse cart');
      }
    }
    const savedDiscount = localStorage.getItem('krown_supply_discount');
    if (savedDiscount) {
      const validated = validateDiscountCode(savedDiscount);
      if (validated) {
        setAppliedDiscountCode(validated.code);
      }
    }
  }, []);

  useEffect(() => {
    if (isMounted) {
      localStorage.setItem('krown_supply_cart', JSON.stringify(items));
    }
  }, [items, isMounted]);

  useEffect(() => {
    if (isMounted) {
      if (appliedDiscountCode) {
        localStorage.setItem('krown_supply_discount', appliedDiscountCode);
      } else {
        localStorage.removeItem('krown_supply_discount');
      }
    }
  }, [appliedDiscountCode, isMounted]);

  const addItem = (newItem: Omit<CartItem, 'id'>) => {
    setItems(prev => {
      const customKey = newItem.personalization 
        ? `${newItem.personalization.gamertag || ''}-${newItem.personalization.playerNumber || ''}`
        : '';
      const generatedId = `${newItem.productId}-${newItem.variant.color}-${newItem.variant.size}${customKey ? `-${customKey}` : ''}`;
      const existingItemIndex = prev.findIndex(item => item.id === generatedId);

      if (existingItemIndex >= 0) {
        const updated = [...prev];
        updated[existingItemIndex].quantity += newItem.quantity;
        return updated;
      }

      return [...prev, { ...newItem, id: generatedId }];
    });
    setIsCartOpen(true);
  };

  const removeItem = (id: string) => {
    setItems(prev => prev.filter(item => item.id !== id));
  };

  const updateQuantity = (id: string, quantity: number) => {
    if (quantity < 1) return;
    setItems(prev => prev.map(item => 
      item.id === id ? { ...item, quantity } : item
    ));
  };

  const clearCart = () => {
    setItems([]);
    setAppliedDiscountCode(null);
    setDiscountError(null);
  };

  const cartTotal = items.reduce((total, item) => total + (item.price * item.quantity), 0);
  const cartCount = items.reduce((count, item) => count + item.quantity, 0);

  const discountConfig = validateDiscountCode(appliedDiscountCode);
  const discountBreakdown = calculateCartDiscount(items, discountConfig);

  const applyDiscount = (rawCode: string) => {
    const trimmed = (rawCode || '').trim();
    if (!trimmed) {
      return { success: false, error: 'Please enter a discount code.' };
    }

    const validated = validateDiscountCode(trimmed);
    if (!validated) {
      const err = 'Invalid discount code. Enter KROWN10 or KROWN15.';
      setDiscountError(err);
      return { success: false, error: err };
    }

    // Check cart eligibility while preserving custom-hat exclusions.
    const testBreakdown = calculateCartDiscount(items, validated);
    if (testBreakdown.errorMessage) {
      setDiscountError(testBreakdown.errorMessage);
      return { success: false, error: testBreakdown.errorMessage };
    }

    setAppliedDiscountCode(validated.code);
    setDiscountError(null);
    return { success: true };
  };

  const removeDiscount = () => {
    setAppliedDiscountCode(null);
    setDiscountError(null);
  };

  return (
    <CartContext.Provider value={{
      items,
      addItem,
      removeItem,
      updateQuantity,
      clearCart,
      cartTotal,
      cartCount,
      isCartOpen,
      setIsCartOpen,
      appliedDiscountCode,
      discountConfig,
      discountBreakdown,
      discountError,
      applyDiscount,
      removeDiscount
    }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (context === undefined) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
}
