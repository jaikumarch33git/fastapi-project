from fastapi import APIRouter
from .endpoints.authentication import router as auth_router
from .endpoints.asset import router as asset_router


router = APIRouter()
router.include_router(auth_router)
router.include_router(asset_router)