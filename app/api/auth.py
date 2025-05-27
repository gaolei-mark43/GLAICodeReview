from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.schemas import RegisterRequest, LoginRequest
from app.models.user import User
from app.utils.crypto import generate_salt, hash_password
from app.utils.db import SessionLocal
from app.utils.redis_client import RedisClient
from app.config import NONCE_EXPIRE_SECONDS

from app.utils.jwt_token import create_access_token, get_current_user
from datetime import timedelta
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 注册
@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # 检查用户名是否已存在
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")
    salt = generate_salt()
    password_hash = hash_password(request.password, salt)
    user = User(username=request.username, password_hash=password_hash, salt=salt)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "注册成功"}

# 登录
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if hash_password(request.password, user.salt) != user.password_hash:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    # nonce唯一性校验
    redis_client = RedisClient.get_client()
    if redis_client.exists(request.nonce):
        raise HTTPException(status_code=400, detail="重复请求，nonce已失效")
    redis_client.set(request.nonce, 1, ex=NONCE_EXPIRE_SECONDS) 
    # 生成JWT令牌
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"msg": "登录成功", "access_token": access_token, "token_type": "bearer"}


# 校验token获取当前用户名
@router.get("/me")
def read_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}