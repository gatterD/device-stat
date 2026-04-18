from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import numpy as np

from app.models import Measurement
from app.schemas import DeviceAnalysis, AxisStats

def compute_analysis(db: Session, device_id: int, start: datetime = None, end: datetime = None) -> DeviceAnalysis:
    query = db.query(Measurement).filter(Measurement.device_id == device_id)
    if start:
        query = query.filter(Measurement.timestamp >= start)
    if end:
        query = query.filter(Measurement.timestamp <= end)

    rows = query.with_entities(Measurement.x, Measurement.y, Measurement.z).all()
    if not rows:
        empty_stats = AxisStats(min=0.0, max=0.0, count=0, sum=0.0, median=0.0)
        return DeviceAnalysis(x=empty_stats, y=empty_stats, z=empty_stats)

    x_vals = [r[0] for r in rows]
    y_vals = [r[1] for r in rows]
    z_vals = [r[2] for r in rows]

    def axis_stats(values):
        arr = np.array(values)
        return AxisStats(
            min=float(np.min(arr)),
            max=float(np.max(arr)),
            count=len(arr),
            sum=float(np.sum(arr)),
            median=float(np.median(arr))
        )

    return DeviceAnalysis(
        x=axis_stats(x_vals),
        y=axis_stats(y_vals),
        z=axis_stats(z_vals)
    )