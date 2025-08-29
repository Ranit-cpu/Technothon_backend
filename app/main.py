from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from app.routers.Users import Users_register,Users_login,Users_dashboard
from app.routers.admin import alogin,admin_dashboard
from app.routers.teams import team_register
from app.routers.events import admin_event,user_event
from app.routers.payments import payment_route
from app.routers.sponsors import sponsors
from app.routers.gallery import gallery
from app.routers.food import food_coupon

import os

app = FastAPI()
origins = [
   "http://localhost:5173",
    "http://localhost:3000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY", "your_super_secret_key_here"))

app.include_router(Users_register.router,tags=["Register"])
app.include_router(Users_login.router,tags=["Login"])
app.include_router(Users_dashboard.router,tags=["Dashboard"])
app.include_router(alogin.router, prefix="/admin", tags=["Login"])
app.include_router(admin_dashboard.router,tags=["Dashboard"])
app.include_router(admin_event.router, tags=["Admin Events"])
app.include_router(team_register.router, tags=["Team Registration"])
app.include_router(payment_route.router, tags=["Payment"])
app.include_router(sponsors.router, tags=["Sponsors"])
app.include_router(gallery.router, tags=["Gallery"])
app.include_router(user_event.router, tags=["User event"])
app.include_router(food_coupon.router,tags=["Food Coupons"])

app.mount("/static", StaticFiles(directory="app/static"), name="static")

if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")       #Read
def root():
    return "Backend running successfully"
