import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "test_db")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")


class Settings():

    JWT_SECRET_KEY="b8f9d2c4e6a1f7b9d3e5c8a0f2b4d6e8c1a3f5b7d9e2c4a6f8b0d2e4f6a8c0b2"

    JWT_ALGORITHM="HS256"

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES=300

    JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
