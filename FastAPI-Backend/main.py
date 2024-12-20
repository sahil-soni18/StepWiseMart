from fastapi import FastAPI
from routers import profile, orders, product, cart


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the StepWiseMart"}


app.include_router(profile.router, prefix="/profile", tags=["Profile"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(product.router, prefix="/product", tags=["Product"])
app.include_router(cart.router, prefix="/cart", tags=["Cart"])