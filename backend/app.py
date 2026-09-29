from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.verify import router
import os

app = FastAPI(title="Aletheia Fake News Detector", version="2.0")

# Phase 4, #26 - Use Allowed frontend domain from env
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)