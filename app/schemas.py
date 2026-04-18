from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MeasurementCreate(BaseModel):
    x: float
    y: float
    z: float

class MeasurementResponse(MeasurementCreate):
    id: int
    device_id: int
    timestamp: datetime
    class Config:
        from_attributes = True

class DeviceBase(BaseModel):
    name: str

class DeviceCreate(DeviceBase):
    user_id: Optional[int] = None

class DeviceResponse(DeviceBase):
    id: int
    user_id: Optional[int]
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    devices: List[DeviceResponse] = []
    class Config:
        from_attributes = True

class AxisStats(BaseModel):
    min: float
    max: float
    count: int
    sum: float
    median: float

class DeviceAnalysis(BaseModel):
    x: AxisStats
    y: AxisStats
    z: AxisStats

class UserAnalysisResponse(BaseModel):
    user_id: int
    total: DeviceAnalysis
    per_device: dict[int, DeviceAnalysis]  # device_id -> stats