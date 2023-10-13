from fastapi import APIRouter
from .routes import encrypt_router, decrypt_router, digital_signature_router, auth_router

router = APIRouter()
router.include_router(auth_router, tags=["auth"], prefix="/auth")
router.include_router(encrypt_router, tags=["encrypt"], prefix="/encrypt")
router.include_router(decrypt_router, tags=["decrypt"], prefix="/decrypt")
router.include_router(digital_signature_router, tags=["digital_signature"], prefix="/digital_signature")