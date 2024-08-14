from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src import models, schemas
from src.database import get_db
from src.discord import DiscordService, get_discord
from src.helpers import get_category

router = APIRouter()

@router.get("/file")
def get_uploaded_files(db: Annotated[Session, Depends(get_db)]):
    return db.query(models.File).all()

@router.get("/file/{file_id}")
def download_file(file_id: str, discord: Annotated[DiscordService, Depends(get_discord)], db: Annotated[Session, Depends(get_db)]):
    file = db.query(models.File).filter(models.File.id == file_id).first()

    if file == None:
        raise HTTPException(status_code=404, detail="File not found.")

    download_url =  discord.download_url(file.discord_id)

    return RedirectResponse(download_url)

@router.get("/file_url/{file_id}")
def download_url(file_id: str, discord: Annotated[DiscordService, Depends(get_discord)], db: Annotated[Session, Depends(get_db)]):
    file = db.query(models.File).filter(models.File.id == file_id).first()

    if file == None:
        raise HTTPException(status_code=404, detail="File not found.")

    download_url =  discord.download_url(file.discord_id)

    return {
        "url": download_url
    }

@router.delete("/file/{file_id}")
def delete_file(file_id: str, discord: Annotated[DiscordService, Depends(get_discord)], db: Annotated[Session, Depends(get_db)]):
    file = db.query(models.File).filter(models.File.id == file_id).first()

    if file == None:
        raise HTTPException(status_code=404, detail="File not found.")

    if file.deleted_at != None:
        discord.delete(file.discord_id)

        db.query(models.File).filter(models.File.id == file_id).delete()
    else:
        file.deleted_at = datetime.now()

    db.commit()

@router.post("/file", status_code=status.HTTP_201_CREATED)
def upload_file(file: Annotated[UploadFile, File(description="File to be uploaded")], discord: Annotated[DiscordService, Depends(get_discord)], db: Annotated[Session, Depends(get_db)]):
    if file.size == None:
        return HTTPException(status_code=411)

    if file.size > 25_000_000:
        raise HTTPException(status_code=413, detail="Maximum file size is 25MB.")

    data = models.File(
        name = file.filename,
        category = get_category(file.content_type),
        discord_id = discord.upload(file)
    )

    db.add(data)
    db.commit()


@router.patch("/file/{file_id}")
def modify_file(file_id: str, payload: schemas.File, db: Annotated[Session, Depends(get_db)]):
    file = db.query(models.File).filter(models.File.id == file_id).first()

    if file == None:
        raise HTTPException(status_code=404, detail="File not found.")

    file.name = payload.name
    file.category = payload.category

    db.commit()
