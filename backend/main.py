from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, content, social, admin
from app.database import engine, Base

app = FastAPI(title="Marketing Automation Platform API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(content.router, prefix="/content", tags=["Content Generation"])
app.include_router(social.router, prefix="/social", tags=["Social Media"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Marketing Automation Platform API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 