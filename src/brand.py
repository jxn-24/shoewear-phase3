from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from .base import Base

class Brand(Base):
    __tablename__ = "brands"
    
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    products = relationship("Product", back_populates="brand")
    
    def __repr__(self):
        return f"<Brand {self.name}>"
    
    @classmethod
    def create(cls, db, name, description=None):
        if not name:
            raise ValueError("Brand name cannot be empty")
        if len(name) > 100:
            raise ValueError("Brand name cannot exceed 100 characters")
            
        brand = cls(name=name, description=description)
        return brand.save(db)
    
    @classmethod
    def find_by_name(cls, db, name):
        return db.query(cls).filter(cls.name == name).first()