"""
Career path prediction using machine learning.
Implements a classification model to predict career paths based on skills.
"""

from typing import List, Dict, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

# Career database with required skills and metadata
CAREER_DATABASE = {
    "Full Stack Developer": {
        "description": "Build and maintain both frontend and backend of web applications",
        "required_skills": ["javascript", "html", "css", "python", "node.js", "react", 
                           "sql", "git", "rest api", "mongodb"],
        "average_salary": "$95,000 - $140,000",
        "growth_rate": "22% (Much faster than average)",
        "category": "Software Development"
    },
    "Data Scientist": {
        "description": "Analyze complex data to help organizations make better decisions",
        "required_skills": ["python", "machine learning", "statistics", "sql", "pandas",
                           "numpy", "data visualization", "r", "scikit-learn", "tensorflow"],
        "average_salary": "$100,000 - $150,000",
        "growth_rate": "36% (Much faster than average)",
        "category": "Data & Analytics"
    },
    "DevOps Engineer": {
        "description": "Bridge development and operations to improve deployment efficiency",
        "required_skills": ["linux", "docker", "kubernetes", "jenkins", "aws", "python",
                           "bash", "ci/cd", "terraform", "monitoring"],
        "average_salary": "$105,000 - $155,000",
        "growth_rate": "25% (Much faster than average)",
        "category": "Infrastructure"
    },
    "Machine Learning Engineer": {
        "description": "Design and implement machine learning applications and systems",
        "required_skills": ["python", "machine learning", "deep learning", "tensorflow",
                           "pytorch", "algorithms", "statistics", "nlp", "computer vision", "cloud"],
        "average_salary": "$115,000 - $175,000",
        "growth_rate": "40% (Much faster than average)",
        "category": "AI & Machine Learning"
    },
    "Frontend Developer": {
        "description": "Create engaging user interfaces for web applications",
        "required_skills": ["javascript", "html", "css", "react", "typescript", "webpack",
                           "git", "responsive design", "sass", "rest api"],
        "average_salary": "$85,000 - $130,000",
        "growth_rate": "20% (Faster than average)",
        "category": "Software Development"
    },
    "Backend Developer": {
        "description": "Build server-side logic and database systems",
        "required_skills": ["python", "java", "sql", "rest api", "microservices", "docker",
                           "mongodb", "redis", "git", "node.js"],
        "average_salary": "$90,000 - $135,000",
        "growth_rate": "22% (Much faster than average)",
        "category": "Software Development"
    },
    "Mobile App Developer": {
        "description": "Create applications for mobile devices",
        "required_skills": ["swift", "kotlin", "react native", "flutter", "mobile ui",
                           "rest api", "git", "firebase", "ios", "android"],
        "average_salary": "$90,000 - $140,000",
        "growth_rate": "24% (Much faster than average)",
        "category": "Software Development"
    },
    "Cloud Architect": {
        "description": "Design and manage cloud computing strategies",
        "required_skills": ["aws", "azure", "cloud architecture", "security", "networking",
                           "docker", "kubernetes", "terraform", "microservices", "ci/cd"],
        "average_salary": "$125,000 - $180,000",
        "growth_rate": "28% (Much faster than average)",
        "category": "Infrastructure"
    },
    "Product Manager": {
        "description": "Guide product development from conception to launch",
        "required_skills": ["product strategy", "agile", "roadmapping", "stakeholder management",
                           "data analysis", "communication", "user research", "jira", "sql", "leadership"],
        "average_salary": "$110,000 - $165,000",
        "growth_rate": "18% (Faster than average)",
        "category": "Product & Management"
    },
    "UX/UI Designer": {
        "description": "Design user experiences and interfaces for digital products",
        "required_skills": ["figma", "user research", "wireframing", "prototyping", "html",
                           "css", "design systems", "usability testing", "adobe xd", "interaction design"],
        "average_salary": "$80,000 - $125,000",
        "growth_rate": "16% (Faster than average)",
        "category": "Design"
    },
    "Data Engineer": {
        "description": "Build and maintain data infrastructure and pipelines",
        "required_skills": ["python", "sql", "etl", "spark", "airflow", "aws", "kafka",
                           "data warehousing", "big data", "hadoop"],
        "average_salary": "$105,000 - $160,000",
        "growth_rate": "33% (Much faster than average)",
        "category": "Data & Analytics"
    },
    "Cybersecurity Analyst": {
        "description": "Protect systems and networks from security threats",
        "required_skills": ["network security", "penetration testing", "security auditing",
                           "firewalls", "encryption", "incident response", "linux", "python", "risk assessment"],
        "average_salary": "$95,000 - $145,000",
        "growth_rate": "35% (Much faster than average)",
        "category": "Security"
    },
    "Business Analyst": {
        "description": "Analyze business processes and recommend improvements",
        "required_skills": ["data analysis", "sql", "excel", "requirements gathering",
                           "process modeling", "communication", "stakeholder management", "agile", "tableau"],
        "average_salary": "$75,000 - $115,000",
        "growth_rate": "14% (Faster than average)",
        "category": "Business & Analytics"
    },
    "AI Research Scientist": {
        "description": "Conduct research in artificial intelligence and develop new AI models",
        "required_skills": ["machine learning", "deep learning", "research", "python",
                           "mathematics", "algorithms", "pytorch", "tensorflow", "nlp", "computer vision"],
        "average_salary": "$130,000 - $200,000",
        "growth_rate": "45% (Much faster than average)",
        "category": "AI & Machine Learning"
    },
    "QA Engineer": {
        "description": "Ensure software quality through testing and automation",
        "required_skills": ["testing", "selenium", "automation", "python", "java",
                           "junit", "jest", "ci/cd", "agile", "bug tracking"],
        "average_salary": "$75,000 - $115,000",
        "growth_rate": "15% (Faster than average)",
        "category": "Quality Assurance"
    }
}


