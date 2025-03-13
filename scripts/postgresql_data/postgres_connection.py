#Import sqlalchemy library's create_engine method 
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

#Load environment variables from .env file
load_dotenv("config/.env.housing")

#Retrieve database credentials from .env file 
DB_USER = (os.getenv("DB_USER"))
DB_PASSWORD = (os.getenv("DB_PASSWORD"))
DB_HOST = (os.getenv("DB_HOST"))
DB_PORT = (os.getenv("DB_PORT"))
DB_NAME = (os.getenv("DB_NAME"))

#Create PostgreSQL database connection engine 
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

#Test whether engine works 
try: 
    with engine.connect() as connection:
        print('Connection was successful')
except Exception as e:
    print(f"Connection failed: {e}")

