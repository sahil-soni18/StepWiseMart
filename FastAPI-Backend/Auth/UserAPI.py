from fastapi import APIRouter, Depends
from db.database import get_db, Session
from models.User import User
from Schemas.UserSchema import *
from Utils import JWTBearer

userRouter = APIRouter()

@userRouter.put("/user/{userId}", response_model=UserOut)
async def profileUpdate(userId: int, userData: UserUpdate, token: dict = Depends(JWTBearer()), db: Session = Depends(get_db)):
    user_id = token.get('user_id')
    if not user_id:
        return {"error": "Invalid token"}
    
    try:
        user = db.query(User).filter(User.id == userId).first()
        if user:

            for key, value in userData.model_dump(exclude_unset=True).items():
                setattr(user, key, value)

            db.commit()
            db.refresh(user)
            return user
        
    except Exception as e:
        return {"error": str(e)}