from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.services.telegram_auth import telegram_auth_service

router = APIRouter()


@router.options("/login")
async def login_options():
    """
    Handle OPTIONS request for login endpoint
    """
    return Response(
        status_code=status.HTTP_200_OK,
        headers={
            "Access-Control-Allow-Origin": settings.FRONTEND_URL,
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "3600"
        }
    )


@router.post("/login", response_model=schemas.Token)
async def login(
    login_data: schemas.LoginRequest,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    try:
        user = crud.user.authenticate(
            db, email=login_data.email, password=login_data.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif not crud.user.is_active(user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return {
            "access_token": security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            "token_type": "bearer",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/logout")
async def logout(
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    Logout current user.
    """
    return {"message": "Successfully logged out"}


@router.post("/register", response_model=schemas.User)
async def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.post("/telegram/login", response_model=schemas.Token)
async def telegram_login(
    *,
    db: Session = Depends(deps.get_db),
    telegram_data: dict,
) -> Any:
    """
    Login or register user with Telegram data.
    """
    # Проверяем данные от Telegram
    verified_data = await telegram_auth_service.verify_telegram_data(telegram_data)
    if not verified_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Telegram data",
        )
    
    # Получаем или создаем пользователя
    user = await telegram_auth_service.get_or_create_user(verified_data)
    
    # Создаем токен доступа
    access_token = await telegram_auth_service.create_access_token(user)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/telegram/login-url")
async def get_telegram_login_url(
    user_id: int,
) -> Any:
    """
    Get Telegram login URL.
    """
    login_url = await telegram_auth_service.get_login_url(user_id)
    return {"url": login_url.url}


@router.get("/telegram/webapp-url")
async def get_telegram_webapp_url() -> Any:
    """
    Get Telegram Web App URL.
    """
    webapp_url = await telegram_auth_service.get_webapp_url()
    return {"url": webapp_url}


@router.post("/test-token", response_model=schemas.User)
def test_token(current_user: schemas.User = Depends(deps.get_current_user)) -> Any:
    """
    Проверка JWT токена.
    """
    return current_user 