from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, content, admin
from app.config.settings import settings
from app.config.database import engine
from app.models.database import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Marketing Automation Platform",
    description="A full-stack web application for automated blog generation and social media posting using AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
# app.include_router(content.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Marketing Automation Platform API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 