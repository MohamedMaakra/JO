import React, { createContext, useState } from "react";
import { v4 as uuidv4 } from "uuid";

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState([]);
  const [reservations, setReservations] = useState([]);

  const addToCart = (offer) => {
    setCart([...cart, { ...offer, cartId: uuidv4() }]);
  };

  const removeFromCart = (cartId) => {
    setCart(cart.filter((item) => item.cartId !== cartId));
  };

  const clearCart = () => {
    setCart([]);
  };

  const addReservation = (reservation) => {
    setReservations([...reservations, reservation]);
  };

  return (
    <CartContext.Provider value={{ cart, addToCart, removeFromCart, clearCart, reservations, addReservation }}>
      {children}
    </CartContext.Provider>
  );
};
