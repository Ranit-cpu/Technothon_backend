from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from app.routers.Users import Users_register,Users_login,Users_dashboard
from app.routers.admin import alogin,admin_dashboard
from app.routers.teams import team_register
from app.routers.events import admin_event
from app.routers.payments import payment_route

import os

app = FastAPI()


app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY", "your_super_secret_key_here"))

app.include_router(Users_register.router,tags=["Register"])
app.include_router(Users_login.router,tags=["Login"])
app.include_router(Users_dashboard.router,tags=["Dashboard"])
app.include_router(alogin.router, prefix="/admin", tags=["Login"])
app.include_router(admin_dashboard.router,tags=["Dashboard"])
app.include_router(admin_event.router, tags=["Admin Events"])
app.include_router(team_register.router, tags=["Team Registration"])
app.include_router(payment_route.router, tags=["Payment"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")       #Read
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


