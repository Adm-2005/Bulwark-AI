import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/defaultdb')
    JWT_SECRET = os.getenv('JWT_SECRET', 'aslkdfjawoeijqo4eij')
    SECRET_KEY = os.getenv('SECRET_KEY', 'zdskaoisefoewqweorwejakldsfawoeiiq132416459844i3dzk')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 18000))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_REFRESH_EXPIRES', 86400))