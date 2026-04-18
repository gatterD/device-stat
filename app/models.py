from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    devices = relationship("Device", back_populates="owner")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="devices")
    measurements = relationship("Measurement", back_populates="device")

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    device = relationship("Device", back_populates="measurements")

class StatsAggregate(Base):
    __tablename__ = "stats_aggregates"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), index=True)
    period_start = Column(DateTime(timezone=True), nullable=True)
    period_end = Column(DateTime(timezone=True), nullable=True)
    x_min = Column(Float)
    x_max = Column(Float)
    x_sum = Column(Float)
    x_count = Column(Integer)
    x_median = Column(Float)
    y_min = Column(Float)
    y_max = Column(Float)
    y_sum = Column(Float)
    y_count = Column(Integer)
    y_median = Column(Float)
    z_min = Column(Float)
    z_max = Column(Float)
    z_sum = Column(Float)
    z_count = Column(Integer)
    z_median = Column(Float)