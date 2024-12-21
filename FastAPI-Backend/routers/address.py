from fastapi import APIRouter, HTTPException

# Create a router instance
router = APIRouter()

# In-memory storage for addresses
addresses = []

# Add a new address
@router.post("/addresses/add")
async def add_address(user_id: int, street: str, city: str, state: str, zipcode: str):
    if not (street.strip() and city.strip() and state.strip() and zipcode.strip()):
        raise HTTPException(status_code=400, detail="All address fields must be provided and not empty.")
    
    # Generate a unique ID for the address
    address_id = len(addresses) + 1
    new_address = {"id": address_id, "user_id": user_id, "street": street, "city": city, "state": state, "zipcode": zipcode}
    addresses.append(new_address)
    return {"message": "Address added", "address": new_address}

# View all addresses
@router.get("/addresses/view")
async def view_addresses():
    if not addresses:
        return {"message": "No addresses available"}
    return {"addresses": addresses}

# Update an address
@router.put("/addresses/update/{address_id}")
async def update_address(address_id: int, street: str = None, city: str = None, state: str = None, zipcode: str = None):
    # Find the address by ID
    address = next((addr for addr in addresses if addr["id"] == address_id), None)
    if not address:
        raise HTTPException(status_code=404, detail="Address not found.")
    
    # Update only provided fields
    if street is not None: address["street"] = street
    if city is not None: address["city"] = city
    if state is not None: address["state"] = state
    if zipcode is not None: address["zipcode"] = zipcode
    
    return {"message": "Address updated", "address": address}

# Remove an address
@router.delete("/addresses/delete/{address_id}")
async def remove_address(address_id: int):
    global addresses
    addresses = [addr for addr in addresses if addr["id"] != address_id]
    return {"message": f"Address with ID {address_id} removed", "addresses": addresses}

# Clear all addresses
@router.delete("/addresses/clear")
async def clear_addresses():
    global addresses
    addresses = []
    return {"message": "All addresses cleared", "addresses": addresses}
