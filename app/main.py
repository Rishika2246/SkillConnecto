from telnetlib import STATUS
from fastapi import FastAPI, Depends, HTTPException, Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
import crud
import schemas
from database import db
from fastapi.middleware.cors import CORSMiddleware
import requests
from bson import ObjectId
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.orm import Session


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# @app.post("/signup", response_model=schemas.Token)
# async def signup(user_create: schemas.UserCreate, db: AsyncSession = Depends(db)):
#     # Check if the username already exists
#     existing_user = await crud.get_user_by_username(db, username=user_create.username)
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Username already registered")

#     # Create a new user in the database
#     hashed_password = crud.hash_password(user_create.password)  # Implement this function to hash the password
#     new_user = await crud.create_user(db, username=user_create.username, email=user_create.email, hashed_password=hashed_password)

#     # Generate an access token for the newly registered user
#     access_token = create_access_token(data={"sub": new_user.username})
    
#     return {"access_token": access_token, "token_type": "bearer"}
@app.post("/register", response_model=schemas.User)
async def register(username: str = Form(...), password: str = Form(...)):
    user_create = schemas.UserCreate(username=username, password=password)
    db_user = await crud.get_user_by_username(db, username=username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await crud.create_user(db, user_create)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user_by_username(db, username=form_data.username)
    if not user or not crud.verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/courses")
async def read_courses(current_user: schemas.User = Depends(get_current_user)):
    return {"message": "Welcome to the Python course!", "user": current_user["username"]}

RECAPTCHA_SECRET_KEY = "6LcwkkIqAAAAAJv1XGeo4BkSnEcJvRpYi98AMr--"

@app.post("/verify-captcha")
async def verify_captcha(recaptcha_response: str = Form(...)):
    data = {
        'secret': "6LcwkkIqAAAAAJv1XGeo4BkSnEcJvRpYi98AMr--",
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()

    if result.get('success'):
        return {"message": "CAPTCHA passed, proceeding to next page"}
    else:
        return {"error": "Invalid CAPTCHA, please try again"}

def convert_to_dicts(data):
    if isinstance(data, list):
        return [item.dict() if hasattr(item, 'dict') else item for item in data]
    if hasattr(data, 'dict'):
        return data.dict()
    return data

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_user_from_db(username: str):
    user = await db["users"].find_one({"username": username})
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code= STATUS.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    
    except JWTError:
        raise credentials_exception
    user = await get_user_from_db(token_data.username)
    if user is None:
        raise credentials_exception 

    return user
@app.put("/profile")
async def edit_profile(updated_data: schemas.Profile, current_user: dict = Depends(get_current_user)):
    updated_data_dict = convert_to_dicts(updated_data.dict())
    await db["users"].update_one(
        {"username": current_user["username"]},
        {"$set": updated_data_dict}
    )

    return {"message": "Profile updated successfully"}









AUTHORIZATION = '1YZj5zaOP3V5z3EONayTpHDHu5E5WX3n'
BASE_URL = 'https://api-preproduction.signzy.app/api/v3'

class AadhaarRequest(BaseModel):
    aadhaarNumber: str

class OtpVerification(BaseModel):
    requestId: str
    otp: str
    isAadhaarMasked: bool = False

@app.post("/send-otp")
async def send_otp(aadhaar: AadhaarRequest):
    url = f"{BASE_URL}/getOkycOtp"
    headers = {
        'Authorization': AUTHORIZATION,
        'Content-Type': 'application/json'
    }
    payload = {"aadhaarNumber": aadhaar.aadhaarNumber}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to send OTP")
@app.post("/verify-otp")
async def verify_otp(otp_data: OtpVerification):
    url = f"{BASE_URL}/fetchOkycData"
    headers = {
        'Authorization': AUTHORIZATION,
        'Content-Type': 'application/json'
    }
    payload = {
        "requestId": otp_data.requestId,
        "otp": otp_data.otp,
        "isAadhaarMasked": otp_data.isAadhaarMasked
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="OTP Verification Failed")

fake_job_db = [
    {"job_title": "Software Engineer", "company": "Tech Corp", "duration": "2 years", "responsibilities": "Developing web applications"},
    {"job_title": "Data Scientist", "company": "Data Analytics Inc.", "duration": "1.5 years", "responsibilities": "Building ML models"},
    {"job_title": "DevOps Engineer", "company": "Cloud Solutions", "duration": "3 years", "responsibilities": "Managing CI/CD pipelines"},
]

@app.get("/profile-page", response_model=dict)
async def get_profile(current_user: schemas.TokenData = Depends(get_current_user)):
    user_profile = db.get(current_user.username)
    if user_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return user_profile
