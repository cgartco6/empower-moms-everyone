from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    category = Column(String)  # trending, traditional, rare, dying
    is_free = Column(Boolean, default=False)
    price_zar = Column(Float, nullable=True)   # South African Rand
    price_usd = Column(Float, nullable=True)   # US Dollars
    intro_to_course_id = Column(Integer, ForeignKey('courses.id'), nullable=True)
    modules = relationship("Module", back_populates="course")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @property
    def display_price(self, currency='ZAR'):
        if self.is_free:
            return 0
        if currency.upper() == 'ZAR':
            return self.price_zar
        else:
            return self.price_usd
