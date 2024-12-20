from fastapi import APIRouter, HTTPException
from datetime import datetime

# Create a router instance
router = APIRouter()

# Sample order data (for demonstration; replace with database integration)
orders = []

# Place a new order
@router.post("/")
async def place_order(user_id: int, items: list[dict], total_price: float):
    """
    items: List of dictionaries with keys: product_id, quantity
    """
    if not items:
        raise HTTPException(status_code=400, detail="Order must contain at least one item.")

    new_order = {
        "order_id": len(orders) + 1,
        "user_id": user_id,
        "items": items,
        "total_price": total_price,
        "status": "Pending",
        "order_date": datetime.now(),
    }
    orders.append(new_order)
    return {"message": "Order placed successfully", "order": new_order}

# View all orders
@router.get("/")
async def get_all_orders():
    if not orders:
        return {"message": "No orders available"}
    return {"orders": orders}

# View an order by ID
@router.get("/{order_id}")
async def get_order_by_id(order_id: int):
    order = next((order for order in orders if order["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    return {"order": order}

# Update the status of an order
@router.put("/{order_id}/status")
async def update_order_status(order_id: int, status: str):
    order = next((order for order in orders if order["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    
    order["status"] = status
    return {"message": "Order status updated successfully", "order": order}

# Cancel an order
@router.delete("/{order_id}")
async def cancel_order(order_id: int):
    global orders
    order = next((order for order in orders if order["order_id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")
    
    if order["status"] in ["Shipped", "Delivered"]:
        raise HTTPException(status_code=400, detail="Cannot cancel an order that has already been shipped or delivered.")
    
    orders = [o for o in orders if o["order_id"] != order_id]
    return {"message": f"Order {order_id} canceled successfully"}
