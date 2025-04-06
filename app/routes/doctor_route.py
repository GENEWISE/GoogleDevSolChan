from fastapi import APIRouter, HTTPException, Depends
from models.doctor_model import Doctor, Patient
from config.db import doctor_collection
from config.auth import decode_access_token
from bson import ObjectId

router = APIRouter()

async def get_current_doctor(token: str):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    doctor = await doctor_collection.find_one({"email": payload["sub"]})
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

# Get Doctor Profile
@router.get("/profile")
async def get_doctor_profile(token: str = Depends(get_current_doctor)):
    return {"name": token["name"], "email": token["email"], "specialization": token["specialization"]}

# Update Doctor Profile
@router.put("/update")
async def update_doctor_profile(update_data: Doctor, token: str = Depends(get_current_doctor)):
    updated_doc = await doctor_collection.update_one(
        {"email": token["email"]}, {"$set": update_data.dict(exclude_unset=True)}
    )
    if updated_doc.modified_count == 0:
        raise HTTPException(status_code=400, detail="Update failed")
    return {"message": "Doctor profile updated"}

# Add Patient
@router.post("/patients/add")
async def add_patient(patient: Patient, token: str = Depends(get_current_doctor)):
    patient.id = str(ObjectId())  # Assign a unique ID
    await doctor_collection.update_one(
        {"email": token["email"]}, {"$push": {"patients": patient.dict()}}
    )
    return {"message": "Patient added successfully"}

# Get All Patients
@router.get("/patients")
async def get_patients(token: str = Depends(get_current_doctor)):
    return token.get("patients", [])

# Update Patient Data
@router.put("/patients/update/{patient_id}")
async def update_patient(patient_id: str, patient_data: Patient, token: str = Depends(get_current_doctor)):
    doctor = await doctor_collection.find_one({"email": token["email"]})
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    patients = doctor.get("patients", [])
    for p in patients:
        if p["id"] == patient_id:
            p.update(patient_data.dict(exclude_unset=True))
            break
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

    await doctor_collection.update_one({"email": token["email"]}, {"$set": {"patients": patients}})
    return {"message": "Patient updated successfully"}

# Delete Patient
@router.delete("/patients/delete/{patient_id}")
async def delete_patient(patient_id: str, token: str = Depends(get_current_doctor)):
    doctor = await doctor_collection.find_one({"email": token["email"]})
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    patients = doctor.get("patients", [])
    updated_patients = [p for p in patients if p["id"] != patient_id]

    if len(updated_patients) == len(patients):
        raise HTTPException(status_code=404, detail="Patient not found")

    await doctor_collection.update_one({"email": token["email"]}, {"$set": {"patients": updated_patients}})
    return {"message": "Patient deleted successfully"}
