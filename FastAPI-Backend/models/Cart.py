from ..db.database import Base
from sqlalchemy import Column, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    items = Column(JSON, nullable=True)  

    user = relationship("User", back_populates="cart")

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id}, items={self.items})>"
    


# cart = Cart(
#     id=1,
#     user_id=101,
#     items=[
#         {"product_id": 1, "quantity": 2},
#         {"product_id": 3, "quantity": 1}
#     ]
# )