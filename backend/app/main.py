from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .database import engine, Base
from .api.endpoints import properties, searches

# Get settings
settings = get_settings()

# Create database tables
from app.database import Base, engine
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(properties.router, prefix=f"{settings.API_V1_STR}/properties")
app.include_router(searches.router, prefix=f"{settings.API_V1_STR}/search")

@app.get("/")
async def root():
    return {"message": "Welcome to Real Estate Aggregator API"}