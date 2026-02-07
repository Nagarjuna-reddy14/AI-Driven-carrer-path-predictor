"""
Firebase initialization and utilities.
Handles Firebase Admin SDK setup and provides helper functions.
"""

import firebase_admin
from firebase_admin import credentials, auth, firestore
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Global Firebase instances
_firebase_app = None
_firestore_client = None


def initialize_firebase():
    """
    Initialize Firebase Admin SDK.
    Should be called once at application startup.
    """
    global _firebase_app, _firestore_client
    
    if _firebase_app is not None:
        logger.warning("Firebase already initialized")
        return
    
    try:
        # Get credentials from settings
        cred_dict = settings.get_firebase_credentials()
        cred = credentials.Certificate(cred_dict)
        
        # Initialize the app
        _firebase_app = firebase_admin.initialize_app(cred)
        _firestore_client = firestore.client()
        
        logger.info("Firebase initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        raise


def get_firestore_client():
    """
    Get Firestore client instance.
    
    Returns:
        firestore.Client: Firestore client
    """
    if _firestore_client is None:
        raise RuntimeError("Firestore not initialized. Call initialize_firebase() first.")
    return _firestore_client


async def verify_firebase_token(token: str) -> dict:
    """
    Verify Firebase authentication token.
    
    Args:
        token: Firebase ID token
        
    Returns:
        dict: Decoded token with user information
        
    Raises:
        ValueError: If token is invalid
    """
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise ValueError(f"Invalid authentication token: {str(e)}")


async def get_user_by_uid(uid: str) -> dict:
    """
    Get user information by UID.
    
    Args:
        uid: Firebase user ID
        
    Returns:
        dict: User information
    """
    try:
        user = auth.get_user(uid)
        return {
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "email_verified": user.email_verified,
            "created_at": user.user_metadata.creation_timestamp
        }
    except Exception as e:
        logger.error(f"Failed to get user: {str(e)}")
        raise ValueError(f"User not found: {str(e)}")
