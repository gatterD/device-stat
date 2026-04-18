from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import numpy as np
from app.models import Measurement, StatsAggregate, Device

def update_device_aggregates(db: Session, device_id: int):
    """Обновляет агрегированные статистики для устройства"""
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        return
    
    measurements = db.query(Measurement).filter(
        Measurement.device_id == device_id
    ).all()
    
    if not measurements:
        return
    
    x_vals = [m.x for m in measurements]
    y_vals = [m.y for m in measurements]
    z_vals = [m.z for m in measurements]
    
    aggregate = db.query(StatsAggregate).filter(
        StatsAggregate.device_id == device_id,
        StatsAggregate.period_start.is_(None),
        StatsAggregate.period_end.is_(None)
    ).first()
    
    if not aggregate:
        aggregate = StatsAggregate(device_id=device_id)
        db.add(aggregate)
    
    aggregate.x_min = float(np.min(x_vals))
    aggregate.x_max = float(np.max(x_vals))
    aggregate.x_sum = float(np.sum(x_vals))
    aggregate.x_count = len(x_vals)
    aggregate.x_median = float(np.median(x_vals))
    
    aggregate.y_min = float(np.min(y_vals))
    aggregate.y_max = float(np.max(y_vals))
    aggregate.y_sum = float(np.sum(y_vals))
    aggregate.y_count = len(y_vals)
    aggregate.y_median = float(np.median(y_vals))
    
    aggregate.z_min = float(np.min(z_vals))
    aggregate.z_max = float(np.max(z_vals))
    aggregate.z_sum = float(np.sum(z_vals))
    aggregate.z_count = len(z_vals)
    aggregate.z_median = float(np.median(z_vals))
    
    db.commit()
    print(f"Aggregates updated for device {device_id}")
