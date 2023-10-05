from datetime import timedelta
from config.config import settings
from config.db import db
from fastapi import APIRouter, Depends, HTTPException, status, Query
from models.user import User, LoginUserSchema
from schemas.user import userEntity, usersEntity
from bson import ObjectId
from scripts.searchEngine.searchEngine import searchEngine
import utils
from auth import AuthJWT

user = APIRouter()

#Falta cambiar las claves secretas en .env
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN

@user.post('/users/create', response_model=dict,status_code=status.HTTP_201_CREATED, tags=["Users"])
async def createUser(user: User, Authorize: AuthJWT = Depends()):
    #importante usar el metodo .dict()
    new_user = user.dict()
    new_user["password"] = utils.hash_password(new_user["password"])
    new_user["email"] = new_user["email"].lower()
    new_user["image_url"] = "https://profilephotos2.blob.core.windows.net/tutoriapp/image_default.png"

    if db.users.count_documents({"email": new_user["email"]}) > 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='El email ya está registrado')
    id = db.users.insert_one(new_user).inserted_id

    user_created = userEntity(db.users.find_one({"_id": id}))

    #crear token de acceso
    access_token = Authorize.create_access_token(
        subject=user_created['email'], expires_time=timedelta(days=ACCESS_TOKEN_EXPIRES_IN))
    
    #crear token de refresco
    refresh_token = Authorize.create_refresh_token(
        subject=user_created['email'], expires_time=timedelta(days=REFRESH_TOKEN_EXPIRES_IN))
    
    return {"status": "success","access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "user": user_created}

@user.post('/users/login', response_model=dict, tags=["Users"])
async def login(user: LoginUserSchema, Authorize: AuthJWT = Depends()):
    
    db_user = db.users.find_one({"email": user.email.lower()})
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email no registrado en nuestro sistema')
    
    actual_user = user.dict()

    if not utils.verify_password(actual_user['password'], db_user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='contraseña incorrecta')
    
    #crear token de acceso
    access_token = Authorize.create_access_token(
        subject=db_user['email'], expires_time=timedelta(days=ACCESS_TOKEN_EXPIRES_IN))
    
    #crear token de refresco
    refresh_token = Authorize.create_refresh_token(
        subject=db_user['email'], expires_time=timedelta(days=REFRESH_TOKEN_EXPIRES_IN))
    
    return {"status": "success","access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "user": userEntity(db_user)}

@user.post('/users/refresh', response_model=dict, tags=["Users"])
async def refresh(Authorize: AuthJWT = Depends()):
    try:

        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='No se pudo refrescar el token')
        
        user = db.users.find_one({"email": current_user})

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='el usuario no existe')
        
        access_token = Authorize.create_access_token(
            subject= user['email'], expires_time=timedelta(days=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Porfavor proporcione un token de refresco')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    return {"access_token": access_token, "user": userEntity(user)}

@user.get('/users/tutores', response_model=list, status_code=status.HTTP_200_OK,tags=["Users"])
async def getUsers(keywords: str = Query(...)):
    if not keywords :
        tutoresCursor = db.users.find({"is_tutor": True})
        tutores =[]
        for tutor in tutoresCursor:
            dict_tutor = {
                "id" : tutor["_id"].__str__(),
                "email": tutor["email"],
                "name": tutor["name"],
                "availability": tutor["availability"],
                "format_tutor": tutor["format_tutor"],
                "cost_tutor": tutor["cost_tutor"],
                "type_tutor": tutor["type_tutor"],
                "method_tutor": tutor["method_tutor"],
                "type_group_tutor": tutor["type_group_tutor"],
                "tutor_opinions": tutor["tutor_opinions"],
                "subjects_tutor": tutor["subjects_tutor"],
                "image_url": tutor["image_url"]
            }
            tutores.append(dict_tutor)
        return tutores
    else:
        keywords = keywords.split(",")
        tutoresCursor = db.users.find({"is_tutor": True})
        tutores =[]
        for tutor in tutoresCursor:
            score = searchEngine(keywords, tutor["subjects_tutor"])
            if score > 0.399:
                dict_tutor = {
                    "id" : tutor["_id"].__str__(),
                    "email": tutor["email"],
                    "name": tutor["name"],
                    "availability": tutor["availability"],
                    "format_tutor": tutor["format_tutor"],
                    "cost_tutor": tutor["cost_tutor"],
                    "type_tutor": tutor["type_tutor"],
                    "method_tutor": tutor["method_tutor"],
                    "type_group_tutor": tutor["type_group_tutor"],
                    "tutor_opinions": tutor["tutor_opinions"],
                    "subjects_tutor": tutor["subjects_tutor"],
                    "image_url": tutor["image_url"],
                    "score": f"{score:.2f}"
                }
                tutores.append(dict_tutor)     
        tutores.sort(key=lambda x: x["score"], reverse=True)
        for tutor in tutores:
            del tutor["score"]
        return tutores

@user.get('/users/{email}', response_model=dict, status_code=status.HTTP_200_OK,tags=["Users"])
async def getUser(email: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        error = e.__class__.__name__
        if error == 'InvalidHeaderError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Porfavor proporcione un token de acceso')
        if error == 'ExpiredSignatureError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='El token de acceso ha expirado')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    user= db.users.find_one({"email": email})
    return {"userData": userEntity(user)}

@user.get('/users/userName/{id}', response_model= dict, status_code=status.HTTP_200_OK,tags=["Users"])
async def getUsers(id : str):
    user = db.users.find_one({"_id": ObjectId(id)})
    user_dict = {
        "name": user["name"],
        "is_tutor": user["is_tutor"]
    }
    print(user_dict)
    return user_dict


@user.patch('/users/update/{id}', response_model=dict, tags=["Users"], status_code=status.HTTP_200_OK)
async def updateUser(id: str, user: dict, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        error = e.__class__.__name__
        if error == 'InvalidHeaderError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Porfavor proporcione un token de acceso')
        if error == 'JWTDecodeError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='El token de acceso ha expirado')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    stored_user_data = db.users.find_one({"_id": ObjectId(id)})
    update_user = {**stored_user_data, **user}
    update_user = User(**update_user).dict()
    user_updated = db.users.find_one_and_update({"_id": ObjectId(id)}, {"$set": update_user}, return_document=True)

    return userEntity(user_updated)

@user.delete('/users/delete/{id}', response_model=dict, tags=["Users"], status_code=status.HTTP_200_OK)
async def deleteUser(id: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        error = e.__class__.__name__
        if error == 'InvalidHeaderError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Porfavor proporcione un token de acceso')
        if error == 'ExpiredSignatureError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='El token de acceso ha expirado')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    user = db.users.count_documents({"_id": ObjectId(id)})
    if user > 0:
        db.users.delete_one({"_id": ObjectId(id)})
        return {"message": "User deleted successfully"}
    return {"error": "User not found"}