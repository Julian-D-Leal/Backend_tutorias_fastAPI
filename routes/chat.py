# import datetime
# from config.db import db
# from models.chat import Message
# import socketio
# import asyncio

# sio_server = socketio.AsyncServer(
#     async_mode='asgi',
#     cors_allowed_origins=[]
# )

# sio_app = socketio.ASGIApp(
#     socketio_server=sio_server,
#     socketio_path='sockets'
# )


# @sio_server.event
# async def connect(sid, environ, auth):
#     print(f'{sid}: connected')
#     await sio_server.emit('join', {'sid': sid})


# @sio_server.event
# async def chat(sid, data):
#     print(f'{sid}: {data}')
#     print("holaaaaa")
#     # message = {
#     #     "sender" : data['sender'],
#     #     "receiver" : data['receiver'],
#     #     "message" : data['message'],
#     #     "date" : datetime.datetime.now().strftime("%Y-%m-%d"),
#     #     "time" : datetime.datetime.now().strftime("%H:%M")
#     # }

#     # db.messages.insert_one(message)
#     await sio_server.emit('chat', {'sid': sid, 'message': data})


# @sio_server.event
# async def disconnect(sid):
#     print(f'{sid}: disconnected')
