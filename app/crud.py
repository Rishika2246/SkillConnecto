# # app/crud.py

# from sqlalchemy.orm import Session

# import schemas
# import models
# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def get_user_by_username(db: Session, username: str):
#     return db.query(models.User).filter(models.User.username == username).first()

# def create_user(db: Session, user: schemas.UserCreate):
#     hashed_password = pwd_context.hash(user.password)
#     db_user = models.User(username=user.username, hashed_password=hashed_password)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

from passlib.context import CryptContext
from bson import ObjectId
import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper function to convert MongoDB ObjectId to string
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "hashed_password": user["hashed_password"],
    }

async def get_user_by_username(db, username: str):
    user = await db["users"].find_one({"username": username})
    return user_helper(user) if user else None

async def create_user(db, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    new_user = {
        "username": user.username,
        "hashed_password": hashed_password,
    }
    result = await db["users"].insert_one(new_user)
    created_user = await db["users"].find_one({"_id": result.inserted_id})
    return user_helper(created_user)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
