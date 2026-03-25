from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import NotFoundError, ValidationError
from app.db.models import User
from app.schemas.auth import UserLoginRequest, UserRegisterRequest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.settings = get_settings()

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, user: User) -> str:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=self.settings.jwt_access_token_expire_minutes
        )
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "exp": expire,
        }
        return jwt.encode(
            payload,
            self.settings.jwt_secret_key,
            algorithm=self.settings.jwt_algorithm,
        )

    def decode_access_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.settings.jwt_secret_key,
                algorithms=[self.settings.jwt_algorithm],
            )
        except JWTError as exc:
            raise ValidationError("Invalid or expired authentication token") from exc

    def get_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError("User not found")
        return user

    def register_user(self, payload: UserRegisterRequest) -> User:
        existing_user = self.get_user_by_email(payload.email)
        if existing_user:
            raise ValidationError("A user with this email already exists")

        user = User(
            email=payload.email.strip().lower(),
            full_name=payload.full_name.strip(),
            hashed_password=self.get_password_hash(payload.password),
            is_active=True,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, payload: UserLoginRequest) -> User:
        user = self.get_user_by_email(payload.email.strip().lower())
        if not user:
            raise ValidationError("Invalid email or password")

        if not self.verify_password(payload.password, user.hashed_password):
            raise ValidationError("Invalid email or password")

        if not user.is_active:
            raise ValidationError("User account is inactive")

        return user