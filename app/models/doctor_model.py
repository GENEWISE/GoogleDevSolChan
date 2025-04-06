from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Patient(BaseModel):
    id: Optional[str] = None
    name: str
    age: int
    diagnosis: str
    treatment: str

class Doctor(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    password: str
    specialization: str
    patients: List[Patient] = []
