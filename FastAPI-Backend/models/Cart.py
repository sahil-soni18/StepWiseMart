# models/Cart.py

from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, nullable=False)  # You can also relate this to the 'Product' table if needed
    quantity = Column(Integer, nullable=False)
    
    # Relationships
    cart = relationship("Cart", back_populates="items")
    
    def __repr__(self):
        return f"<CartItem(cart_id={self.cart_id}, product_id={self.product_id}, quantity={self.quantity})>"

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Relates to User
    total_price = Column(Float, nullable=False)  # Total price of the cart
    created_at = Column(DateTime, default=datetime.utcnow)  # When the cart was created
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # When the cart was last updated

    # Relationships
    user = relationship("User", back_populates="cart")  # User who owns the cart
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")  # Cart items
    
    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id}, total_price={self.total_price}, created_at={self.created_at})>"
