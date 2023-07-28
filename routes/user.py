from datetime import timedelta
from config.config import settings
from config.db import db
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User, LoginUserSchema
from schemas.user import userEntity, usersEntity
from bson import ObjectId
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
    del new_user['id']

    if db.subjects.count_documents({"email": new_user["email"]}) > 0:
        return {"error": "El email ya está registrado"}
    id = db.users.insert_one(new_user).inserted_id

    user_created = userEntity(db.users.find_one({"_id": id}))

    #crear token de acceso
    access_token = Authorize.create_access_token(
        subject=user_created['email'], expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    
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
        subject=db_user['email'], expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    
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
            subject= user['email'], expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Porfavor proporcione un token de refresco')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    return {"access_token": access_token}


# @user.post('/users/logout', response_model=dict, tags=["Users"])
# async def logout(Authorize: AuthJWT = Depends()):
#     Authorize.unset_jwt_cookies()

#     return{"status": "success", "message": "Se ha cerrado la sesión"}

#falta modificar la función para que retorne los tutores que se están buscando
@user.get('/users/tutores', response_model=list[User], status_code=status.HTTP_200_OK,tags=["Users"])
async def getUsers(Authorize: AuthJWT = Depends()):
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
    
    return usersEntity(db.users.find())

@user.get('/users/{email}', response_model=User, status_code=status.HTTP_200_OK,tags=["Users"])
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
    print(db.users.find_one({"email": email}))
    
    return userEntity(db.users.find_one({"email": email}))



@user.put('/users/update/{id}', response_model=User, tags=["Users"], status_code=status.HTTP_200_OK)
async def updateUser(id: str, user: User, Authorize: AuthJWT = Depends()):
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

    user_received = user.dict()
    user_received["email"] = user_received["email"].lower()
    user_received["password"] = utils.hash_password(user_received["password"])
    del user_received['id']
    user_updated = await userEntity(db.users.find_one_and_update({"_id": ObjectId(id)}, {"$set": user_received}, return_document=True))
    return user_updated

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