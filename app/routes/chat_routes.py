from fastapi import APIRouter, Depends
from pymongo import MongoClient
import os
from datetime import datetime
from bson import ObjectId

router = APIRouter()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

@router.post("/send_message/")
async def send_message(sender: str, receiver: str, message: str):
    chat_data = {
        "sender": sender,
        "receiver": receiver,
        "message": message,
        "timestamp": datetime.utcnow()
    }
    chat_id = db.chats.insert_one(chat_data).inserted_id
    return {"message": "Message sent successfully", "chat_id": str(chat_id)}

@router.get("/get_chat/{sender}/{receiver}")
async def get_chat(sender: str, receiver: str):
    chats = db.chats.find({"$or": [{"sender": sender, "receiver": receiver}, {"sender": receiver, "receiver": sender}]})
    chat_list = [{"sender": chat["sender"], "receiver": chat["receiver"], "message": chat["message"], "timestamp": chat["timestamp"].isoformat()} for chat in chats]
    return {"chat_history": chat_list}