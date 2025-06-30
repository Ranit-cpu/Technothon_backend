# # app/routers/participants_Login.py
# from fastapi import APIRouter, HTTPException, Request, Depends
# from fastapi.responses import HTMLResponse
# from sqlalchemy.ext.asyncio import AsyncSession
# from starlette.templating import Jinja2Templates
# from werkzeug.security import check_password_hash
# from sqlalchemy.future import select
# from app.database import get_sql_session
# from app.models.auth_models import UserLoginRequest
# from app.models.participant_models import Participant
# from fastapi.responses import RedirectResponse
# router = APIRouter()
#
# templates = Jinja2Templates(directory="app/templates")
#
# #@router.get("/login", response_class=HTMLResponse)
# async def show_register_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})
#
# #@router.post("/login")      #Create
# async def login_user(data: LoginRequest, request: Request, db_sql: AsyncSession = Depends(get_sql_session)):
#     result = await db_sql.execute(select(Participant).where(Participant.email == data.email))
#     user = result.scalar_one_or_none()
#
#     if user is None:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#
#     try:
#         if check_password_hash(user.password, data.password):
#             request.session['user_id'] = user.id
#             return {"status": "success", "message": "Login successful", "redirect": "/dashboard"}
#         else:
#             raise HTTPException(status_code=401, detail="Invalid credentials")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
#
# @router.get("/logout")
# async def logout_user(request: Request):
#     request.session.clear()
#     return RedirectResponse(url="/", status_code=302)