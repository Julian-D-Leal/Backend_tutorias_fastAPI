from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from auth import AuthJWT
from azure.storage.blob import BlobServiceClient
from config.config import settings
from config.db import db
import magic

blob1 = APIRouter()
blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_STORAGE_CONNECTION_STRING)
KB = 1024
MB = 1024 * KB


SUPPORTED_FILES_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'image/jpg': 'jpg',
}


@blob1.post('/blobs/upload/{email}', response_model=dict, status_code=status.HTTP_200_OK, tags=["Blobs"])
async def create_upload_file(email: str,file: UploadFile = File(...), Authorize: AuthJWT = Depends()):
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

    return await uploadToAzure(email,file)


async def uploadToAzure(email: str,file: UploadFile = File(...)):
   
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='No se ha enviado ningún archivo'
        )
    
    container_name = 'tutoriapp'
    content = await file.read()
    size = len(content)

    if not 0 < size <= 5 * MB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='El tamaño del archivo debe ser menor a 5MB'
        )
    
    file_type = magic.from_buffer(content, mime=True)

    if file_type not in SUPPORTED_FILES_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='El archivo debe ser de tipo PNG, jpge o jpg'
        )
    
    with blob_service_client:
        container_client = blob_service_client.get_container_client(container_name)
        try:
            file.filename = f'{email.lower()}.{SUPPORTED_FILES_TYPES[file_type]}'
            blob_client = container_client.get_blob_client(file.filename)
            
            blob_client.upload_blob(content, overwrite=True)
        except Exception as e:
            error = e.__class__.__name__
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    
    db.users.find_one_and_update({"email": email}, {"$set": {"image_url": blob_client.url}})

    return {"message": "Imagen guardada con éxito", "url": blob_client.url}

