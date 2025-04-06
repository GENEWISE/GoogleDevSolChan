from fastapi import APIRouter, HTTPException
from models.doctor_model import Doctor
from config.db import doctor_collection
from config.auth import hash_password, verify_password, create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/register")
async def register_doctor(doctor: Doctor):
    existing = await doctor_collection.find_one({"email": doctor.email})
    if existing:
        raise HTTPException(status_code=400, detail="Doctor already registered")
    
    doctor.password = hash_password(doctor.password)
    await doctor_collection.insert_one(doctor.dict())
    return {"message": "Doctor registered successfully"}

@router.post("/login")
async def login_doctor(email: str, password: str):
    doctor = await doctor_collection.find_one({"email": email})
    if not doctor or not verify_password(password, doctor["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": doctor["email"]}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}
