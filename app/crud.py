from sqlalchemy.orm import Session
from sqlalchemy import func
import numpy as np
from app import models, schemas
from app.services.analysis import compute_analysis

# User CRUD
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_devices(db: Session, user_id: int):
    return db.query(models.Device).filter(models.Device.user_id == user_id).all()

# Device CRUD
def create_device(db: Session, device: schemas.DeviceCreate):
    db_device = models.Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()

# Measurement CRUD
def create_measurement(db: Session, device_id: int, measurement: schemas.MeasurementCreate):
    db_measurement = models.Measurement(**measurement.dict(), device_id=device_id)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    # Импорт внутри функции чтобы избежать циклических импортов
    from tasks.analytics import update_aggregates_task
    update_aggregates_task.delay(device_id)
    return db_measurement

# User Analysis
def get_user_analysis(db: Session, user_id: int, start=None, end=None):
    devices = get_user_devices(db, user_id)
    per_device = {}
    
    for device in devices:
        stats = compute_analysis(db, device.id, start, end)
        per_device[device.id] = stats
    
    total = compute_analysis_for_user_devices(db, user_id, start, end)
    return schemas.UserAnalysisResponse(user_id=user_id, total=total, per_device=per_device)

def compute_analysis_for_user_devices(db: Session, user_id: int, start=None, end=None):
    devices = get_user_devices(db, user_id)
    if not devices:
        return schemas.DeviceAnalysis(
            x=schemas.AxisStats(min=0, max=0, count=0, sum=0, median=0),
            y=schemas.AxisStats(min=0, max=0, count=0, sum=0, median=0),
            z=schemas.AxisStats(min=0, max=0, count=0, sum=0, median=0)
        )
    
    device_ids = [d.id for d in devices]
    query = db.query(models.Measurement).filter(models.Measurement.device_id.in_(device_ids))
    
    if start:
        query = query.filter(models.Measurement.timestamp >= start)
    if end:
        query = query.filter(models.Measurement.timestamp <= end)
    
    rows = query.with_entities(
        models.Measurement.x,
        models.Measurement.y,
        models.Measurement.z
    ).all()
    
    if not rows:
        return schemas.DeviceAnalysis(
            x=schemas.AxisStats(min=0, max=0, count=0, sum=0, median=0),
            y=schemas.AxisStats(min=0, max=0, count=0, sum=0, median=0),
            z=schemas.AxisStats(min=0, max=0, count=0, sum=0, median=0)
        )
    
    x_vals = [r[0] for r in rows]
    y_vals = [r[1] for r in rows]
    z_vals = [r[2] for r in rows]
    
    return schemas.DeviceAnalysis(
        x=schemas.AxisStats(
            min=float(np.min(x_vals)),
            max=float(np.max(x_vals)),
            count=len(x_vals),
            sum=float(np.sum(x_vals)),
            median=float(np.median(x_vals))
        ),
        y=schemas.AxisStats(
            min=float(np.min(y_vals)),
            max=float(np.max(y_vals)),
            count=len(y_vals),
            sum=float(np.sum(y_vals)),
            median=float(np.median(y_vals))
        ),
        z=schemas.AxisStats(
            min=float(np.min(z_vals)),
            max=float(np.max(z_vals)),
            count=len(z_vals),
            sum=float(np.sum(z_vals)),
            median=float(np.median(z_vals))
        )
    )
