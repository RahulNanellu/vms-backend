from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.visitors import router as visitors_router
from app.api.routes.ptt import router as ptt_router
from app.api.routes.admin import router as admin_router
from app.api.routes import users as users_router
from app.api.routes.auth import router as auth_router

app = FastAPI(title="VMS + QuickTalk API", version="0.1.0")

# Routers
app.include_router(auth_router,     prefix="/auth",     tags=["auth"])
app.include_router(health_router,   prefix="/health",   tags=["health"])
app.include_router(visitors_router, prefix="/visitors", tags=["visitors"])
app.include_router(ptt_router,      prefix="/ptt",      tags=["ptt"])
app.include_router(admin_router,    prefix="/admin",    tags=["admin"])
app.include_router(users_router.router, prefix="/users", tags=["users"])
