from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Relates to User
    # cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)  # Relates to Cart
    total_price = Column(Float, nullable=False)  # Total price of the order
    status = Column(String, default="pending")  # Order status (e.g., pending, completed, canceled)
    payment_status = Column(String, default="unpaid")  # Payment status
    created_at = Column(DateTime, default=datetime.utcnow)  # When the order was placed
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # When the order was last updated

    # Relationships
    user = relationship("User", back_populates="orders")  # User who placed the order
    payment = relationship("Payment", back_populates="order", uselist=False)

    # cart = relationship("Cart", back_populates="order")  # Cart associated with the order
    # Add Product relationship if you store products directly in the order
    # products = relationship("Product", secondary="order_products")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total_price={self.total_price}, status={self.status})>"
