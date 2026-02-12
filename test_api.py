"""
Backend API tests.
Run with: pytest tests/test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()


class TestSkillExtraction:
    """Test skill extraction functionality."""
    
    def test_extract_skills_from_text(self):
        """Test skill extraction from sample text."""
        from app.ml.skill_extractor import extract_skills_from_text
        
        text = """
        I am a software developer with 5 years of experience in Python, JavaScript, 
        and React. I have worked with machine learning, TensorFlow, and data analysis.
        """
        
        result = extract_skills_from_text(text)
        
        assert "skills" in result
        assert "confidence" in result
        assert isinstance(result["skills"], list)
        assert len(result["skills"]) > 0
        assert "python" in result["skills"]
    
    def test_empty_text_extraction(self):
        """Test extraction with empty text."""
        from app.ml.skill_extractor import extract_skills_from_text
        
        result = extract_skills_from_text("")
        
        assert result["total_skills_found"] == 0


class TestCareerPrediction:
    """Test career prediction functionality."""
    
    def test_predict_careers(self):
        """Test career prediction with sample skills."""
        from app.ml.career_predictor import predict_career_paths
        
        skills = ["python", "machine learning", "tensorflow", "data analysis"]
        predictions = predict_career_paths(skills, top_k=3)
        
        assert len(predictions) == 3
        assert all("career_title" in p for p in predictions)
        assert all("confidence" in p for p in predictions)
        assert all(0 <= p["confidence"] <= 1 for p in predictions)
    
    def test_skill_gap_analysis(self):
        """Test skill gap analysis."""
        from app.ml.career_predictor import analyze_skill_gaps
        
        user_skills = ["python", "sql", "html"]
        gaps = analyze_skill_gaps(user_skills, "Full Stack Developer")
        
        assert "missing_skills" in gaps
        assert "matched_skills" in gaps
        assert "gap_percentage" in gaps


class TestRoadmapGeneration:
    """Test roadmap generation functionality."""
    
    def test_generate_roadmap(self):
        """Test roadmap generation."""
        from app.ml.roadmap_generator import generate_learning_roadmap
        
        roadmap = generate_learning_roadmap(
            career_path="Full Stack Developer",
            missing_skills=["react", "node.js", "docker"],
            current_skills=["python", "sql"]
        )
        
        assert "phases" in roadmap
        assert "skills_to_learn" in roadmap
        assert "timeline" in roadmap
        assert len(roadmap["phases"]) > 0


class TestModels:
    """Test Pydantic models."""
    
    def test_user_profile_validation(self):
        """Test user profile validation."""
        from app.models.schemas import UserProfileInput
        
        # Valid profile
        profile = UserProfileInput(
            education="B.S. Computer Science",
            skills=["python", "java"],
            interests=["AI", "Web Development"],
            experience_years=3
        )
        
        assert profile.education == "B.S. Computer Science"
        assert len(profile.skills) == 2
    
    def test_invalid_profile(self):
        """Test invalid profile raises error."""
        from app.models.schemas import UserProfileInput
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            UserProfileInput(
                education="",  # Empty education
                skills=[],  # Empty skills
                interests=[],  # Empty interests
            )


# Run tests with:
# pytest tests/test_api.py -v --cov=app
