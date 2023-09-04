from fastapi import APIRouter
from models.chat import Message
from schemas.messages import messageEntity, messagesEntity
from config.db import db
import socketio
from bson import ObjectId
from schemas.user import usersEntity
from schemas.chat import conversationsEntity
import socketio

router = APIRouter()

sio_server = socketio.AsyncServer(
    async_mode='asgi'
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
    socketio_path='sockets'
)


@sio_server.event
async def connect(sid, environ, socket):
    print("connected:", sid)



@sio_server.event
async def messages(sid, data):
    historial = await get_messages_for_conversation(data["idUser"], data["idReceiver"])
    await sio_server.emit('messages', {'sid': sid, 'messages': historial})

@sio_server.event
async def chat(sid, message):
    print(f'mensaje: {message}')
    print(type(message))
    # del message_format.id
    db.messages.insert_one(message)
    await sio_server.emit('chat', {'sid': sid, 'message': messageEntity(message)})


@sio_server.event
async def disconnect(sid):
    print(f'{sid}: disconnected')

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

    objectIds = [ObjectId(_id) for _id in distinct_users]
    users = db.users.find({"_id": {"$in": objectIds}}, {"name": 1, "_id": 1, "image_url": 1})
    return conversationsEntity(users)

