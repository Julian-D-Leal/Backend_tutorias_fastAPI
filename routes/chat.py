# from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# from models.chat import Message
# from schemas.messages import messagesEntity
# from config.db import db
# import socketio
# import json
# from bson import ObjectId
# from schemas.user import usersEntity

# router = APIRouter()

# # Create a socket.io server instance
# sio = socketio.AsyncServer(cors_allowed_origins="*")

# @sio.on("connect")
# async def connect(sid, environ):
#     print(f"User {sid} connected")

# @sio.on("disconnect")
# async def disconnect(sid):
#     print(f"User {sid} disconnected")

# @sio.on("message")
# async def message(sid, data):  # Agrega el parámetro "sid" para obtener el ID del socket
#     print(f"Message from {sid}: {data}")
#     await sio.emit("message", data, room=sid)

# @router.get("/chat/{user_id}/{recipient_id}")
# async def get_messages_for_conversation(user_id: str, recipient_id: str):
#     messages = db.messages.find({
#         "$or": [
#             {"sender": user_id, "receiver": recipient_id},
#             {"sender": recipient_id, "receiver": user_id}
#         ]
#     })
#     messages = messagesEntity(messages)
#     return messages

# @router.get("/messages/{user_id}")
# async def get_messages_for_conversation(user_id: str):
#         distinct_senders = db.messages.distinct("sender", {"receiver": user_id})
#         distinct_receivers = db.messages.distinct("receiver", {"sender": user_id})
#         distinct_users = list(set(distinct_senders + distinct_receivers))
#         distinct_users = [user for user in distinct_users if user != user_id]

#         objectIds = [ObjectId(_id) for _id in distinct_users]
#         users = db.users.find({"_id": {"$in": objectIds}})
#         users = list(users)
#         return usersEntity(users)

# @router.websocket("/ws/chat")
# async def chat_endpoint(websocket: WebSocket):
#     await websocket.accept()

#     try:
#         while True:
#             message_data = await websocket.receive_text()
#             message = Message(**json.loads(message_data))
#             print(f"Received message: {message.message}")
#             del message.id
#             db.messages.insert_one(message.dict())
#             await sio.emit("message", message.dict(), room=message.receiver)
#     except WebSocketDisconnect:
#         pass

