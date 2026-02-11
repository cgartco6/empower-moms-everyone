export default function Checkout() {
  const [step, setStep] = useState(1);
  const [paymentMethod, setPaymentMethod] = useState('');
  const [orderData, setOrderData] = useState(null);
  
  const handlePlaceOrder = async () => {
    const res = await fetch('/api/v1/checkout', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({cart: cartItems, payment_method: paymentMethod})
    });
    const data = await res.json();
    if (data.payment.redirect_url) {
      window.location.href = data.payment.redirect_url;
    } else if (data.payment.bank_account) {
      setOrderData(data.payment);  // show bank details for EFT
    }
  };
  
  return (
    <div className="checkout">
      {/* Payment method cards: PayFast, Stripe, PayPal, Crypto, FNB EFT, PayShap */}
    </div>
  );
}
