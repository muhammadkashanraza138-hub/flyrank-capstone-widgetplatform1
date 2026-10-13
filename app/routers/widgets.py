from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.core.deps import current_user
from app.models.models import Widget
from app.schemas.schemas import WidgetCreate,WidgetOut
import uuid
router=APIRouter(prefix='/widgets',tags=['widgets'])
@router.post('',response_model=WidgetOut,status_code=201)
def create(body:WidgetCreate,user=Depends(current_user),db:Session=Depends(get_db)):
    w=Widget(id=str(uuid.uuid4()),tenant_id=user.tenant_id,**body.model_dump()); db.add(w); db.commit(); db.refresh(w); return w
@router.get('',response_model=list[WidgetOut])
def list_widgets(user=Depends(current_user),db:Session=Depends(get_db)): return db.query(Widget).filter_by(tenant_id=user.tenant_id).all()
@router.get('/{widget_id}',response_model=WidgetOut)
def get_widget(widget_id,user=Depends(current_user),db:Session=Depends(get_db)):
    w=db.query(Widget).filter_by(id=widget_id,tenant_id=user.tenant_id).first()
    if not w: raise HTTPException(404,'Widget not found')
    return w
@router.put('/{widget_id}',response_model=WidgetOut)
def update(widget_id,body:WidgetCreate,user=Depends(current_user),db:Session=Depends(get_db)):
    w=db.query(Widget).filter_by(id=widget_id,tenant_id=user.tenant_id).first()
    if not w: raise HTTPException(404,'Widget not found')
    for k,v in body.model_dump().items(): setattr(w,k,v)
    w.version+=1; db.commit(); db.refresh(w); return w
@router.delete('/{widget_id}',status_code=204)
def delete(widget_id,user=Depends(current_user),db:Session=Depends(get_db)):
    w=db.query(Widget).filter_by(id=widget_id,tenant_id=user.tenant_id).first()
    if not w: raise HTTPException(404,'Widget not found')
    db.delete(w); db.commit()
@router.get('/{widget_id}/snippet')
def snippet(widget_id,user=Depends(current_user),db:Session=Depends(get_db)):
    w=db.query(Widget).filter_by(id=widget_id,tenant_id=user.tenant_id).first()
    if not w: raise HTTPException(404,'Widget not found')
    from app.core.config import settings
    return {'snippet':f'<script src="{settings.api_base_url}/widget.js?id={widget_id}"></script>'}
