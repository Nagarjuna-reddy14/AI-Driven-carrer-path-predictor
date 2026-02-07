"""
Learning roadmap generator.
Creates personalized learning paths based on career goals and skill gaps.
"""

from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

# Learning resources database
LEARNING_RESOURCES = {
    "python": {
        "courses": [
            {"title": "Python for Everybody", "type": "course", "url": "https://www.coursera.org/specializations/python", "duration": "8 months", "difficulty": "beginner"},
            {"title": "Complete Python Bootcamp", "type": "course", "url": "https://www.udemy.com/course/complete-python-bootcamp/", "duration": "22 hours", "difficulty": "beginner"}
        ],
        "projects": [
            {"title": "Build a Web Scraper", "description": "Create a web scraper to extract data from websites", "skills_practiced": ["python", "beautifulsoup", "requests"], "difficulty": "intermediate", "estimated_time": "1 week"},
            {"title": "Personal Portfolio Website Backend", "description": "Build a REST API for your portfolio", "skills_practiced": ["python", "fastapi", "sql"], "difficulty": "intermediate", "estimated_time": "2 weeks"}
        ]
    },
    "javascript": {
        "courses": [
            {"title": "JavaScript - The Complete Guide", "type": "course", "url": "https://www.udemy.com/course/javascript-the-complete-guide-2020-beginner-advanced/", "duration": "52 hours", "difficulty": "beginner"},
            {"title": "Modern JavaScript From The Beginning", "type": "course", "url": "https://www.udemy.com/course/modern-javascript-from-the-beginning/", "duration": "21 hours", "difficulty": "beginner"}
        ],
        "projects": [
            {"title": "Todo List App", "description": "Build an interactive todo list with local storage", "skills_practiced": ["javascript", "html", "css"], "difficulty": "beginner", "estimated_time": "3 days"},
            {"title": "Weather Dashboard", "description": "Create a weather app using external APIs", "skills_practiced": ["javascript", "api", "async"], "difficulty": "intermediate", "estimated_time": "1 week"}
        ]
    },
    "react": {
        "courses": [
            {"title": "React - The Complete Guide", "type": "course", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "duration": "48 hours", "difficulty": "intermediate"},
            {"title": "The Complete React Developer Course", "type": "course", "url": "https://www.udemy.com/course/react-2nd-edition/", "duration": "39 hours", "difficulty": "intermediate"}
        ],
        "projects": [
            {"title": "E-commerce Product Page", "description": "Build a responsive product showcase with cart", "skills_practiced": ["react", "hooks", "context api"], "difficulty": "intermediate", "estimated_time": "2 weeks"},
            {"title": "Social Media Dashboard", "description": "Create a dashboard with real-time data", "skills_practiced": ["react", "state management", "api integration"], "difficulty": "advanced", "estimated_time": "3 weeks"}
        ]
    },
    "machine learning": {
        "courses": [
            {"title": "Machine Learning Specialization", "type": "course", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "duration": "3 months", "difficulty": "intermediate"},
            {"title": "Deep Learning Specialization", "type": "course", "url": "https://www.coursera.org/specializations/deep-learning", "duration": "5 months", "difficulty": "advanced"}
        ],
        "projects": [
            {"title": "House Price Predictor", "description": "Build a regression model to predict house prices", "skills_practiced": ["machine learning", "scikit-learn", "data analysis"], "difficulty": "intermediate", "estimated_time": "2 weeks"},
            {"title": "Image Classifier", "description": "Create a CNN to classify images", "skills_practiced": ["deep learning", "tensorflow", "computer vision"], "difficulty": "advanced", "estimated_time": "3 weeks"}
        ]
    }
}

# Certification recommendations by career
CERTIFICATIONS = {
    "Full Stack Developer": [
        {"name": "AWS Certified Developer - Associate", "provider": "Amazon", "url": "https://aws.amazon.com/certification/", "cost": "$150", "duration": "3 months prep"},
        {"name": "Microsoft Certified: Azure Developer Associate", "provider": "Microsoft", "url": "https://learn.microsoft.com/certifications/", "cost": "$165", "duration": "2-3 months prep"}
    ],
    "Data Scientist": [
        {"name": "Google Data Analytics Professional Certificate", "provider": "Google", "url": "https://grow.google/certificates/data-analytics/", "cost": "$49/month", "duration": "6 months"},
        {"name": "IBM Data Science Professional Certificate", "provider": "IBM", "url": "https://www.coursera.org/professional-certificates/ibm-data-science", "cost": "$49/month", "duration": "10 months"}
    ],
    "DevOps Engineer": [
        {"name": "AWS Certified DevOps Engineer - Professional", "provider": "Amazon", "url": "https://aws.amazon.com/certification/", "cost": "$300", "duration": "4-6 months prep"},
        {"name": "Kubernetes Certified Administrator (CKA)", "provider": "CNCF", "url": "https://www.cncf.io/certification/cka/", "cost": "$395", "duration": "3 months prep"}
    ],
    "Machine Learning Engineer": [
        {"name": "TensorFlow Developer Certificate", "provider": "Google", "url": "https://www.tensorflow.org/certificate", "cost": "$100", "duration": "2-3 months prep"},
        {"name": "AWS Certified Machine Learning - Specialty", "provider": "Amazon", "url": "https://aws.amazon.com/certification/", "cost": "$300", "duration": "4 months prep"}
    ]
}

