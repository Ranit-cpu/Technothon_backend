from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from app.routers.Users import Users_register, Users_login, Users_dashboard
from app.routers.admin import alogin, admin_dashboard
from app.routers.applications import applications
from app.routers.teams import team_register
from app.routers.events import admin_event, user_event,AU_2024,AU_2025, eventdata, IE_2024,IE_2025
from app.routers.payments import payment_route
from app.routers.sponsors import sponsors
from app.routers.gallery import gallery
from app.routers.update_attandence import Update_csv
from app.routers.food import food_coupon
from app.routers.participants import participant_data
from app.routers.domains import domains
from app.routers.jobs import jobs

import os

app = FastAPI(root_path="/api")

# ✅ allow frontend development servers
origins = [
    "http://localhost:5173",  # vite
    "http://localhost:3000",  # CRA
]

# ✅ CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # IMPORTANT for cookies/sessions
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Session middleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY", "super-secret-key"))

# ✅ Routers
app.include_router(Users_register.router, tags=["Register"])
app.include_router(Users_login.router, tags=["Login"])
app.include_router(Users_dashboard.router, tags=["Dashboard"])
app.include_router(alogin.router, prefix="/admin", tags=["Login"])
app.include_router(Update_csv.router, tags=["Update CSV"])
app.include_router(admin_dashboard.router, tags=["Dashboard"])
app.include_router(admin_event.router, tags=["Admin Events"])
app.include_router(team_register.router, tags=["Team Registration"])
app.include_router(payment_route.router, tags=["Payment"])
app.include_router(sponsors.router, tags=["Sponsors"])
app.include_router(gallery.router, tags=["Gallery"])
app.include_router(user_event.router, tags=["User event"])
app.include_router(domains.router,tags=["Domains"])
app.include_router(jobs.router, tags=["Jobs"])
app.include_router(applications.router, tags=["Applications"])
app.include_router(food_coupon.router, tags=["Food Coupons"])
app.include_router(participant_data.router, tags=["Past Teams"])
app.include_router(eventdata.router, tags=["Event Data"])
app.include_router(IE_2024.router, tags=["IE 2024 Data"])
app.include_router(AU_2024.router, tags=["AU 2024 Data"])
app.include_router(IE_2025.router, tags=["IE 2025 Data"])
app.include_router(AU_2025.router, tags=["AU 2025 Data"])

# ✅ Static + Uploads
app.mount("/static", StaticFiles(directory="app/static"), name="static")

if not os.path.exists("uploads"):
    os.makedirs("uploads")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def root():
    return {"message": "Backend running successfully 🚀"}
