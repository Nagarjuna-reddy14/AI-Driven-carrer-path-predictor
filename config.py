"""
Application configuration settings.
Loads environment variables and provides typed configuration.
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    
    # App settings
    APP_NAME: str = "Career Path Predictor API"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # Firebase settings
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_CLIENT_EMAIL: str
    FIREBASE_CLIENT_ID: str
    FIREBASE_AUTH_URI: str = "https://accounts.google.com/o/oauth2/auth"
    FIREBASE_TOKEN_URI: str = "https://oauth2.googleapis.com/token"
    
    # CORS settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # File upload settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["application/pdf"]
    
    # ML Model settings
    MODEL_PATH: str = "app/ml/models"
    CONFIDENCE_THRESHOLD: float = 0.6
    TOP_K_PREDICTIONS: int = 3
    
    # API Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_firebase_credentials(self) -> dict:
        """
        Get Firebase credentials as a dictionary.
        Properly formats the private key.
        """
        return {
            "type": "service_account",
            "project_id": self.FIREBASE_PROJECT_ID,
            "private_key_id": self.FIREBASE_PRIVATE_KEY_ID,
            "private_key": self.FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
            "client_email": self.FIREBASE_CLIENT_EMAIL,
            "client_id": self.FIREBASE_CLIENT_ID,
            "auth_uri": self.FIREBASE_AUTH_URI,
            "token_uri": self.FIREBASE_TOKEN_URI,
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{self.FIREBASE_CLIENT_EMAIL}"
        }


# Create settings instance
settings = Settings()
