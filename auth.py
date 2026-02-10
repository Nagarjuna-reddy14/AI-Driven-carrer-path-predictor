"""
Authentication API routes.
Handles Firebase token verification and user authentication.
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from app.models.schemas import TokenVerification, UserResponse, ErrorResponse
from app.core.firebase import verify_firebase_token, get_user_by_uid
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


async def get_current_user(authorization: str = Header(None)) -> dict:
    """
    Dependency to get current authenticated user.
    
    Args:
        authorization: Authorization header with Bearer token
        
    Returns:
        dict: Decoded user information
        
    Raises:
        HTTPException: If authentication fails
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization header"
        )
    
    try:
        # Extract token from "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication scheme"
            )
        
        # Verify token
        decoded_token = await verify_firebase_token(token)
        return decoded_token
        
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/verify", response_model=UserResponse)
async def verify_token(token_data: TokenVerification):
    """
    Verify Firebase authentication token.
    
    Args:
        token_data: Token verification request
        
    Returns:
        UserResponse: User information
    """
    try:
        decoded_token = await verify_firebase_token(token_data.token)
        
        # Get full user information
        user_info = await get_user_by_uid(decoded_token['uid'])
        
        return UserResponse(**user_info)
        
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        raise HTTPException(status_code=500, detail="Token verification failed")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """
    Get current authenticated user information.
    
    Args:
        current_user: Current user from dependency
        
    Returns:
        UserResponse: User information
    """
    try:
        user_info = await get_user_by_uid(current_user['uid'])
        return UserResponse(**user_info)
    except Exception as e:
        logger.error(f"Error fetching user info: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch user information")
