from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from app.users.models.users_models import User_Create, Login_User
from app.database.database import get_db
from app.schemas import schemas
from app.utils.hash_generator import hash, verify_hash
from app.middlewares import oauth2


# create an instance of the APIRouter class
router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)

# route to create a new user and login this user, return the token
@router.post("/", response_description="Login a user", response_model=Login_User, status_code=status.HTTP_202_ACCEPTED)
async def create_user(user: User_Create, db: Session = Depends(get_db)):
    user_find = db.query(schemas.User_Schema).filter(schemas.User_Schema.email == user.email).first()
    
    # if the user.email already exists in the database, login the user
    if user_find:
        return await login(username=user_find.email, password=user.sub, db=db)

    # save the user sub without hashing
    original_sub = user.sub

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

    # login the user
    return await login(username=new_user.email, password=original_sub, db=db)


# function to login a user
async def login(username: str, password: str, db: Session = Depends(get_db)):
    # find if the user exists in the database
    user = db.query(schemas.User_Schema).filter(schemas.User_Schema.email == username).first()

    # if the user.email does not exist in the database, raise an error
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid email")
    
    # if the password does not match the user.sub, raise an error
    if not verify_hash(password.lstrip().rstrip(), user.sub):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid sub")
    
    #create a token
    access_token = oauth2.create_access_token(data={"user_id": str(user.id)})

    return {"access_token": access_token, "user": user, "token_type": "bearer"}