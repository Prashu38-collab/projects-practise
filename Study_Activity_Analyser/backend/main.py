from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from database.connection import Base, engine
from routers import activities, analytics, health

# Ensure DB tables are created
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Welcome to Study Activity Analyzer API",
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health",
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health router (available both at /health and /api/v1/health)
app.include_router(health.router)
app.include_router(health.router, prefix=settings.API_V1_PREFIX)

# Primary v1 API Router
app.include_router(activities.router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics.router, prefix=settings.API_V1_PREFIX)

# Fallback root routes for backward compatibility during transition
app.include_router(activities.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")