from fastapi import APIRouter, HTTPException, Depends
from models.access_model import AccessRequest
from config.db import access_requests_collection, doctor_collection
from config.auth import decode_access_token

router = APIRouter()

async def get_current_doctor(token: str):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    doctor = await doctor_collection.find_one({"email": payload["sub"]})
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.post("/request")
async def request_access(request: AccessRequest, token: str = Depends(get_current_doctor)):
    existing_request = await access_requests_collection.find_one({
        "requesting_doctor": request.requesting_doctor,
        "target_doctor": request.target_doctor,
        "patient_id": request.patient_id
    })

    if existing_request:
        raise HTTPException(status_code=400, detail="Access request already exists")

    await access_requests_collection.insert_one(request.dict())
    return {"message": "Access request sent"}

# View Incoming Access Requests
@router.get("/incoming")
async def incoming_requests(token: str = Depends(get_current_doctor)):
    requests = await access_requests_collection.find({"target_doctor": token["email"]}).to_list(100)
    return requests

# View Outgoing Access Requests
@router.get("/outgoing")
async def outgoing_requests(token: str = Depends(get_current_doctor)):
    requests = await access_requests_collection.find({"requesting_doctor": token["email"]}).to_list(100)
    return requests

# Approve/Deny Access Request
@router.put("/update/{request_id}")
async def update_access_request(request_id: str, status: str, token: str = Depends(get_current_doctor)):
    if status not in ["approved", "denied"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    request = await access_requests_collection.find_one({"_id": request_id, "target_doctor": token["email"]})
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    await access_requests_collection.update_one({"_id": request_id}, {"$set": {"status": status}})
    return {"message": f"Access request {status}"}
