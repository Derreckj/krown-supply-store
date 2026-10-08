"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

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
}

export const CartContext = createContext<CartContextType | undefined>(undefined);

export function CartProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);
  const [isMounted, setIsMounted] = useState(false);
  const [isCartOpen, setIsCartOpen] = useState(false);

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
  }, []);

  useEffect(() => {
    if (isMounted) {
      localStorage.setItem('krown_supply_cart', JSON.stringify(items));
    }
  }, [items, isMounted]);

  const addItem = (newItem: Omit<CartItem, 'id'>) => {
    setItems(prev => {
      // Build unique identifier that incorporates gamertag and playerNumber so custom items don't collide or stack
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
    // Open cart drawer smoothly upon adding an item
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

  const clearCart = () => setItems([]);

  const cartTotal = items.reduce((total, item) => total + (item.price * item.quantity), 0);
  const cartCount = items.reduce((count, item) => count + item.quantity, 0);

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
      setIsCartOpen
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
