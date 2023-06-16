from fastapi import FastAPI
from routes.subject import subject

app = FastAPI(
    title="Tutorias FastAPI",
    description= "API desarrollada para el proyecto de trabajo de grado de la Universidad del Valle",
    version="0.0.1",
    openapi_tags=[{
        "name": "Subjects",
        "description": "Subjects endpoints"
    }]
)

app.include_router(subject)