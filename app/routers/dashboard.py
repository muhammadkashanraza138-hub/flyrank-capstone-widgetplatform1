from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db import get_db
from app.core.deps import current_user
from app.models.models import Submission,Widget
router=APIRouter(prefix='/dashboard',tags=['dashboard'])
@router.get('/submissions')
def submissions(user=Depends(current_user),db:Session=Depends(get_db)):
    rows=db.query(Submission).filter_by(tenant_id=user.tenant_id).order_by(Submission.created_at.desc()).limit(100).all()
    return [{'id':x.id,'widget_id':x.widget_id,'data':x.data,'geo':x.geo,'created_at':x.created_at} for x in rows]
@router.get('/stats')
def stats(user=Depends(current_user),db:Session=Depends(get_db)):
    total=db.query(func.count(Submission.id)).filter_by(tenant_id=user.tenant_id).scalar() or 0
    per=db.query(Submission.widget_id,func.count(Submission.id)).filter_by(tenant_id=user.tenant_id).group_by(Submission.widget_id).all()
    return {'total_submissions':total,'per_widget':{k:v for k,v in per}}
