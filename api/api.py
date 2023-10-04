from fastapi import APIRouter

from .routes import encrypt_router, decrypt_router

router = APIRouter()
router.include_router(encrypt_router, tags=["encrypt"], prefix="/encrypt")
router.include_router(decrypt_router, tags=["decrypt"], prefix="/decrypt")