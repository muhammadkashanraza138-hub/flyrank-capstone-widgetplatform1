from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Any
class UserCreate(BaseModel): email:str; password:str=Field(min_length=8,max_length=128)
class Token(BaseModel): access_token:str; token_type:str='bearer'
class WidgetCreate(BaseModel):
    type:Literal['signup','cta','popover']='signup'; title:str=Field(min_length=1,max_length=160); description:str|None=None; fields:list[dict[str,Any]]=Field(min_length=1,max_length=10); button_text:str=Field(min_length=1,max_length=80); display_options:dict[str,Any]={}
class WidgetOut(WidgetCreate): model_config=ConfigDict(from_attributes=True); id:str; version:int; tenant_id:int
class SubmissionIn(BaseModel): data:dict[str,Any]=Field(max_length=20); honeypot:str|None=None
class SubmissionOut(BaseModel): id:str; status:str; geo:dict|None=None
