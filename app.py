from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import settings
from routes.subject import subject
from routes.user import user
from routes.password_reset import password_reset

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
    }]
)

origins = [
    settings.CLIENT_ORIGIN,
    '0.0.0.0'
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
