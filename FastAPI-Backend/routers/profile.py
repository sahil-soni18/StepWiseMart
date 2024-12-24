from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from models.user import User
from schemas.user_schema import UserCreate, UserOut
from db.database import get_db

router = APIRouter()

# Create a new user profile
@router.post("/profile", response_model=UserOut)
def create_user_profile(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        address=user_data.address,
        contact=user_data.contact,
        is_admin=user_data.is_admin,
        password=user_data.password,  # Directly storing the password
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Get a user profile by ID
@router.get("/profile/{user_id}", response_model=UserOut)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update a user profile
@router.put("/profile/{user_id}", response_model=UserOut)
def update_user_profile(
    user_id: int, 
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Optionally update fields
    db_user.name = user_data.name
    db_user.email = user_data.email
    db_user.address = user_data.address
    db_user.contact = user_data.contact
    db_user.is_admin = user_data.is_admin

    if user_data.password:
        # Update password if provided
        db_user.password = user_data.password  # Directly storing the password

    db.commit()
    db.refresh(db_user)
    return db_user

# Delete a user profile
@router.delete("/profile/{user_id}", response_model=UserOut)
def delete_user_profile(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return db_user
