from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(sub: str):
    return pwd_context.hash(sub)


def verify_hash(plain_sub, hashed_sub):
    return pwd_context.verify(plain_sub, hashed_sub)