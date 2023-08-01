from datetime import timedelta
from config.db import db
from fastapi import APIRouter, HTTPException,status
from models.password_reset import ChangePassword, PasswordReset
from bson import ObjectId
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import uuid
import smtplib
import utils
from email.utils import formataddr


password_reset = APIRouter()

#funcion para generar el token
def generate_token():
    return str(uuid.uuid4())

#funcion para enviar el correo
def send_reset_email(email,code):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_email = 'info.tutoriapp@gmail.com'
    smtp_password = 'reihohpjgvdvdrmc'

    sender_name = 'Tutoriapp'
    receiver_email = email
    subject = 'Código de recuperación de contraseña'
    message = f'Tu código es: {code}'

    # Crea el objeto del mensaje
    msg = EmailMessage()
    msg['From'] = formataddr((sender_name, smtp_email))
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Agrega el cuerpo del mensaje
    msg.set_content(message)

    # Inicia la conexión al servidor SMTP y envía el mensaje
    smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
    smtp.login(smtp_email, smtp_password)
    smtp.sendmail(smtp_email, receiver_email, msg.as_string())
    smtp.quit()

@password_reset.post('/password_reset/', response_model=PasswordReset, tags=["Password Reset"])
async def createPasswordReset(password_reset: PasswordReset):
    db_user = db.users.find_one({"email": password_reset.email.lower()})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email no registrado en nuestro sistema')
    user_email = password_reset.email.lower()
    reset_code = generate_token()
    send_reset_email(user_email,reset_code)
    current_datetime = datetime.now()
    expiration_datetime = current_datetime + timedelta(hours=1)
    password_reset = PasswordReset(
        id=None,
        email=user_email,
        token=reset_code,
        expires=expiration_datetime,
        used='pendiente'
        )
    result = db.password_resets.insert_one(password_reset.dict())
    password_reset.id = str(result.inserted_id)
    
    return password_reset

@password_reset.post("/change_password/", response_model=ChangePassword, tags=["Password Reset"])
async def change_password(change_password: ChangePassword):

    tokens = list(db.password_resets.find({"token": change_password.token}))
    sorted_tokens = sorted(tokens, key=lambda x: x["expires"], reverse=True)

    if not sorted_tokens:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Token no válido')

    db_token = sorted_tokens[0]

    if db_token["used"] == "usado":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Token ya usado')
    elif db_token["expires"] < datetime.now():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Token expirado')
    else:
        new_password = utils.hash_password(change_password.password)
        db.password_resets.update_one({"_id": ObjectId(db_token["_id"])}, {"$set": {"used": "usado"}})
        db.users.update_one({"email": db_token["email"]}, {"$set": {"password": new_password}})

    response = {
        "token": change_password.token,
        "password": change_password.password
    }
    return response