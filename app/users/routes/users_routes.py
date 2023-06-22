from fastapi import APIRouter, status, HTTPException, Response, Depends
from sqlalchemy.orm import Session
from app.users.models.users_models import User_Model, User_Create
from app.database.database import get_db
from app.schemas import schemas
from app.utils.hash_generator import hash, verify_hash


# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)


# define a route to get user by id
@router.get("/{user_id}")
async def get_user_by_id(user_id: int):
    return {"id": id}


# define a route to create a new user
@router.post("/", response_description="Create a new user", response_model=User_Model, 
                status_code=status.HTTP_201_CREATED)
async def create_user(user: User_Create, db: Session = Depends(get_db)):
    #hash the sub - user.sub
    hashed_sub = hash(user.sub)
    user.sub = hashed_sub
    # This creates a new `User_Schema` object with the same data as the
    # `user` object.
    new_user = schemas.User_Schema(**user.dict())
    # This adds the new `User_Schema` object to the database.
    db.add(new_user)
    # This commits the changes to the database.
    db.commit()
    # This refreshes the object in memory with the changes from the database.
    db.refresh(new_user)
    print(type(new_user.id))
    return new_user