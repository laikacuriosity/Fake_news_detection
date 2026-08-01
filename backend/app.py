from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.verify import router

app = FastAPI(title="fakenewsdetector", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only — restrict this before any real deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)