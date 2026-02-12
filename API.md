# 📚 API Documentation - Career Path Predictor

Base URL: `http://localhost:8000` (development) or your deployed URL

## Authentication

All protected endpoints require a Bearer token from Firebase Authentication.

```
Authorization: Bearer <firebase-id-token>
```

---

## Endpoints

### 🏥 Health & Status

#### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "Career Path Predictor API"
}
```

#### GET `/`
API information.

---

### 🔐 Authentication

#### POST `/api/auth/verify`
Verify Firebase authentication token.

**Request Body:**
```json
{
  "token": "firebase-id-token"
}
```

**Response:**
```json
{
  "uid": "user-id",
  "email": "user@example.com",
  "display_name": null,
  "email_verified": true,
  "created_at": 1234567890
}
```

#### GET `/api/auth/me`
Get current authenticated user.

**Headers:** `Authorization: Bearer <token>`

---

### 📄 Analysis

#### POST `/api/analyze/resume`
Analyze resume PDF and extract skills.

**Headers:**
- `Authorization: Bearer <token>`
- `Content-Type: multipart/form-data`

**Form Data:**
- `file`: PDF file (max 10MB)

**Response:**
```json
{
  "success": true,
  "user_id": "user-id",
  "extracted_text_length": 5432,
  "skills": ["python", "javascript", "react", "machine learning"],
  "categories": {
    "programming": ["python", "javascript"],
    "web_development": ["react"],
    "ai_ml": ["machine learning"]
  },
  "confidence": 0.85,
  "total_skills_found": 15
}
```

#### POST `/api/analyze/text`
Analyze text and extract skills.

**Form Data:**
- `text`: Text to analyze

**Response:** Same as resume endpoint

#### GET `/api/analyze/skills/categories`
Get available skill categories.

---

### 🎯 Prediction

#### POST `/api/predict/career`
Predict career paths based on user profile.

**Request Body:**
```json
{
  "education": "B.S. Computer Science",
  "skills": ["python", "javascript", "react", "sql"],
  "interests": ["web development", "AI"],
  "experience_years": 3
}
```

**Response:**
```json
{
  "analysis_id": "uuid",
  "user_id": "user-id",
  "predictions": [
    {
      "career_title": "Full Stack Developer",
      "confidence": 0.87,
      "description": "Build and maintain both frontend and backend...",
      "average_salary": "$95,000 - $140,000",
      "growth_rate": "22% (Much faster than average)",
      "required_skills": ["javascript", "python", "react", "sql"],
      "skill_match_percentage": 85.5,
      "matched_skills": ["python", "javascript", "react"],
      "missing_skills": ["node.js", "docker"]
    }
  ],
  "top_career": {...},
  "skill_gaps": {
    "missing_skills": ["docker", "kubernetes"],
    "matched_skills": ["python", "sql"],
    "partial_skills": [],
    "gap_percentage": 20.0
  },
  "analyzed_at": "2024-01-20T10:30:00"
}
```

#### GET `/api/predict/careers`
List all available career paths.

**Response:**
```json
{
  "careers": [
    {
      "title": "Full Stack Developer",
      "description": "Build and maintain...",
      "category": "Software Development",
      "salary_range": "$95,000 - $140,000",
      "growth_rate": "22% (Much faster than average)"
    }
  ],
  "total": 15
}
```

#### GET `/api/predict/career/{career_title}`
Get detailed information about a specific career.

#### POST `/api/predict/skill-gaps/{career_title}`
Analyze skill gaps for a specific career.

**Request Body:**
```json
["python", "sql", "javascript"]
```

---

### 🗺️ Roadmap

#### POST `/api/roadmap/generate`
Generate a personalized learning roadmap.

**Request Body:**
```json
{
  "career_path": "Full Stack Developer",
  "missing_skills": ["react", "node.js", "docker"],
  "current_skills": ["python", "sql", "html"]
}
```

**Response:**
```json
{
  "roadmap_id": "uuid",
  "user_id": "user-id",
  "career_path": "Full Stack Developer",
  "timeline": "6-9 months",
  "phases": [
    {
      "phase": 1,
      "title": "Foundation",
      "duration": "1-2 months",
      "skills": ["javascript", "css"],
      "focus": "Build core competencies"
    }
  ],
  "skills_to_learn": ["react", "node.js", "docker"],
  "tools": ["VS Code", "Docker Desktop", "Git"],
  "projects": [
    {
      "title": "Build a Web Scraper",
      "description": "Create a web scraper...",
      "skills_practiced": ["python", "beautifulsoup"],
      "difficulty": "intermediate",
      "estimated_time": "1 week"
    }
  ],
  "certifications": [
    {
      "name": "AWS Certified Developer",
      "provider": "Amazon",
      "url": "https://aws.amazon.com/certification/",
      "cost": "$150",
      "duration": "3 months prep"
    }
  ],
  "resources": [
    {
      "title": "React - The Complete Guide",
      "type": "course",
      "url": "https://udemy.com/...",
      "duration": "48 hours",
      "difficulty": "intermediate"
    }
  ],
  "created_at": "2024-01-20T10:30:00"
}
```

#### GET `/api/roadmap/{roadmap_id}`
Retrieve a saved roadmap.

#### GET `/api/roadmap/user/roadmaps`
Get all roadmaps for current user.

**Response:**
```json
{
  "roadmaps": [
    {
      "roadmap_id": "uuid",
      "career_path": "Full Stack Developer",
      "timeline": "6-9 months",
      "created_at": "2024-01-20T10:30:00"
    }
  ],
  "total": 3
}
```

#### GET `/api/roadmap/resources/{skill}`
Get learning resources for a specific skill.

#### DELETE `/api/roadmap/{roadmap_id}`
Delete a roadmap.

---

### 👤 User Profile

#### POST `/api/user/profile`
Save or update user profile.

**Request Body:**
```json
{
  "education": "B.S. Computer Science",
  "skills": ["python", "javascript"],
  "interests": ["AI", "Web Dev"],
  "experience_years": 3
}
```

#### GET `/api/user/profile`
Get user profile.

#### GET `/api/user/analyses`
Get all analyses for current user.

**Response:**
```json
{
  "analyses": [
    {
      "analysis_id": "uuid",
      "top_career": "Full Stack Developer",
      "confidence": 0.87,
      "analyzed_at": "2024-01-20T10:30:00",
      "total_predictions": 3
    }
  ],
  "total": 5
}
```

#### GET `/api/user/analysis/{analysis_id}`
Get a specific analysis.

#### DELETE `/api/user/profile`
Delete user profile and all associated data.

---

## Error Responses

All endpoints may return these error responses:

### 400 Bad Request
```json
{
  "detail": "Error message",
  "message": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Invalid authentication token"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "field"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ],
  "message": "Invalid request data"
}
```

### 500 Internal Server Error
```json
{
  "message": "An unexpected error occurred",
  "detail": "Error details"
}
```

---

## Rate Limiting

- Default: 60 requests per minute per IP
- Authenticated: 120 requests per minute per user

---

## Interactive Documentation

Once the backend is running:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Example Usage

### Python
```python
import requests

# Login with Firebase
# (Get token from Firebase Auth)

headers = {
    "Authorization": f"Bearer {firebase_token}"
}

# Predict careers
response = requests.post(
    "http://localhost:8000/api/predict/career",
    json={
        "education": "B.S. CS",
        "skills": ["python", "javascript"],
        "interests": ["AI"],
        "experience_years": 2
    },
    headers=headers
)

predictions = response.json()
```

### JavaScript
```javascript
const token = await firebase.auth().currentUser.getIdToken();

const response = await fetch('http://localhost:8000/api/predict/career', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    education: 'B.S. CS',
    skills: ['python', 'javascript'],
    interests: ['AI'],
    experience_years: 2
  })
});

const predictions = await response.json();
```

---

## Changelog

### v1.0.0 (2024-01-20)
- Initial release
- Resume analysis
- Career prediction
- Roadmap generation
- User profile management
