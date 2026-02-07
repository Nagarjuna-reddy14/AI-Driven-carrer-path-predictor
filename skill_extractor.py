"""
NLP-based skill extraction from text and resumes.
Uses spaCy for entity recognition and custom pattern matching.
"""

import spacy
from typing import List, Dict, Set
import re
import logging

logger = logging.getLogger(__name__)

# Global spaCy model
_nlp = None

# Comprehensive skill database organized by category
SKILL_DATABASE = {
    "programming": [
        "python", "javascript", "java", "c++", "c#", "ruby", "php", "swift",
        "kotlin", "go", "rust", "typescript", "r", "matlab", "scala", "perl"
    ],
    "web_development": [
        "html", "css", "react", "angular", "vue", "node.js", "express",
        "django", "flask", "fastapi", "spring boot", "asp.net", "jquery",
        "webpack", "babel", "sass", "less", "bootstrap", "tailwind css"
    ],
    "mobile_development": [
        "react native", "flutter", "android", "ios", "swift", "kotlin",
        "xamarin", "ionic", "cordova"
    ],
    "database": [
        "sql", "mysql", "postgresql", "mongodb", "redis", "oracle",
        "sql server", "cassandra", "dynamodb", "elasticsearch", "neo4j"
    ],
    "cloud": [
        "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
        "jenkins", "terraform", "ansible", "cloudformation", "heroku"
    ],
    "data_science": [
        "machine learning", "deep learning", "tensorflow", "pytorch",
        "scikit-learn", "pandas", "numpy", "data analysis", "statistics",
        "tableau", "power bi", "jupyter", "r studio"
    ],
    "ai_ml": [
        "artificial intelligence", "nlp", "computer vision", "neural networks",
        "reinforcement learning", "keras", "opencv", "hugging face"
    ],
    "devops": [
        "ci/cd", "git", "github", "gitlab", "bitbucket", "linux",
        "bash", "powershell", "monitoring", "prometheus", "grafana"
    ],
    "soft_skills": [
        "leadership", "communication", "teamwork", "problem solving",
        "critical thinking", "project management", "agile", "scrum",
        "time management", "collaboration"
    ],
    "tools": [
        "jira", "confluence", "slack", "vs code", "intellij", "eclipse",
        "postman", "figma", "adobe xd", "photoshop", "illustrator"
    ],
    "testing": [
        "unit testing", "integration testing", "selenium", "jest",
        "pytest", "junit", "cypress", "testng", "qa", "quality assurance"
    ],
    "security": [
        "cybersecurity", "penetration testing", "encryption", "oauth",
        "jwt", "ssl", "firewall", "security auditing"
    ]
}

# Flatten skill database for quick lookup
ALL_SKILLS = set()
for category, skills in SKILL_DATABASE.items():
    ALL_SKILLS.update(skills)


def load_nlp_model():
    """
    Load spaCy NLP model.
    Downloads if not present.
    """
    global _nlp
    
    if _nlp is not None:
        return _nlp
    
    try:
        _nlp = spacy.load("en_core_web_lg")
        logger.info("spaCy model loaded successfully")
    except OSError:
        logger.warning("spaCy model not found. Downloading...")
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_lg"])
        _nlp = spacy.load("en_core_web_lg")
    
    return _nlp


def extract_skills_from_text(text: str) -> Dict[str, any]:
    """
    Extract skills from text using NLP and pattern matching.
    
    Args:
        text: Input text (resume, profile, etc.)
        
    Returns:
        dict: Extracted skills with categories and confidence
    """
    nlp = load_nlp_model()
    
    # Normalize text
    text_lower = text.lower()
    
    # Extract skills using multiple methods
    extracted_skills = set()
    skill_categories = {category: [] for category in SKILL_DATABASE.keys()}
    
    # Method 1: Direct pattern matching
    for category, skills in SKILL_DATABASE.items():
        for skill in skills:
            # Use word boundaries for exact matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                extracted_skills.add(skill)
                skill_categories[category].append(skill)
    
    # Method 2: NLP entity recognition for technical terms
    doc = nlp(text)
    
    # Extract noun chunks that might be skills
    for chunk in doc.noun_chunks:
        chunk_text = chunk.text.lower()
        if chunk_text in ALL_SKILLS:
            extracted_skills.add(chunk_text)
            for category, skills in SKILL_DATABASE.items():
                if chunk_text in skills:
                    skill_categories[category].append(chunk_text)
    
    # Method 3: Custom patterns for common skill formats
    # Match patterns like "experience with X", "proficient in Y"
    skill_patterns = [
        r'experience (?:with|in) ([\w\s.+#-]+)',
        r'proficient in ([\w\s.+#-]+)',
        r'skilled in ([\w\s.+#-]+)',
        r'knowledge of ([\w\s.+#-]+)',
        r'expertise in ([\w\s.+#-]+)'
    ]
    
    for pattern in skill_patterns:
        matches = re.finditer(pattern, text_lower)
        for match in matches:
            potential_skill = match.group(1).strip()
            if potential_skill in ALL_SKILLS:
                extracted_skills.add(potential_skill)
                for category, skills in SKILL_DATABASE.items():
                    if potential_skill in skills:
                        skill_categories[category].append(potential_skill)
    
    # Remove empty categories
    skill_categories = {k: list(set(v)) for k, v in skill_categories.items() if v}
    
    # Calculate confidence based on text length and skills found
    text_length = len(text.split())
    skill_density = len(extracted_skills) / max(text_length, 1)
    confidence = min(0.95, 0.5 + (skill_density * 10))  # Cap at 0.95
    
    return {
        "skills": sorted(list(extracted_skills)),
        "categories": skill_categories,
        "confidence": round(confidence, 2),
        "total_skills_found": len(extracted_skills)
    }


def enhance_skills_with_synonyms(skills: List[str]) -> List[str]:
    """
    Enhance skill list by adding related skills and synonyms.
    
    Args:
        skills: List of extracted skills
        
    Returns:
        list: Enhanced skill list
    """
    enhanced = set(skills)
    
    # Skill relationships
    skill_relations = {
        "python": ["django", "flask", "fastapi", "pandas", "numpy"],
        "javascript": ["node.js", "react", "vue", "angular", "typescript"],
        "java": ["spring boot", "maven", "gradle"],
        "aws": ["ec2", "s3", "lambda", "rds"],
        "machine learning": ["scikit-learn", "tensorflow", "pytorch"],
    }
    
    for skill in skills:
        if skill in skill_relations:
            # Add related skills with lower confidence
            enhanced.update(skill_relations[skill][:2])  # Add top 2 related
    
    return list(enhanced)
