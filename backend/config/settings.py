# backend/config/settings.py
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4"
    TEMPERATURE: float = 0.7

    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost/empower"

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379"

    # Payment Gateways
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    PAYFAST_MERCHANT_ID: Optional[str] = None
    PAYFAST_MERCHANT_KEY: Optional[str] = None
    PAYFAST_URL: str = "https://sandbox.payfast.co.za/eng/process"
    PAYFAST_RETURN_URL: str = "https://yourapp.com/payment/success"
    PAYFAST_CANCEL_URL: str = "https://yourapp.com/payment/cancel"
    PAYFAST_NOTIFY_URL: str = "https://yourapp.com/payment/webhook"
    COINPAYMENTS_PUBLIC_KEY: Optional[str] = None
    COINPAYMENTS_PRIVATE_KEY: Optional[str] = None
    COINPAYMENTS_IPN_URL: str = "https://yourapp.com/payment/crypto-ipn"

    # Social Media API Tokens
    TIKTOK_ACCESS_TOKEN: Optional[str] = None
    FACEBOOK_ACCESS_TOKEN: Optional[str] = None
    INSTAGRAM_ACCESS_TOKEN: Optional[str] = None
    TWITTER_API_KEY: Optional[str] = None
    TWITTER_API_SECRET: Optional[str] = None
    YOUTUBE_API_KEY: Optional[str] = None
    LINKEDIN_ACCESS_TOKEN: Optional[str] = None

    # Image Generation
    IMAGE_PROVIDER: str = "dalle"

    class Config:
        env_file = ".env"

settings = Settings()
