import { useState, useEffect } from 'react';
import { useCart } from '../../context/CartContext';
import CartItem from './CartItem';

export default function Cart() {
  const { items, total, updateQuantity, removeItem } = useCart();
  
  return (
    <div className="cart-container">
      <h2>Your Learning Cart</h2>
      {items.length === 0 ? (
        <p>Your cart is empty. <Link to="/courses">Browse courses</Link></p>
      ) : (
        <>
          {items.map(item => <CartItem key={item.id} item={item} 
            onUpdate={updateQuantity} onRemove={removeItem} />)}
          <div className="cart-summary">
            <span>Total: R{total}</span>
            <Link to="/checkout" className="btn-checkout">Proceed to Checkout</Link>
          </div>
        </>
      )}
    </div>
  );
}
