from sqlalchemy import Column, Integer, ForeignKey, String, Float, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from db.database import Base


class OrderProduct(Base):
    __tablename__ = "order_products"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationships
    order = relationship("Order", back_populates="products")  # Define relationship to Order
    product = relationship("Product")  # Define relationship to Product

    
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Relates to User
    total_price = Column(Float, nullable=False)  # Total price of the order
    status = Column(String, default="pending")  # Order status (e.g., pending, completed, canceled)
    payment_status = Column(String, default="unpaid")  # Payment status
    created_at = Column(DateTime, default=datetime.utcnow)  # When the order was placed
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # When the order was last updated

    # Relationships
    user = relationship("User", back_populates="orders")  # User who placed the order
    products = relationship("OrderProduct", back_populates="order", cascade="all, delete-orphan")
    payment = relationship("Payment", back_populates="order", uselist=False)  # Payment details

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total_price={self.total_price}, status={self.status})>"
