from fastapi import FastAPI

from app.core.config import settings
from app.routes.auth import router as auth_router
from app.routes.referral import router as referral_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Подключение роутов
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(referral_router, prefix="/referral", tags=["referral"])


@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the Referral System API!"}
