from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import settings
from app.utils.db import get_db_session
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserResponse, Token
from app.utils.errors import AuthenticationException, ValidationException

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(email: str, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"email": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    db = get_db_session()
    try:
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise ValidationException("Email already registered")
        
        new_user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            full_name=user_data.full_name,
            phone=user_data.phone,
            is_active=True
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return new_user
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    db = get_db_session()
    try:
        user = db.query(User).filter(User.email == credentials.email).first()
        
        if not user or not verify_password(credentials.password, user.hashed_password):
            raise AuthenticationException()
        
        if not user.is_active:
            raise AuthenticationException("User account is inactive")
        
        user.last_login = datetime.utcnow()
        db.commit()
        
        access_token = create_access_token(user.email)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    finally:
        db.close()