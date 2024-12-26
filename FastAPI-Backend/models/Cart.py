from ..db.database import Base
from sqlalchemy import Column, JSON, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    items = Column(JSON, nullable=True)  
    total_price = Column(Integer, default=0)

    user = relationship("User", back_populates="cart")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id}, items={self.items})>"
    


