from fastapi import FastAPI
from app.database import engine, Base
from app.api import devices, analysis, users

app = FastAPI(title="Device Stats Service")

# Подключаем роутеры
app.include_router(devices.router)
app.include_router(analysis.router)
app.include_router(users.router)

@app.on_event("startup")
async def startup_event():
    # Импортируем модели для регистрации в Base.metadata
    import app.models
    # Создаём таблицы если их нет
    Base.metadata.create_all(bind=engine)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Device Stats Service is running"}
