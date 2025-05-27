from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Product(Base):
    __tablename__ = "products"
    
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    size = Column(Integer, nullable=False)
    color = Column(String(50))
    quantity = Column(Integer, default=0)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    brand = relationship("Brand", back_populates="products")
    
    def __repr__(self):
        return f"<Product {self.name} - {self.brand.name}>"
    
    @classmethod
    def create(cls, db, name, price, size, brand_id, color=None, quantity=0):
        if not name:
            raise ValueError("Product name cannot be empty")
        if price <= 0:
            raise ValueError("Price must be positive")
        if size <= 0:
            raise ValueError("Size must be positive")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
            
        product = cls(
            name=name,
            price=price,
            size=size,
            brand_id=brand_id,
            color=color,
            quantity=quantity
        )
        return product.save(db)
    
    @classmethod
    def find_by_name(cls, db, name):
        return db.query(cls).filter(cls.name.ilike(f"%{name}%")).all()
    
    @classmethod
    def find_by_brand(cls, db, brand_id):
        return db.query(cls).filter(cls.brand_id == brand_id).all()