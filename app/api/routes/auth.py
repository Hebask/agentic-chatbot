from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.auth import (
    AuthResponse,
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
def register(payload: UserRegisterRequest, db: Session = Depends(get_db)) -> AuthResponse:
    auth_service = AuthService(db)
    user = auth_service.register_user(payload)
    token = auth_service.create_access_token(user)

    return AuthResponse(
        user=UserResponse.model_validate(user),
        token=TokenResponse(access_token=token),
    )


@router.post("/login", response_model=AuthResponse)
def login(payload: UserLoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(payload)
    token = auth_service.create_access_token(user)

    return AuthResponse(
        user=UserResponse.model_validate(user),
        token=TokenResponse(access_token=token),
    )