from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Amenity Schemas
class AmenityBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    duration_minutes: int
    available: bool = True
    image_url: Optional[str] = None

class AmenityCreate(AmenityBase):
    pass

class AmenityResponse(AmenityBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Amenity Order Schemas
class AmenityOrderCreate(BaseModel):
    guest_id: str
    guest_name: Optional[str] = None
    amenity_id: str
    scheduled_for: datetime
    guest_notes: Optional[str] = None

class AmenityOrderResponse(BaseModel):
    order_id: str
    amenity_name: str
    status: str
    total_amount: float
    assigned_to: Optional[str] = None
    message: str

class AmenityOrderDetail(BaseModel):
    id: str
    guest_id: str
    guest_name: Optional[str]
    amenity_id: str
    amenity_name: str
    status: str
    total_amount: float
    scheduled_for: datetime
    assigned_to: Optional[str]
    assigned_to_name: Optional[str]
    guest_notes: Optional[str]
    staff_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

# Assignment Schemas
class AssignmentRequest(BaseModel):
    staff_id: str
    staff_name: str

class CompletionRequest(BaseModel):
    notes: Optional[str] = None

# Status Update Schemas
class StatusUpdate(BaseModel):
    status: str