from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Text
from .database import Base
import uuid
from datetime import datetime

class Amenity(Base):
    __tablename__ = "amenities"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String)  # transport, spa, tour, equipment, other
    duration_minutes = Column(Integer)  # Estimated duration in minutes
    available = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AmenityOrder(Base):
    __tablename__ = "amenity_orders"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guest_id = Column(String, nullable=False)
    guest_name = Column(String)
    amenity_id = Column(String, nullable=False)
    amenity_name = Column(String)
    status = Column(String, default="requested")  # requested, assigned, in_progress, completed, cancelled
    total_amount = Column(Float)
    scheduled_for = Column(DateTime)
    assigned_to = Column(String)  # staff_id
    assigned_to_name = Column(String)  # staff name
    guest_notes = Column(Text)
    staff_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime)