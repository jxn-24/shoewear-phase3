from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import as_declarative

@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, index=True)
    
    def save(self, db):
        db.add(self)
        db.commit()
        db.refresh(self)
        return self
    
    def delete(self, db):
        db.delete(self)
        db.commit()
    
    @classmethod
    def get_all(cls, db):
        return db.query(cls).all()
    
    @classmethod
    def find_by_id(cls, db, id):
        return db.query(cls).filter(cls.id == id).first()