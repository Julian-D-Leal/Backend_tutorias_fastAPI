from config.db import db
from fastapi import APIRouter, status
from models.user import User
from schemas.user import userEntity, usersEntity
from bson import ObjectId
from passlib.hash import sha256_crypt

user = APIRouter()



@user.get('/users', response_model=list[User], status_code=status.HTTP_200_OK,tags=["Users"])
async def getUsers():
    return usersEntity(db.users.find())

@user.get('/users/{id}', response_model=User, status_code=status.HTTP_200_OK,tags=["Users"])
async def getUser(id: str):
    return userEntity(db.users.find_one({"_id": ObjectId(id)}))

@user.post('/users/create', response_model=User,status_code=status.HTTP_201_CREATED, tags=["Users"])
async def createUser(user: User):
    #importante usar el metodo .dict()
    new_user = user.dict()
    new_user["password"] = sha256_crypt.hash(new_user["password"])
    print(new_user)
    del new_user['id']

    if db.subjects.count_documents({"email": new_user["email"]}) > 0:
        return {"error": "El email ya está registrado"}
    id = db.users.insert_one(new_user).inserted_id

    user_created = db.users.find_one({"_id": id})

    return userEntity(user_created)

@user.put('/users/update/{id}', response_model=User, tags=["Users"], status_code=status.HTTP_200_OK)
async def updateUser(id: str, user: User):
    user_received = user.dict()
    del user_received['id']
    user_updated = userEntity(db.users.find_one_and_update({"_id": ObjectId(id)}, {"$set": user_received}, return_document=True))
    return user_updated

@user.delete('/users/delete/{id}', response_model=dict, tags=["Users"], status_code=status.HTTP_200_OK)
async def deleteUser(id: str):
    user = db.users.count_documents({"_id": ObjectId(id)})
    if user > 0:
        db.users.delete_one({"_id": ObjectId(id)})
        return {"message": "User deleted successfully"}
    return {"error": "User not found"}