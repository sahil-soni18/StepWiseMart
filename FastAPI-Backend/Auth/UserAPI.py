from fastapi import APIRouter, Depends, HTTPException, status
from db.database import get_db, Session
from models.User import User
from Schemas.UserSchema import *
from .Utils import JWTBearer, get_password_hash

userRouter = APIRouter()

@userRouter.put("/user/{userId}", response_model=UserOut)
async def profileUpdate(userId: int, userData: UserUpdate, token: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    email = token.get('email')
    print("------------------DEBUGGING-------------------")
    print(f"User Id: {email}")
    print(f"Token: {token}")
    print(f"User Data: {userData}")
    print("------------------DEBUGGING-------------------")
    
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    try:
        user = db.query(User).filter(User.id == userId).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Check if the userId matches the token userId (optional, for security)
        if user.email != email:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")

        # Update the user fields based on the userData
        for key, value in userData.model_dump(exclude_unset=True).items():
            if key == "password" and value:  # If password is being updated, hash it
                print("-------------------- Updating password ---------------------------")
                print(f"Key: {key} Value: {value}...")
                value = get_password_hash(value)
                print(f"Hashed Password: {value}")
            setattr(user, key, value)

        print(f" User: {user.password}")

        # db.add(user)
        db.commit()
        db.refresh(user)
        
        return user  # Return updated user as UserOut

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {str(e)}")




# "$2b$12$duzpIV2WVEkyl9ZmJDlgeuoXYYCXODb6iNuoS7n2DS4FoVEZ4HJvq"
# "$2b$12$e0k6LTrrdRsLFm85MjheB.WhRW44RUDIgSBDDs8Iqpxa776KOiN4W"