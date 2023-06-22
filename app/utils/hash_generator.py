from passlib.context import CryptContext

# This is a class that will be used to hash passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This function will take a string and return a hashed version of it
def hash(sub: str):
    return pwd_context.hash(sub)

# This function will take a string and a hashed string and return a boolean,
#verifying that the string is the same as the hashed string
def verify_hash(plain_sub, hashed_sub):
    return pwd_context.verify(plain_sub, hashed_sub)