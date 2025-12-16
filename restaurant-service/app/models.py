from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, JSON, Text
from .database import Base
import uuid
from datetime import datetime

class MenuItem(Base):
    __tablename__ = "menu_items"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    available = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)
    preparation_time = Column(Integer, default=15)  # minutes
    created_at = Column(DateTime, default=datetime.utcnow)

class RestaurantOrder(Base):
    __tablename__ = "restaurant_orders"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guest_id = Column(String, nullable=False)
    room_number = Column(String)
    order_type = Column(String)  # room_service, in_restaurant
    items = Column(JSON)  # List of {menu_item_id, name, quantity, price, item_total}
    status = Column(String, default="received")  # received, in_progress, ready, delivered, cancelled
    total_amount = Column(Float)
    special_requests = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class TableReservation(Base):
    __tablename__ = "table_reservations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    guest_id = Column(String, nullable=False)
    guest_name = Column(String, nullable=False)
    persons_count = Column(Integer, nullable=False)
    reservation_date = Column(String, nullable=False)  # YYYY-MM-DD
    reservation_time = Column(String, nullable=False)  # HH:MM
    table_number = Column(Integer)
    status = Column(String, default="confirmed")  # confirmed, cancelled, completed
    special_requests = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)