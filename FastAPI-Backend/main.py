from fastapi import FastAPI
from routers.cart import cartRouter
from routers.admin import adminRouter
from routers.orders import orderRouter
from routers.payment import paymentRouter
from routers.product import productRouter
from Auth.UserAPI import userRouter
from Auth.AuthAPI import authRouter

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the StepWiseMart"}


app.include_router(paymentRouter, prefix="/payment", tags=["Transaction"])
app.include_router(orderRouter, prefix="/orders", tags=["Orders"])
app.include_router(productRouter, prefix="/product", tags=["Product"])
app.include_router(cartRouter, prefix="/cart", tags=["Cart"])
app.include_router(authRouter, prefix="/auth", tags=["Auth"])
app.include_router(userRouter, prefix="/profile", tags=["Auth"])

app.include_router(adminRouter, prefix="/admin", tags=["Admin"])