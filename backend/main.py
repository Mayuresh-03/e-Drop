from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
from starlette.middleware.sessions import SessionMiddleware

from database.postgresConn import engine, Base
from models import all_model
from router import user_routes, auth_routes

# Create database tables
all_model.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kurukshetra Backend API",
    description="Backend API Kurukshetra"
)

# 1. SESSION MIDDLEWARE
# Required for Google OAuth redirect state management
app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SESSION_SECRET", "super-secret-key-change-me"),
    same_site="lax",
    https_only=False  # Set to True in production with HTTPS
)

# 2. CORS ORIGINS
# Added Docker container origins (http://localhost:8080) and wildcard allowance for development
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to Kurukshetra!"}

# Include routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)