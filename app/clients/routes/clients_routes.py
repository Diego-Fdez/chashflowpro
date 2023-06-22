from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from typing import Optional
from app.clients.models.clients_models import Client_Create, Client_Model, Client_Update
from app.database.database import get_db
from app.schemas import schemas
from app.middlewares import oauth2

# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/clients",
    tags=["Clients"],
    responses={404: {"description": "Not found"}}
)

# define a route and function to create a new client
@router.post("/", response_description="Create a new client", response_model=Client_Model,
              summary="Create a new client", status_code=status.HTTP_201_CREATED)
async def create_client(client: Client_Create, db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    # convert the client object to a dictionary
    new_client = schemas.Client_Schema(user_id=current_user.id, **client.dict())
    # save the new client to the database
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client