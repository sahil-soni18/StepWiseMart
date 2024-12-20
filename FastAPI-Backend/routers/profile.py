from fastapi import APIRouter, HTTPException

# Create a router instance
router = APIRouter()

# Sample user profiles (for demonstration; replace with database integration)
profiles = {}

# Create a new profile
@router.post("/")
async def create_profile(user_id: int, name: str, email: str, age: int = None):
    """
    Create a new user profile.
    """
    if user_id in profiles:
        raise HTTPException(status_code=400, detail="Profile already exists for this user ID.")
    
    profiles[user_id] = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "age": age,
    }
    return {"message": "Profile created successfully", "profile": profiles[user_id]}

# Get a profile by user ID
@router.get("/{user_id}")
async def get_profile(user_id: int):
    """
    Retrieve a user profile by user ID.
    """
    profile = profiles.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return {"profile": profile}

# Update an existing profile
@router.put("/{user_id}")
async def update_profile(user_id: int, name: str = None, email: str = None, age: int = None):
    """
    Update a user's profile.
    """
    profile = profiles.get(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    
    if name:
        profile["name"] = name
    if email:
        profile["email"] = email
    if age is not None:
        profile["age"] = age

    return {"message": "Profile updated successfully", "profile": profile}

# Delete a profile
@router.delete("/{user_id}")
async def delete_profile(user_id: int):
    """
    Delete a user profile by user ID.
    """
    if user_id not in profiles:
        raise HTTPException(status_code=404, detail="Profile not found.")
    
    del profiles[user_id]
    return {"message": f"Profile for user ID {user_id} deleted successfully"}
