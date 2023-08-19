from datetime import timedelta
from email.mime.image import MIMEImage
import random
import string
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
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64

password_reset = APIRouter()

#funcion para generar el token
def generate_token(): 
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(6))
    return short_code

#funcion para enviar el correo
def send_reset_email(email,code, name):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_email = 'info.tutoriapp@gmail.com'
    smtp_password = 'reihohpjgvdvdrmc'

    sender_name = 'Tutoriapp'
    receiver_email = email
    subject = 'Código de recuperación de contraseña'
    message = f'''
    <!DOCTYPE html>
<html>

<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #1F3040;
        }}

        .container {{
            width: 100%;
            height: 100%;
        }}

        .body {{
            max-width: 100vw;
            max-height: 69vh;
            height: 68vh;
            display: flex;
            flex-direction: column;
            background-color: #155B68;
            justify-content: center;
        }}

        .head {{
            color: white;
            display: flex;
            flex-direction: column;
            height: 15vh;
            align-items: center;
            justify-content: center;
        }}

        .titulo {{
            text-align: center;
            font-size: 3vh;
        }}

        .footer {{
            height: 15vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}

        .logo {{
            width: 7vh;
            height: 7vh;
        }}

        .mensaje {{
            text-align: center;
            font-size: 3vh;
            color: #1F3040;
            padding: 0vh 20vw;
        }}

        h2 {{
            font-size: 1.8vh;
            text-align: left;
            color: white;
            padding: 0 20vw;
        }}

        .code {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 1.8vh;
        }}

        .code-value {{
            width: 5vh;
            height: 5vh;
            border: 2px solid white;
            border-radius: 5px;
            font-size: 3vh;
            margin: 0 5px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #1F3040;
        }}
        .box {{
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            text-align: center;
            flex: 0 0 calc(33.33% - 40px);
        }}
        .codigotexto{{
            text-align: center;
        }}
    </style>
</head>

<body>
    <div class="container">
        <div class="head">
            <h1 class="titulo">
                TUTORIAPP
            </h1>
            <img class="logo" src="https://i.ibb.co/DWHVDfC/logo.png" alt="TutoriApp"/>
        </div>
        <div class="body">
            <h2 class="mensaje">
                Hola {name}
            </h2>
            <h2 >
                Hemos recibido una solicitud para restablecer la contraseña de tu cuenta en Tutoriapp.
            </h2>
            <div>
                <h2 class="codigotexto">
                    Código de recuperación
                </h2>
                <div class="code">
                    <div class="code-value">{code[0]}</div>
                    <div class="code-value">{code[1]}</div>
                    <div class="code-value">{code[2]}</div>
                    <div class="code-value">{code[3]}</div>
                    <div class="code-value">{code[4]}</div>
                    <div class="code-value">{code[5]}</div>
                </div>
            </div>
            <h2>
               El código que tienes en este correo electrónico es necesario para reestablecer tu contraseña. No compartas este código con nadie.
            </h2>
            <h2>
                Si no estás tratando de iniciar sesión, te invitamos a reestablecer tu contraseña de inmediato.
            </h2>
            <h2>
                Atentamente, el equipo de Tutoriapp.
            </h2>
        </div>
        <div class="footer">
            <h2>
                Si tienes alguna duda contactanos: info.tutoriapp@gmail.com
            </h2>
            <h2>
                © 2023 Tutoriapp. Todos los derechos reservados.
            </h2>
        </div>
    </div>
</body>

</html>
    '''
   
       
    # Crea el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = formataddr((sender_name, smtp_email))
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Agrega el cuerpo del mensaje
    msText = MIMEText(message, 'html')
    msg.attach(msText)

    # Inicia la conexión al servidor SMTP y envía el mensaje
    smtp = smtplib.SMTP_SSL(smtp_server, smtp_port)
    smtp.login(smtp_email, smtp_password)
    smtp.sendmail(smtp_email, receiver_email, msg.as_string())
    smtp.quit()

@password_reset.post('/password_reset/{email}', response_model=dict, tags=["Password Reset"])
async def createCodeReset(email: str):
    db_user = db.users.find_one({"email": email.lower()})
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Email no registrado en nuestro sistema')
    
    reset_code = generate_token()
    send_reset_email(email,reset_code, db_user["name"])
    current_datetime = datetime.now()
    expiration_datetime = current_datetime + timedelta(hours=1)
    password_reset = PasswordReset(
        email=email,
        token=reset_code,
        expires=expiration_datetime
        )
    del password_reset.id
    print(password_reset.dict())
    db.password_resets.insert_one(password_reset.dict())
    
    return {"message": "código de recuperación enviado."}

@password_reset.post("/change_password/", response_model=dict, tags=["Password Reset"])
async def change_password(change_password: ChangePassword):
    token = db.password_resets.find_one({"token": change_password.token})
    password = change_password.password
    if not token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Codigo no válido')

    if token['expires'] < datetime.now():
        db.password_resets.delete_many({"expires": {"$lt": datetime.now()}})
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='El tiempo de uso del codigo de recuperación se ha terminado')
    else:
        new_password = utils.hash_password(password)
        db.password_resets.delete_one({"_id": ObjectId(token["_id"])})
        db.password_resets.delete_many({"expires": {"$lt": datetime.now()}})
        db.users.update_one({"email":token["email"]}, {"$set": {"password": new_password}})

    return {"message": "Contraseña cambiada satisfactoriamente"}
