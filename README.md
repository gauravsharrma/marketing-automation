# Marketing Automation Platform

A full-stack web application for automated blog generation and social media posting using AI.

## Features

- 🔐 Authentication with Email OTP and Google OAuth
- 👥 Role-based access control (Admin/User)
- ✍️ AI-powered blog generation using Cohere
- 📱 Automated social media posting to Facebook and LinkedIn
- 📊 Admin and User dashboards
- 🎨 Modern UI with Tailwind CSS
- ☁️ Cloud-native deployment on Render

## Tech Stack

- Backend: Python FastAPI
- Frontend: HTML, JavaScript, Tailwind CSS
- Database: PostgreSQL (hosted on Render)
- Authentication: JWT + Email OTP
- AI: Cohere API
- Social APIs: Facebook Graph API, LinkedIn Marketing API

## Environment Variables

Create a `.env` file with the following variables:

```env
# App Settings
SECRET_KEY=your-secret-key
FRONTEND_URL=https://your-frontend-url.onrender.com
BACKEND_URL=https://your-backend-url.onrender.com

# Database
DATABASE_URL=postgresql://user:password@host:port/dbname

# Redis (for OTP storage)
REDIS_URL=redis://user:password@host:port

# OAuth Settings
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# API Keys
COHERE_API_KEY=your-cohere-api-key
FACEBOOK_ACCESS_TOKEN=your-facebook-access-token
LINKEDIN_ACCESS_TOKEN=your-linkedin-access-token

# Email Settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
```

## Deployment on Render

### Backend Service

1. Create a new Web Service
2. Connect your GitHub repository
3. Use the following settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add all environment variables

### Frontend Service

1. Create a new Static Site
2. Connect your GitHub repository
3. Use the following settings:
   - Build Command: `npm install && npm run build`
   - Publish Directory: `frontend/dist`
   - Add environment variables as needed

### Database

1. Create a new PostgreSQL database on Render
2. Use the provided connection string in your backend service's environment variables

## Local Development

1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`
5. Run the backend:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Open the frontend `index.html` in your browser

## API Documentation

Once running, visit `/docs` for the interactive API documentation.

## License

MIT 