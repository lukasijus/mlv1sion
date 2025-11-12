# app/models/orm.py
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


def gen_uuid():
    return str(uuid.uuid4())


class Tenant(Base):
    __tablename__ = "tenants"
    id = sa.Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = sa.Column(sa.Text, nullable=False)


class User(Base):
    __tablename__ = "users"
    id = sa.Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    tenant_id = sa.Column(
        UUID(as_uuid=False), sa.ForeignKey("tenants.id"), nullable=False
    )
    email = sa.Column(sa.String, nullable=False, unique=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, default=True)


class Asset(Base):
    __tablename__ = "assets"
    id = sa.Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    tenant_id = sa.Column(UUID(as_uuid=False), nullable=False, index=True)
    key = sa.Column(sa.String, nullable=False)  # s3 key
    sha256 = sa.Column(sa.String, nullable=True)
    size = sa.Column(sa.Integer)
    meta_data = sa.Column(JSONB, default={})
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)


class Outbox(Base):
    __tablename__ = "outbox"
    id = sa.Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    aggregate_type = sa.Column(sa.String, nullable=False)
    aggregate_id = sa.Column(sa.String, nullable=False)
    payload = sa.Column(JSONB, nullable=False)
    dispatched = sa.Column(sa.Boolean, default=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
