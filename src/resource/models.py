from sqlalchemy import Column, String, Integer, DateTime, func, Text, Boolean

from database import Base


class DeviceConfiguration(Base):
    __tablename__ = 'device_configurations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(255), unique=True, nullable=False)
    app_config_uri = Column(String(512), nullable=False)
    depth_config_uri = Column(String(512), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
