class PricingCalculator:
    """
    Affordable pricing strategy:
    - Free intro courses: always R0 / $0
    - Paid courses: base + per‑module cost
      ZAR: R450 base + R75 per module
      USD: $29 base + $5 per module
    """
    
    ZAR_BASE = 450
    ZAR_PER_MODULE = 75
    USD_BASE = 29
    USD_PER_MODULE = 5
    
    @classmethod
    def calculate(cls, module_count: int, is_free: bool = False):
        if is_free:
            return {"price_zar": 0, "price_usd": 0}
        return {
            "price_zar": round(cls.ZAR_BASE + (module_count * cls.ZAR_PER_MODULE), 2),
            "price_usd": round(cls.USD_BASE + (module_count * cls.USD_PER_MODULE), 2)
        }
