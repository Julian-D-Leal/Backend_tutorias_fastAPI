from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import settings
from routes.subject import subject
from routes.user import user
from routes.password_reset import password_reset
from routes.blob import blob1 as blob
from routes.chat import router as chat_router
from routes.chat import sio_app

app = FastAPI(
    title="Tutorias FastAPI",
    description= "API desarrollada para el proyecto de trabajo de grado en la Universidad del Valle",
    version="0.0.3",
    openapi_tags=[{
        "name": "Subjects",
        "description": "Subjects endpoints"
    },
    {
        "name": "Users",
        "description": "Users and authentication endpoints"
    },
    {
        "name": "Password Reset",
        "description": "Password reset endpoints"
    },
    {
        "name": "Blobs",
        "description": "Upload image of profile endpoint"
    }]
)


origins = [
    settings.CLIENT_ORIGIN,
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subject)
app.include_router(user)
app.include_router(password_reset)
app.include_router(blob)
app.include_router(chat_router)
app.mount('/', app=sio_app)
