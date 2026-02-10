"""
Roadmap API routes.
Handles learning roadmap generation and recommendations.
"""

from fastapi import APIRouter, HTTPException, Depends
from app.api.auth import get_current_user
from app.ml.roadmap_generator import generate_learning_roadmap, get_skill_resources
from app.ml.career_predictor import get_career_info
from app.core.firebase import get_firestore_client
from datetime import datetime
import logging
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate")
async def generate_roadmap(
    career_path: str,
    missing_skills: list[str],
    current_skills: list[str],
    current_user: dict = Depends(get_current_user)
):
    """
    Generate a personalized learning roadmap.
    
    Args:
        career_path: Target career path
        missing_skills: Skills to learn
        current_skills: Skills already known
        current_user: Authenticated user
        
    Returns:
        dict: Complete learning roadmap
    """
    try:
        # Validate career path
        try:
            get_career_info(career_path)
        except ValueError:
            raise HTTPException(status_code=404, detail="Invalid career path")
        
        # Generate roadmap
        roadmap = generate_learning_roadmap(career_path, missing_skills, current_skills)
        
        # Add metadata
        roadmap_id = str(uuid.uuid4())
        result = {
            "roadmap_id": roadmap_id,
            "user_id": current_user['uid'],
            **roadmap,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Save to Firestore
        try:
            db = get_firestore_client()
            doc_ref = db.collection('roadmaps').document(roadmap_id)
            doc_ref.set({
                **result,
                'user_email': current_user.get('email'),
                'created_at': datetime.utcnow()
            })
            logger.info(f"Roadmap saved to Firestore: {roadmap_id}")
        except Exception as e:
            logger.error(f"Failed to save roadmap to Firestore: {str(e)}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Roadmap generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate roadmap")


@router.get("/{roadmap_id}")
async def get_roadmap(
    roadmap_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve a saved roadmap.
    
    Args:
        roadmap_id: Roadmap ID
        current_user: Authenticated user
        
    Returns:
        dict: Roadmap data
    """
    try:
        db = get_firestore_client()
        doc_ref = db.collection('roadmaps').document(roadmap_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Roadmap not found")
        
        roadmap_data = doc.to_dict()
        
        # Verify user owns this roadmap
        if roadmap_data.get('user_id') != current_user['uid']:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return roadmap_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving roadmap: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve roadmap")


@router.get("/user/roadmaps")
async def get_user_roadmaps(current_user: dict = Depends(get_current_user)):
    """
    Get all roadmaps for current user.
    
    Returns:
        dict: User's roadmaps
    """
    try:
        db = get_firestore_client()
        roadmaps_ref = db.collection('roadmaps')
        query = roadmaps_ref.where('user_id', '==', current_user['uid']).order_by('created_at', direction='DESCENDING')
        
        roadmaps = []
        for doc in query.stream():
            data = doc.to_dict()
            roadmaps.append({
                "roadmap_id": doc.id,
                "career_path": data.get('career_path'),
                "timeline": data.get('timeline'),
                "created_at": data.get('created_at')
            })
        
        return {
            "roadmaps": roadmaps,
            "total": len(roadmaps)
        }
        
    except Exception as e:
        logger.error(f"Error retrieving user roadmaps: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve roadmaps")


@router.get("/resources/{skill}")
async def get_resources_for_skill(
    skill: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get learning resources for a specific skill.
    
    Args:
        skill: Skill name
        
    Returns:
        dict: Learning resources
    """
    try:
        resources = get_skill_resources(skill)
        
        return {
            "skill": skill,
            "courses": resources.get('courses', []),
            "projects": resources.get('projects', []),
            "total_resources": len(resources.get('courses', [])) + len(resources.get('projects', []))
        }
        
    except Exception as e:
        logger.error(f"Error getting skill resources: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get resources")


@router.delete("/{roadmap_id}")
async def delete_roadmap(
    roadmap_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a roadmap.
    
    Args:
        roadmap_id: Roadmap ID
        
    Returns:
        dict: Success message
    """
    try:
        db = get_firestore_client()
        doc_ref = db.collection('roadmaps').document(roadmap_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Roadmap not found")
        
        roadmap_data = doc.to_dict()
        
        # Verify user owns this roadmap
        if roadmap_data.get('user_id') != current_user['uid']:
            raise HTTPException(status_code=403, detail="Access denied")
        
        doc_ref.delete()
        
        return {
            "success": True,
            "message": "Roadmap deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting roadmap: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete roadmap")
