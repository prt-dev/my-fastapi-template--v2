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
REMOTE_UPLOAD_API_URL = os.getenv("REMOTE_UPLOAD_API_URL", "https://apiapp.hotelmahalaiims.com/upload.php")
REMOTE_UPLOAD_BASE_URL = os.getenv("REMOTE_UPLOAD_BASE_URL", "https://apiapp.hotelmahalaiims.com")


RAZORPAY_KEY_ID=os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET=os.getenv('RAZORPAY_KEY_SECRET')

class Settings():

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', '')

    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES') or 30)

    JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRE_DAYS') or 7)