# Tools by skill category
TOOLS_BY_SKILL = {
    "python": ["PyCharm", "VS Code", "Jupyter Notebook", "Anaconda"],
    "javascript": ["VS Code", "Node.js", "npm", "Chrome DevTools"],
    "react": ["VS Code", "React DevTools", "Create React App", "Vite"],
    "machine learning": ["Jupyter", "Google Colab", "TensorBoard", "MLflow"],
    "docker": ["Docker Desktop", "Docker Compose", "Kubernetes", "Minikube"],
    "git": ["Git", "GitHub", "GitLab", "GitHub Desktop"]
}


def generate_learning_roadmap(
    career_path: str,
    missing_skills: List[str],
    current_skills: List[str]
) -> Dict:
    """
    Generate a personalized learning roadmap.
    
    Args:
        career_path: Target career path
        missing_skills: Skills to learn
        current_skills: Skills user already has
        
    Returns:
        dict: Complete learning roadmap
    """
    logger.info(f"Generating roadmap for {career_path} with {len(missing_skills)} skills to learn")
    
    # Organize skills into phases based on dependencies
    phases = _create_learning_phases(missing_skills, current_skills)
    
    # Gather resources for each skill
    resources = []
    projects = []
    tools = set()
    
    for skill in missing_skills:
        skill_lower = skill.lower()
        
        # Add courses
        if skill_lower in LEARNING_RESOURCES:
            resources.extend(LEARNING_RESOURCES[skill_lower].get("courses", [])[:2])
            projects.extend(LEARNING_RESOURCES[skill_lower].get("projects", [])[:2])
        
        # Add tools
        if skill_lower in TOOLS_BY_SKILL:
            tools.update(TOOLS_BY_SKILL[skill_lower])
    
    # Get certifications for this career
    certifications = CERTIFICATIONS.get(career_path, [])
    
    # Estimate timeline
    timeline = _estimate_timeline(len(missing_skills), len(phases))
    
    return {
        "career_path": career_path,
        "timeline": timeline,
        "phases": phases,
        "skills_to_learn": missing_skills,
        "tools": list(tools),
        "projects": projects[:5],  # Top 5 projects
        "certifications": certifications,
        "resources": resources[:8]  # Top 8 resources
    }


def _create_learning_phases(missing_skills: List[str], current_skills: List[str]) -> List[Dict]:
    """
    Organize skills into learning phases.
    
    Returns:
        list: Learning phases with skills and timeline
    """
    # Skill dependency graph (simplified)
    dependencies = {
        "html": [],
        "css": ["html"],
        "javascript": ["html", "css"],
        "react": ["javascript"],
        "node.js": ["javascript"],
        "python": [],
        "django": ["python"],
        "flask": ["python"],
        "sql": [],
        "mongodb": [],
        "docker": ["linux"],
        "kubernetes": ["docker"]
    }
    
    current_skills_lower = [s.lower() for s in current_skills]
    missing_skills_lower = [s.lower() for s in missing_skills]
    
    # Phase 1: Foundational skills (no dependencies)
    phase1 = []
    phase2 = []
    phase3 = []
    
    for skill in missing_skills_lower:
        deps = dependencies.get(skill, [])
        
        if not deps:
            # No dependencies - foundation
            phase1.append(skill)
        elif all(dep in current_skills_lower or dep in phase1 for dep in deps):
            # Dependencies satisfied by current skills or phase 1
            phase2.append(skill)
        else:
            # Advanced skills
            phase3.append(skill)
    
    phases = []
    
    if phase1:
        phases.append({
            "phase": 1,
            "title": "Foundation",
            "duration": "1-2 months",
            "skills": phase1,
            "focus": "Build core competencies"
        })
    
    if phase2:
        phases.append({
            "phase": 2,
            "title": "Intermediate",
            "duration": "2-3 months",
            "skills": phase2,
            "focus": "Develop practical skills"
        })
    
    if phase3:
        phases.append({
            "phase": 3,
            "title": "Advanced",
            "duration": "2-4 months",
            "skills": phase3,
            "focus": "Master specialized technologies"
        })
    
    # Always add a final project phase
    phases.append({
        "phase": len(phases) + 1,
        "title": "Portfolio Projects",
        "duration": "1-2 months",
        "skills": ["portfolio building", "real-world projects"],
        "focus": "Build impressive projects to showcase skills"
    })
    
    return phases


def _estimate_timeline(num_skills: int, num_phases: int) -> str:
    """
    Estimate total timeline based on skills and phases.
    
    Args:
        num_skills: Number of skills to learn
        num_phases: Number of learning phases
        
    Returns:
        str: Timeline estimate
    """
    # Rough estimate: 2-4 weeks per skill
    weeks = num_skills * 3
    months = weeks // 4
    
    if months <= 3:
        return "2-3 months"
    elif months <= 6:
        return "4-6 months"
    elif months <= 9:
        return "6-9 months"
    else:
        return "9-12 months"


def get_skill_resources(skill: str) -> Dict:
    """
    Get learning resources for a specific skill.
    
    Args:
        skill: Skill name
        
    Returns:
        dict: Resources for the skill
    """
    skill_lower = skill.lower()
    return LEARNING_RESOURCES.get(skill_lower, {
        "courses": [],
        "projects": []
    })
