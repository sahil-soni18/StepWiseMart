from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, DateTime, JSON
# from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from ..db.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String, nullable=False)
    # category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
 
    image_urls = Column(JSON, nullable=True) 
    colors = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    # category = relationship('Category', back_populates='products')


    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, colors={self.colors})>"