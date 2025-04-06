from pydantic import BaseModel, EmailStr

class AccessRequest(BaseModel):
    requesting_doctor: EmailStr
    target_doctor: EmailStr
    patient_id: str
    status: str = "pending"