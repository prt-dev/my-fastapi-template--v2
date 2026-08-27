import os
from pathlib import Path
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import frontend_url
from app.router.auth_router import router as auth_router
from app.router.user_router import router as user_router
from app.router.product_router import router as product_router
from app.router.cart_router import router as cart_router
from app.router.client_router import router as client_router
from app.router.blog_router import router as blog_router
from app.router.upload_router import router as upload_router

app = FastAPI(title="FastAPI Template API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://blog-management-gold.vercel.app", "https://blog-management-gold.vercel.app/", "https://blog-management-git-master-prateek-dev.vercel.app", "https://blog-management-5fbawa4q8-prateek-dev.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Ensure uploads directory exists and mount it for static file serving
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

api_router = APIRouter(prefix="/api/v1")


api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(product_router)
api_router.include_router(cart_router)
api_router.include_router(client_router)
api_router.include_router(blog_router)
api_router.include_router(upload_router)

app.include_router(api_router)

