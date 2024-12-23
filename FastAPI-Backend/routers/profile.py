# from fastapi import APIRouter, HTTPException

# # Create a router instance
# router = APIRouter()

# # Sample user profiles (for demonstration; replace with database integration)
# profiles = {}

# # Create a new profile
# @router.post("/profile")
# async def create_profile(user_id: int, name: str, email: str, age: int = None):
#     """
#     Create a new user profile.
#     """
#     if user_id in profiles:
#         raise HTTPException(status_code=400, detail="Profile already exists for this user ID.")
    
#     profiles[user_id] = {
#         "user_id": user_id,
#         "name": name,
#         "email": email,
#         "age": age,
#     }
#     return {"message": "Profile created successfully", "profile": profiles[user_id]}

# # Get a profile by user ID
# @router.get("/profile/{user_id}")
# async def get_profile(user_id: int):
#     """
#     Retrieve a user profile by user ID.
#     """
#     profile = profiles.get(user_id)
#     if not profile:
#         raise HTTPException(status_code=404, detail="Profile not found.")
#     return {"profile": profile}

# # Update an existing profile
# @router.put("/profile/{user_id}")
# async def update_profile(user_id: int, name: str = None, email: str = None, age: int = None):
#     """
#     Update a user's profile.
#     """
#     profile = profiles.get(user_id)
#     if not profile:
#         raise HTTPException(status_code=404, detail="Profile not found.")
    
#     if name:
#         profile["name"] = name
#     if email:
#         profile["email"] = email
#     if age is not None:
#         profile["age"] = age

#     return {"message": "Profile updated successfully", "profile": profile}

# # Delete a profile
# @router.delete("/profile/{user_id}")
# async def delete_profile(user_id: int):
#     """
#     Delete a user profile by user ID.
#     """
#     if user_id not in profiles:
#         raise HTTPException(status_code=404, detail="Profile not found.")
    
#     del profiles[user_id]
#     return {"message": f"Profile for user ID {user_id} deleted successfully"}



from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from models.user import User
from schemas.user_schema import UserCreate, UserOut
from db.database import get_db
from security import hash_password, verify_password

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

    # Hash the password before storing it
    hashed_password = hash_password(user_data.password)

    # Create a new user
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        address=user_data.address,
        contact=user_data.contact,
        is_admin=user_data.is_admin,
        password=hashed_password,
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
        db_user.password = hash_password(user_data.password)

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
