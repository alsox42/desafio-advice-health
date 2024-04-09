import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:postgres@127.0.0.1/db_nork_town')
    SQLALCHEMY_TRACK_MODIFICATIONS = False