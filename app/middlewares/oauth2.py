from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.database import database
from app.config import configs
from app.auth.models import auth_models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth")

#expiration time
ACCESS_TOKEN_EXPIRE_DAYS = 15

#Secret_key
SECRET_KEY = configs.settings.secret_key

#algorithm
ALGORITHM = configs.settings.algorithm

# function to create access token
def create_access_token(data: dict):
    # copy data to new dic
    to_encode = data.copy()

    # add expiration time
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)

    # update dic with expiration time
    to_encode.update({"exp": expire})

    # encode dic with secret key and algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # return encoded_jwt
    return encoded_jwt


# function to verify access token
def verify_access_token(token: str, credentials_exception):
    try:
        # decode token with secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # get id from payload
        id: str = payload.get("user_id")

        # if id is None, raise exception
        if id is None:
            raise credentials_exception
        
        # return token data
        token_data = auth_models.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    

# function to get current user from token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    # verify access 
    token = verify_access_token(token, credentials_exception)

    # get user from db, compare id from token and db
    user = db.query(schemas.User_Schema).filter(schemas.User_Schema.id == token.id).first()
    
    # return user
    return user