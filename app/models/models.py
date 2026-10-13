from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
class Base(DeclarativeBase): pass
class Tenant(Base):
    __tablename__='tenants'; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(120)); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
class User(Base):
    __tablename__='users'; id:Mapped[int]=mapped_column(primary_key=True); tenant_id:Mapped[int]=mapped_column(ForeignKey('tenants.id'),index=True); email:Mapped[str]=mapped_column(String(255),unique=True); password_hash:Mapped[str]=mapped_column(String(255)); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
class Widget(Base):
    __tablename__='widgets'; id:Mapped[str]=mapped_column(String(36),primary_key=True); tenant_id:Mapped[int]=mapped_column(ForeignKey('tenants.id'),index=True); type:Mapped[str]=mapped_column(String(30)); title:Mapped[str]=mapped_column(String(160)); description:Mapped[str|None]=mapped_column(String(500),nullable=True); fields:Mapped[list]=mapped_column(JSONB); button_text:Mapped[str]=mapped_column(String(80)); display_options:Mapped[dict]=mapped_column(JSONB); version:Mapped[int]=mapped_column(Integer,default=1); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc)); updated_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))
class Submission(Base):
    __tablename__='submissions'; id:Mapped[str]=mapped_column(String(36),primary_key=True); widget_id:Mapped[str]=mapped_column(ForeignKey('widgets.id'),index=True); tenant_id:Mapped[int]=mapped_column(ForeignKey('tenants.id'),index=True); data:Mapped[dict]=mapped_column(JSONB); ip_address:Mapped[str|None]=mapped_column(String(64),nullable=True); geo:Mapped[dict|None]=mapped_column(JSONB,nullable=True); user_agent:Mapped[str|None]=mapped_column(String(500),nullable=True); idempotency_key:Mapped[str|None]=mapped_column(String(255),nullable=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=lambda:datetime.now(timezone.utc))
