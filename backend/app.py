import os
import chromadb
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.verify import router
from services.utils.logger import logger
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)


state = {}

def verify_and_seed_chromadb():
    try:
        persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./rag/chroma_db")
        client = chromadb.PersistentClient(path=persist_dir)
        collection = client.get_or_create_collection("trusted_sources")
        if collection.count() == 0:
            logger.warning("ChromaDB 'trusted_sources' is empty. Running automatic database population...")
            try:
                from rag.populate_knowledge import populate
                populate()
                logger.info("ChromaDB successfully seeded.")
            except ImportError:
                logger.error("Could not find populate script, skipping auto-seed.")
    except Exception as e:
        logger.error(f"Error checking ChromaDB: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup chroma DB if missing
    verify_and_seed_chromadb()
    
    # Pre-warm DeBERTa-v3 model onto GPU/CPU
    from core.device import get_device, get_device_name
    from services.stance_detection import _load_model
    dev = get_device()
    logger.info(f"Loading DeBERTa-v3 cross-encoder into memory on {dev.type.upper()} ({get_device_name()})...")
    try:
        _load_model()
        logger.info(f"DeBERTa-v3 successfully pre-warmed on {dev.type.upper()}.")
    except Exception as e:
        logger.error(f"Failed to load DeBERTa-v3 model: {e}")
    yield
    state.clear()

app = FastAPI(title="SatyaScan Truth Intelligence System", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def root():
    return {"status": "online", "service": "SatyaScan Truth Intelligence API", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
def health():
    from core.device import get_device, get_device_name
    dev = get_device()
    return {
        "status": "healthy",
        "service": "SatyaScan Backend Engine",
        "version": "1.0.0",
        "device": dev.type.upper(),
        "gpu": get_device_name()
    }
