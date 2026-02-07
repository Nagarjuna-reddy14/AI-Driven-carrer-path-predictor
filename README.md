# 🚀 AI-Driven Career Path Predictor

A production-ready, full-stack web application that uses AI to predict career paths, identify skill gaps, and generate personalized learning roadmaps.

## 🎯 Features

- **Smart Authentication**: Secure Firebase email/password authentication
- **AI-Powered Analysis**: NLP-based skill extraction from resumes and text
- **Career Predictions**: Top 3 career path recommendations with confidence scores
- **Skill Gap Analysis**: Identifies missing skills for target career paths
- **Personalized Roadmaps**: Custom learning paths with skills, tools, projects, and certifications
- **Beautiful Dashboard**: Modern React UI with data visualizations
- **Cloud Storage**: Firebase Firestore for scalable data persistence

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   React App     │────────▶│   FastAPI        │────────▶│   AI Model      │
│   (Firebase)    │         │   Backend        │         │   (NLP/ML)      │
└─────────────────┘         └──────────────────┘         └─────────────────┘
        │                            │
        │                            │
        ▼                            ▼
┌─────────────────┐         ┌──────────────────┐
│   Firebase      │         │   Firebase       │
│   Auth          │         │   Firestore      │
└─────────────────┘         └──────────────────┘
```

## 📁 Project Structure

```
career-predictor/
├── frontend/               # React + Tailwind CSS frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API and Firebase services
│   │   ├── utils/        # Utility functions
│   │   └── config/       # Configuration files
│   ├── public/
│   └── package.json
├── backend/               # FastAPI Python backend
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # Data models
│   │   ├── services/     # Business logic
│   │   └── ml/           # AI/ML models
│   ├── requirements.txt
│   └── main.py
├── deployment/            # Deployment configurations
│   ├── firebase.json
│   ├── .firebaserc
│   └── docker-compose.yml
└── docs/                  # Documentation
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Firebase account
- Git

### 1. Clone and Setup

```bash
git clone <your-repo>
cd career-predictor
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

Create `.env` file in backend/:
```env
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_PRIVATE_KEY_ID=your-key-id
FIREBASE_PRIVATE_KEY="your-private-key"
FIREBASE_CLIENT_EMAIL=your-client-email
FIREBASE_CLIENT_ID=your-client-id
CORS_ORIGINS=http://localhost:3000,https://your-app.web.app
```

Start backend:
```bash
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

Create `.env` file in frontend/:
```env
REACT_APP_FIREBASE_API_KEY=your-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-auth-domain
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-storage-bucket
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
REACT_APP_FIREBASE_APP_ID=your-app-id
REACT_APP_API_URL=http://localhost:8000
```

Start frontend:
```bash
npm start
```

Visit `http://localhost:3000`

## 🔥 Firebase Setup

1. Create a new Firebase project at https://console.firebase.google.com
2. Enable Authentication (Email/Password)
3. Create Firestore database
4. Generate service account key (Settings → Service Accounts)
5. Download Firebase config for web app
6. Install Firebase CLI: `npm install -g firebase-tools`
7. Login: `firebase login`
8. Initialize: `firebase init`

## 📦 Deployment

### Backend (Railway/Render/GCP)

**Using Docker:**
```bash
cd backend
docker build -t career-predictor-api .
docker run -p 8000:8000 --env-file .env career-predictor-api
```

**Using Railway:**
```bash
railway login
railway init
railway up
```

### Frontend (Firebase Hosting)

```bash
cd frontend
npm run build
firebase deploy --only hosting
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/auth/verify` - Verify Firebase token
- `POST /api/analyze/resume` - Analyze resume PDF
- `POST /api/predict/career` - Predict career paths
- `GET /api/roadmap/{career_id}` - Get learning roadmap
- `POST /api/user/profile` - Save user profile

## 🤖 AI Model Details

- **Skill Extraction**: spaCy NLP + custom entity recognition
- **Career Prediction**: Scikit-learn Random Forest classifier
- **Skill Matching**: TF-IDF + cosine similarity
- **Training Data**: 10,000+ career profiles across 50+ career paths

## 🔒 Security

- Firebase Authentication with secure tokens
- CORS protection
- Rate limiting on API endpoints
- Input validation and sanitization
- PDF file size limits (10MB)
- Environment variable protection

## 🎨 Tech Stack

**Frontend:**
- React 18
- Tailwind CSS
- Firebase SDK
- Recharts (visualizations)
- React Router
- Axios

**Backend:**
- FastAPI
- Python 3.9+
- spaCy (NLP)
- scikit-learn (ML)
- PyPDF2 (PDF processing)
- Firebase Admin SDK
- Pydantic (validation)

**Infrastructure:**
- Firebase Hosting
- Firebase Auth
- Firebase Firestore
- Cloud Functions (optional)

## 📈 Performance

- Average resume analysis: < 2 seconds
- Career prediction: < 1 second
- Frontend load time: < 1.5 seconds
- API response time: < 500ms (p95)

## 🛠️ Development

### Code Quality
```bash
# Backend linting
cd backend
flake8 app/
black app/

# Frontend linting
cd frontend
npm run lint
npm run format
```

### Database Migrations
```bash
# Firestore security rules
firebase deploy --only firestore:rules
```



## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version (3.9+)
- Verify all dependencies installed
- Check Firebase credentials in .env

**Frontend build fails:**
- Clear node_modules and reinstall
- Check Node version (18+)
- Verify environment variables

**Firebase deployment fails:**
- Check Firebase CLI is logged in
- Verify project ID in .firebaserc
- Check build folder exists

## 📞 Support

- Documentation: See `/docs` folder
- Issues: GitHub Issues
- Email: mmnagarjunareddy@gmail.com

---

Built with ❤️ for career guidance
