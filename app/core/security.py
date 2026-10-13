from datetime import datetime,timedelta,timezone
from jose import jwt
import hashlib
SECRET=''
def hash_password(p): return hashlib.sha256(p.encode()).hexdigest()
def verify_password(p,h): return hash_password(p)==h
def make_token(user_id,tenant_id,secret): return jwt.encode({'sub':str(user_id),'tenant_id':tenant_id,'exp':datetime.now(timezone.utc)+timedelta(hours=8)},secret,algorithm='HS256')
def decode_token(token,secret): return jwt.decode(token,secret,algorithms=['HS256'])
