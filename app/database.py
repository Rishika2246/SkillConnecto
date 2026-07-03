# app/database.py

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# import motor.motor_asyncio
# from dotenv import load_dotenv
# import os

# load_dotenv()

# MONGO_DETAILS = os.getenv("MONGO_URI")

# client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
# db = client['bytebreakers']

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DATABASE_URL = "mongodb+srv://user_badri:badri@clusterbytebreakers.nempj.mongodb.net/?retryWrites=true&w=majority&appName=clusterbytebreakers"

client = AsyncIOMotorClient(MONGO_DATABASE_URL)
db = client.bytebreakers 