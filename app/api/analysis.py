from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app import crud, schemas
from app.database import get_db
from app.services.analysis import compute_analysis

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.get("/devices/{device_id}", response_model=schemas.DeviceAnalysis)
def get_device_analysis(
    device_id: int,
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    device = crud.get_device(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return compute_analysis(db, device_id, start, end)

@router.get("/users/{user_id}", response_model=schemas.UserAnalysisResponse)
def get_user_analysis(
    user_id: int,
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_user_analysis(db, user_id, start, end)