def predict_career_paths(user_skills: List[str], top_k: int = 3) -> List[Dict]:
    """
    Predict top career paths based on user skills.
    
    Args:
        user_skills: List of user's skills
        top_k: Number of top predictions to return
        
    Returns:
        list: Top career predictions with confidence scores
    """
    logger.info(f"Predicting careers for {len(user_skills)} skills")
    
    # Normalize user skills
    user_skills_lower = [skill.lower().strip() for skill in user_skills]
    user_skills_text = " ".join(user_skills_lower)
    
    # Calculate similarity scores for each career
    career_scores = []
    
    for career_title, career_data in CAREER_DATABASE.items():
        # Get required skills for this career
        required_skills = [s.lower() for s in career_data["required_skills"]]
        required_skills_text = " ".join(required_skills)
        
        # Method 1: Jaccard similarity (set-based)
        user_set = set(user_skills_lower)
        required_set = set(required_skills)
        intersection = user_set.intersection(required_set)
        union = user_set.union(required_set)
        jaccard_score = len(intersection) / len(union) if union else 0
        
        # Method 2: TF-IDF cosine similarity
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([user_skills_text, required_skills_text])
        cosine_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Method 3: Skill match percentage
        matches = len(intersection)
        match_percentage = (matches / len(required_set)) * 100 if required_set else 0
        
        # Combined confidence score (weighted average)
        confidence = (jaccard_score * 0.3 + cosine_score * 0.4 + (match_percentage / 100) * 0.3)
        
        career_scores.append({
            "career_title": career_title,
            "confidence": round(confidence, 3),
            "description": career_data["description"],
            "average_salary": career_data["average_salary"],
            "growth_rate": career_data["growth_rate"],
            "required_skills": career_data["required_skills"],
            "skill_match_percentage": round(match_percentage, 1),
            "matched_skills": list(intersection),
            "missing_skills": list(required_set - user_set)
        })
    
    # Sort by confidence and return top K
    career_scores.sort(key=lambda x: x["confidence"], reverse=True)
    top_predictions = career_scores[:top_k]
    
    logger.info(f"Top prediction: {top_predictions[0]['career_title']} "
                f"with {top_predictions[0]['confidence']:.2f} confidence")
    
    return top_predictions


def analyze_skill_gaps(user_skills: List[str], target_career: str) -> Dict:
    """
    Analyze skill gaps for a target career.
    
    Args:
        user_skills: List of user's current skills
        target_career: Target career path
        
    Returns:
        dict: Skill gap analysis
    """
    if target_career not in CAREER_DATABASE:
        raise ValueError(f"Unknown career: {target_career}")
    
    user_skills_lower = set(s.lower().strip() for s in user_skills)
    required_skills = set(s.lower() for s in CAREER_DATABASE[target_career]["required_skills"])
    
    matched_skills = list(user_skills_lower.intersection(required_skills))
    missing_skills = list(required_skills - user_skills_lower)
    
    # Calculate gap percentage
    gap_percentage = (len(missing_skills) / len(required_skills)) * 100 if required_skills else 0
    
    return {
        "missing_skills": missing_skills,
        "matched_skills": matched_skills,
        "partial_skills": [],  # Could be enhanced with fuzzy matching
        "gap_percentage": round(gap_percentage, 1),
        "total_required": len(required_skills),
        "total_matched": len(matched_skills)
    }


def get_all_careers() -> List[str]:
    """Get list of all available careers."""
    return list(CAREER_DATABASE.keys())


def get_career_info(career_title: str) -> Dict:
    """Get detailed information about a career."""
    if career_title not in CAREER_DATABASE:
        raise ValueError(f"Unknown career: {career_title}")
    return CAREER_DATABASE[career_title]
