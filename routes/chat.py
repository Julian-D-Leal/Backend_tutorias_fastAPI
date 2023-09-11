from fastapi import APIRouter
from models.chat import Message
from schemas.messages import messageEntity, messagesEntity
from config.db import db
import socketio
from bson import ObjectId
from schemas.chat import conversationsEntity
import socketio

router = APIRouter()

sio_server = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=[]
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='sockets'
)

@sio_server.event
async def connect(sid, environ, socket):
    print("connected:", sid)

@sio_server.event
async def disconnect(sid):
    print(f'{sid}: disconnected')

@sio_server.event
async def messages(sid, data):
    print(data)
    sender = data["idUser"]
    receiver = data["idReceiver"]
    room_id = await get_room_id(sender, receiver)
    historial = await get_messages_for_conversation(data["idUser"], data["idReceiver"])
    await sio_server.emit('messages', {'sid': sid, 'messages': historial}, room=room_id)

@sio_server.event
async def chat(sid, message):
    sender = message["sender"]
    receiver = message["receiver"]
    room_id = await get_room_id(sender, receiver)
    message = Message(**message)
    del message.id
    print(f'mensaje: {message}')
    message = message.dict()
    db.messages.insert_one(message)
    await sio_server.emit('chat', {'sid': sid, 'message': messageEntity(message)},  room=room_id)

@sio_server.event
async def join_room(sid, data):
    sender = data["idUser"]
    receiver = data["idReceiver"]
    room_id = await get_room_id(sender, receiver)
    print(f'{sid}: joined room {room_id}')
    sio_server.enter_room(sid, room_id)
    db.messages.update_many({"sender": receiver, "receiver": sender}, {"$set": {"read": True}})
    await sio_server.emit('join_room', {'sid': sid, 'room': room_id}, room=room_id)

async def get_room_id(user_id: str, recipient_id: str):
    sorted_ids = sorted([user_id, recipient_id])
    concatenated_ids = "".join(sorted_ids)
    room_id = db.rooms.find_one({"room": concatenated_ids})
    if not room_id:
        room_id = db.rooms.insert_one({"room": concatenated_ids})
    print(room_id.get("room"))
    return room_id.get("room")

async def get_messages_for_conversation(user_id: str, recipient_id: str):
    messages = db.messages.find({
        "$or": [
            {"sender": user_id, "receiver": recipient_id},
            {"sender": recipient_id, "receiver": user_id}
        ]
    })
    return messagesEntity(messages)

@router.get("/messages/{user_id}")
async def get_conversations_by_id(user_id: str):
    distinct_senders = db.messages.distinct("sender", {"receiver": user_id})
    distinct_receivers = db.messages.distinct("receiver", {"sender": user_id})
    distinct_users = list(set(distinct_senders + distinct_receivers))
    distinct_users = [user for user in distinct_users if user != user_id]
    unread_messages = db.messages.distinct("sender",{"receiver": user_id, "read": False})

    objectIds = [ObjectId(_id) for _id in distinct_users]
    objectIds_unread_messages= [ObjectId(_id) for _id in unread_messages]
    users = db.users.find({"_id": {"$in": objectIds}}, {"name": 1, "_id": 1, "image_url": 1})
    response=[]
    for user in users:
        user_info = {"_id": user["_id"], "name": user["name"], "image_url": user["image_url"],"read": False if user["_id"] in objectIds_unread_messages else True}
        response.append(user_info)
    print("response:" + str(response))
    return conversationsEntity(response)

