"""
User profile API routes.
Handles user profile management and data storage.
"""

from fastapi import APIRouter, HTTPException, Depends
from app.api.auth import get_current_user
from app.models.schemas import UserProfileInput
from app.core.firebase import get_firestore_client
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/profile")
async def save_user_profile(
    profile: UserProfileInput,
    current_user: dict = Depends(get_current_user)
):
    """
    Save or update user profile.
    
    Args:
        profile: User profile data
        current_user: Authenticated user
        
    Returns:
        dict: Success message
    """
    try:
        db = get_firestore_client()
        user_ref = db.collection('users').document(current_user['uid'])
        
        profile_data = {
            "education": profile.education,
            "skills": profile.skills,
            "interests": profile.interests,
            "experience_years": profile.experience_years,
            "updated_at": datetime.utcnow(),
            "email": current_user.get('email')
        }
        
        # Check if profile exists
        doc = user_ref.get()
        if doc.exists:
            user_ref.update(profile_data)
            message = "Profile updated successfully"
        else:
            profile_data['created_at'] = datetime.utcnow()
            user_ref.set(profile_data)
            message = "Profile created successfully"
        
        logger.info(f"Profile saved for user {current_user['uid']}")
        
        return {
            "success": True,
            "message": message,
            "user_id": current_user['uid']
        }
        
    except Exception as e:
        logger.error(f"Error saving profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to save profile")


@router.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Get user profile.
    
    Returns:
        dict: User profile data
    """
    try:
        db = get_firestore_client()
        user_ref = db.collection('users').document(current_user['uid'])
        doc = user_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        profile_data = doc.to_dict()
        
        return {
            "user_id": current_user['uid'],
            "email": current_user.get('email'),
            **profile_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve profile")


@router.get("/analyses")
async def get_user_analyses(current_user: dict = Depends(get_current_user)):
    """
    Get all analyses for current user.
    
    Returns:
        dict: User's analyses
    """
    try:
        db = get_firestore_client()
        analyses_ref = db.collection('analyses')
        query = analyses_ref.where('user_id', '==', current_user['uid']).order_by('analyzed_at', direction='DESCENDING')
        
        analyses = []
        for doc in query.stream():
            data = doc.to_dict()
            analyses.append({
                "analysis_id": doc.id,
                "top_career": data.get('top_career', {}).get('title'),
                "confidence": data.get('top_career', {}).get('confidence'),
                "analyzed_at": data.get('analyzed_at'),
                "total_predictions": len(data.get('predictions', []))
            })
        
        return {
            "analyses": analyses,
            "total": len(analyses)
        }
        
    except Exception as e:
        logger.error(f"Error retrieving analyses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analyses")


@router.get("/analysis/{analysis_id}")
async def get_analysis(
    analysis_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific analysis.
    
    Args:
        analysis_id: Analysis ID
        
    Returns:
        dict: Analysis data
    """
    try:
        db = get_firestore_client()
        doc_ref = db.collection('analyses').document(analysis_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        analysis_data = doc.to_dict()
        
        # Verify user owns this analysis
        if analysis_data.get('user_id') != current_user['uid']:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return analysis_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve analysis")


@router.delete("/profile")
async def delete_user_profile(current_user: dict = Depends(get_current_user)):
    """
    Delete user profile and all associated data.
    
    Returns:
        dict: Success message
    """
    try:
        db = get_firestore_client()
        
        # Delete user profile
        user_ref = db.collection('users').document(current_user['uid'])
        user_ref.delete()
        
        # Delete user's analyses
        analyses_ref = db.collection('analyses')
        query = analyses_ref.where('user_id', '==', current_user['uid'])
        for doc in query.stream():
            doc.reference.delete()
        
        # Delete user's roadmaps
        roadmaps_ref = db.collection('roadmaps')
        query = roadmaps_ref.where('user_id', '==', current_user['uid'])
        for doc in query.stream():
            doc.reference.delete()
        
        logger.info(f"Deleted all data for user {current_user['uid']}")
        
        return {
            "success": True,
            "message": "Profile and all associated data deleted successfully"
        }
        
    except Exception as e:
        logger.error(f"Error deleting profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete profile")
