# utils.py
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = "FastAPI-ECommerce-Backend"  # Replace with a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Expiry time for access tokens

# Initialize the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to create JWT access token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash password
def get_password_hash(password):
    return pwd_context.hash(password)
