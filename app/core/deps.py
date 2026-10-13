from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db import get_db
from app.core.config import settings
from app.core.security import decode_token
security=HTTPBearer()
def current_user(creds:HTTPAuthorizationCredentials=Depends(security),db:Session=Depends(get_db)):
    from app.models.models import User
    try: payload=decode_token(creds.credentials,settings.jwt_secret); uid=int(payload['sub'])
    except Exception: raise HTTPException(status_code=401,detail='Invalid authentication')
    user=db.get(User,uid)
    if not user: raise HTTPException(status_code=401,detail='Invalid authentication')
    return user
