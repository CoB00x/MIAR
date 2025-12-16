from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# Menu Schemas
class MenuItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    available: bool = True
    image_url: Optional[str] = None
    preparation_time: int = 15

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemResponse(MenuItemBase):
    id: str
    
    class Config:
        from_attributes = True

class MenuCategory(BaseModel):
    category: str
    items: List[MenuItemResponse]

class MenuResponse(BaseModel):
    categories: Dict[str, List[MenuItemResponse]]

# Order Schemas
class OrderItem(BaseModel):
    menu_item_id: str
    quantity: int

class OrderCreate(BaseModel):
    guest_id: str
    room_number: Optional[str] = None
    order_type: str  # room_service, in_restaurant
    items: List[OrderItem]
    special_requests: Optional[str] = None

class OrderItemResponse(BaseModel):
    menu_item_id: str
    name: str
    quantity: int
    price: float
    item_total: float

class OrderResponse(BaseModel):
    order_id: str
    status: str
    total_amount: float
    currency: str = "RUB"
    estimated_preparation_time: int
    message: str

class OrderDetailResponse(BaseModel):
    id: str
    guest_id: str
    room_number: Optional[str]
    order_type: str
    items: List[OrderItemResponse]
    status: str
    total_amount: float
    special_requests: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Table Reservation Schemas
class TableReservationCreate(BaseModel):
    guest_id: str
    guest_name: str
    persons_count: int
    reservation_date: str  # YYYY-MM-DD
    reservation_time: str  # HH:MM
    special_requests: Optional[str] = None

class TableReservationResponse(BaseModel):
    reservation_id: str
    table_number: int
    status: str
    message: str

class TableReservationDetail(BaseModel):
    id: str
    guest_id: str
    guest_name: str
    persons_count: int
    reservation_date: str
    reservation_time: str
    table_number: Optional[int]
    status: str
    special_requests: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Status Update Schemas
class StatusUpdate(BaseModel):
    status: str