from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import uuid
from typing import Optional
from app.users.models.users_models import User_Model, Update_User
from app.database.database import get_db
from app.schemas import schemas
from app.middlewares import oauth2


# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)


# define a route to get user by id
@router.get("/{user_id}", response_description="Get user detail", response_model=User_Model, 
            status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: uuid.UUID, db: Session = Depends(get_db),
                            current_user: int = Depends(oauth2.get_current_user)):
    user = db.query(schemas.User_Schema).filter(schemas.User_Schema.id == user_id).first()
    # if user is None return an exception:
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {user_id} not found")
    
    # if the user is not the current_user or is not superuser return an exception:
    if (user.id != current_user.id) | (not user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Only the user can access this route")
    
    return user


# define a route to update all users
@router.get("/", response_description="Get all users", response_model=list[User_Model], 
            status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 50, skip: int = 0, search: Optional[str] = ""):
    # search if the current_user is superuser
    is_superuser = db.query(schemas.User_Schema).filter(schemas.User_Schema.id == current_user.id).first().is_superuser
    
    # if current_user is not superuser return an exception:
    if not is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Only superusers can access this route")
    
    # query the database for all users, limit, skip offset the results and search by username
    users = db.query(schemas.User_Schema).filter(schemas.User_Schema.username.contains(search)).limit(
        limit).offset(skip).all()
    # if users is None or [] return an exception:
    if users == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No users found")
    
    return users


# define route and function to deactivate user
@router.patch("/deactivate/{user_id}", response_description="Deactivate user", status_code=status.HTTP_200_OK)
async def deactivate_user(user_id: uuid.UUID, db: Session = Depends(get_db),
                            current_user: int = Depends(oauth2.get_current_user)):
    find_user = db.query(schemas.User_Schema).filter(schemas.User_Schema.id == user_id)
    user = find_user.first()

    if (user.id != current_user.id) | (not user.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action, only the user can perform this action")
    
    find_user.update({"is_active": False}, synchronize_session=False)
    db.commit()

    return {"message": "User deactivated successfully"}


# define route and function to update user
@router.patch("/{user_id}", response_description="Update user", response_model=User_Model, status_code=status.HTTP_200_OK)
async def update_user(user_id: uuid.UUID, user: Update_User, db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    # find the user to update by id
    find_user = db.query(schemas.User_Schema).filter(schemas.User_Schema.id == user_id)
    user_to_update = find_user.first()

    # if user_to_update is not the current_user or is not superuser return an exception:
    if (user_to_update.id != current_user.id) | (not user_to_update.is_superuser):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action, only the user can perform this action")
    
    # if the user is not updating his/her own username or phone number, use data from the user into DB:
    if (not user.username) | (user.username == ""):
        user.username = user_to_update.username

    if (not user.phone_number) | (user.phone_number == ""):
        user.phone_number = user_to_update.phone_number
    
    # update the user in the database:
    find_user.update(user.dict(), synchronize_session=False)
    db.commit()

    # return the updated user:
    return find_user.first()