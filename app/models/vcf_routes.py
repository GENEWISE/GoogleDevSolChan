from fastapi import APIRouter, File, UploadFile, Depends
from pymongo import MongoClient
import os
# Custom parser for VCF files
from bson import ObjectId

router = APIRouter()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

@router.post("/upload_vcf/")
async def upload_vcf(file: UploadFile = File(...)):
    file_content = await file.read()
    parsed_data = vcf_parser.parse_vcf(file_content.decode("utf-8"))

    # Store metadata
    file_metadata = {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(file_content),
        "variants_count": len(parsed_data),
    }
    file_id = db.vcf_files.insert_one(file_metadata).inserted_id

    # Store variants
    for variant in parsed_data:
        variant["file_id"] = file_id
        db.variants.insert_one(variant)

    return {"message": "VCF file uploaded and processed", "file_id": str(file_id)}
