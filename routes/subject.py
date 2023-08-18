from config.db import db
from fastapi import APIRouter
from models.subject import Subject
from schemas.subject import subjectEntity, subjectsEntity
from bson import ObjectId

subject = APIRouter()

@subject.get('/subjects', response_model=list[Subject], tags=["Subjects"])
async def getSubjects():
    return subjectsEntity(db.subjects.find())
    

@subject.get('/subjects/{id}', response_model=Subject, tags=["Subjects"])
async def getSubject(id: str):
    return subjectEntity(db.subjects.find_one({"_id": ObjectId(id)}))

#Crear materias
# @subject.post('/subjects/create', response_model=dict, tags=["Subjects"])
# async def createSubject(subject: list[Subject]):
    

#     for subj in subject:
#         subj = subj.dict()
#         del subj['id']

#         if db.subjects.count_documents({"name": subj["name"]}) > 0:
#             return {"error": "Ya existe una materia con ese nombre"}
    
#         db.subjects.insert_one(subj)

#     return {"message": "creado con exito"}

# @subject.put('/subjects/update/{id}', response_model=Subject, tags=["Subjects"])
# async def updateSubject(id: str, subject: Subject):
#     subject_received = dict(subject)
#     del subject_received['id']
#     subject_updated = subjectEntity(conn.tutorias_db.subjects.find_one_and_update({"_id": ObjectId(id)}, {"$set": subject_received}, return_document=True))
#     return subject_updated

# @subject.delete('/subjects/delete/{id}', response_model=dict, tags=["Subjects"])
# async def deleteSubject(id: str):
#     subject = conn.tutorias_db.subjects.count_documents({"_id": ObjectId(id)})
#     if subject > 0:
#         conn.tutorias_db.subjects.delete_one({"_id": ObjectId(id)})
#         return {"message": "Subject deleted successfully"}
#     return {"error": "Subject not found"}

