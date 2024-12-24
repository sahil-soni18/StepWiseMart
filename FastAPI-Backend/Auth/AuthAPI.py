from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from db.database import get_db, Session
from models.User import User
# from fastapi.security import OAuth2PasswordRequestForm    # For UserName and password authentication only.
from Schemas.AuthSchemas import UserCred, UserInDB, Token
from Utils import verify_password, get_password_hash, create_access_token
from datetime import datetime, timedelta, timezone
from Schemas.UserSchema import UserOut, UserCreate

authRouter = APIRouter()


# Login endpoint

@authRouter.post('/login', response_model=bool)
async def login( response: Response, userCredentails: UserCred, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == userCredentails.email).first()

    if user:
        if verify_password(userCredentails.password, user.password_hash):
            access_token = create_access_token(data={"sub": userCredentails.email})
            access_token = access_token.decode("utf8")

            response.set_cookie(
                key="AccessToken",
                value=access_token,
                httponly=True,
                max_age=int(timedelta(hours=1).total_seconds()),
                expires=datetime.now(timezone.utc) + timedelta(hours=1)
            )

            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            


# Signup Endpoint

@authRouter.post('/signup', response_model=UserOut)
async def signup(response: Response, userData: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == userData.email).first()

    if not user:
        try:
            hashed_password = get_password_hash(userData.password)
            newUser = User(
                name = userData.name,
                email = userData.email,
                password_hash = hashed_password,
                address = userData.address,
                contact = userData.contact,
                is_admin = userData.is_admin,
                created_at = datetime.now(),
                updated_at = datetime.now()
            )

            db.add(newUser)
            db.commit()
            db.refresh(newUser)

            access_token = create_access_token(data={"sub": newUser.email})
            access_token = access_token.decode("utf8")

            response.set_cookie(
                key="AccessToken",
                value=access_token,
                httponly=True,
                max_age=int(timedelta(hours=1).total_seconds()),
                expires=datetime.now(timezone.utc) + timedelta(hours=1)
            )

            return UserOut(**newUser.dict())

        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error while creating user: {str(e)}")
        
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")




# Logout endpoint

@authRouter.post('/logout')
async def logout(response: Response):
    response.delete_cookie("AccessToken")
    return {"message": "Logged out successfully"}