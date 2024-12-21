from fastapi import FastAPI
from routers import profile, orders, product, cart, category, address

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the StepWiseMart"}

# Include routers for different modules
app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(product.router, prefix="/product", tags=["Product"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])
app.include_router(category.router, prefix="/category", tags=["Category"])
app.include_router(address.router, prefix="/address", tags=["Address"])
