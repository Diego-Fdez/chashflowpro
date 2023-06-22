from fastapi import APIRouter, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session
import uuid
from app.users.models.users_models import User_Model
from app.database.database import get_db
from app.schemas import schemas


# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)


# define a route to get user by id
@router.get("/{user_id}", response_description="Get user detail", response_model=User_Model, 
            status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(schemas.User_Schema).filter(schemas.User_Schema.id == user_id).first()
    # if user is None return an exception:
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user_id} not found")
    return user


# define a route to update all users
@router.get("/", response_description="Get all users", response_model=list[User_Model], 
            status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db)):
    # query the database for all users
    users = db.query(schemas.User_Schema).all()
    # if users is None or [] return an exception:
    if users == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No users found")
    
    return users