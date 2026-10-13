from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import User,Tenant
from app.schemas.schemas import UserCreate,Token
from app.core.security import hash_password,make_token
from app.core.config import settings
router=APIRouter(prefix='/auth',tags=['auth'])
@router.post('/register',response_model=Token)
def register(body:UserCreate,db:Session=Depends(get_db)):
    if db.query(User).filter_by(email=body.email).first(): raise HTTPException(409,'Email already registered')
    tenant=Tenant(name=f'{body.email} tenant'); db.add(tenant); db.flush()
    user=User(tenant_id=tenant.id,email=body.email,password_hash=hash_password(body.password)); db.add(user); db.commit()
    return Token(access_token=make_token(user.id,tenant.id,settings.jwt_secret))
@router.post('/login',response_model=Token)
def login(body:UserCreate,db:Session=Depends(get_db)):
    user=db.query(User).filter_by(email=body.email).first()
    from app.core.security import verify_password
    if not user or not verify_password(body.password,user.password_hash): raise HTTPException(401,'Invalid credentials')
    return Token(access_token=make_token(user.id,user.tenant_id,settings.jwt_secret))
