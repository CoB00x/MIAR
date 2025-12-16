from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .database import get_db
from . import models, schemas

router = APIRouter(prefix="/api", tags=["amenities"])

# Amenity Endpoints
@router.get("/amenities", response_model=List[schemas.AmenityResponse])
def get_amenities(
    category: str = None,
    available: bool = True,
    db: Session = Depends(get_db)
):
    """Get list of amenities with optional filtering"""
    query = db.query(models.Amenity)
    
    if available:
        query = query.filter(models.Amenity.available == True)
    
    if category:
        query = query.filter(models.Amenity.category == category)
    
    return query.order_by(models.Amenity.category, models.Amenity.name).all()

@router.post("/amenities", response_model=schemas.AmenityResponse)
def create_amenity(amenity: schemas.AmenityCreate, db: Session = Depends(get_db)):
    """Create new amenity (admin only)"""
    db_amenity = models.Amenity(**amenity.dict())
    db.add(db_amenity)
    db.commit()
    db.refresh(db_amenity)
    return db_amenity

# Amenity Order Endpoints
@router.post("/amenity-orders", response_model=schemas.AmenityOrderResponse)
def create_amenity_order(order: schemas.AmenityOrderCreate, db: Session = Depends(get_db)):
    """Create new amenity order"""
    # Get amenity details
    amenity = db.query(models.Amenity).filter(
        models.Amenity.id == order.amenity_id,
        models.Amenity.available == True
    ).first()
    
    if not amenity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Amenity not found or unavailable"
        )
    
    # Create order
    db_order = models.AmenityOrder(
        guest_id=order.guest_id,
        guest_name=order.guest_name,
        amenity_id=amenity.id,
        amenity_name=amenity.name,
        total_amount=amenity.price,
        scheduled_for=order.scheduled_for,
        guest_notes=order.guest_notes,
        status="requested"
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return {
        "order_id": db_order.id,
        "amenity_name": amenity.name,
        "status": db_order.status,
        "total_amount": amenity.price,
        "message": "Amenity order created successfully"
    }

@router.get("/amenity-orders/{order_id}", response_model=schemas.AmenityOrderDetail)
def get_amenity_order(order_id: str, db: Session = Depends(get_db)):
    """Get amenity order details"""
    order = db.query(models.AmenityOrder).filter(models.AmenityOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Amenity order not found")
    return order

@router.get("/amenity-orders", response_model=List[schemas.AmenityOrderDetail])
def list_amenity_orders(
    guest_id: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """List amenity orders with optional filtering"""
    query = db.query(models.AmenityOrder)
    
    if guest_id:
        query = query.filter(models.AmenityOrder.guest_id == guest_id)
    
    if status:
        query = query.filter(models.AmenityOrder.status == status)
    
    return query.order_by(models.AmenityOrder.created_at.desc()).all()

@router.patch("/amenity-orders/{order_id}/assign", response_model=schemas.AmenityOrderDetail)
def assign_amenity_order(
    order_id: str,
    assignment: schemas.AssignmentRequest,
    db: Session = Depends(get_db)
):
    """Assign staff member to amenity order"""
    order = db.query(models.AmenityOrder).filter(models.AmenityOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Amenity order not found")
    
    if order.status == "completed":
        raise HTTPException(status_code=400, detail="Cannot assign completed order")
    
    order.assigned_to = assignment.staff_id
    order.assigned_to_name = assignment.staff_name
    order.status = "assigned"
    order.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(order)
    
    return order

@router.patch("/amenity-orders/{order_id}/status", response_model=schemas.AmenityOrderDetail)
def update_amenity_order_status(
    order_id: str,
    status_update: schemas.StatusUpdate,
    db: Session = Depends(get_db)
):
    """Update amenity order status"""
    order = db.query(models.AmenityOrder).filter(models.AmenityOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Amenity order not found")
    
    valid_statuses = ["requested", "assigned", "in_progress", "completed", "cancelled"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    order.status = status_update.status
    order.updated_at = datetime.utcnow()
    
    # Set completed_at timestamp if status is completed
    if status_update.status == "completed":
        order.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(order)
    
    return order

@router.patch("/amenity-orders/{order_id}/complete", response_model=schemas.AmenityOrderDetail)
def complete_amenity_order(
    order_id: str,
    completion: schemas.CompletionRequest,
    db: Session = Depends(get_db)
):
    """Mark amenity order as completed"""
    order = db.query(models.AmenityOrder).filter(models.AmenityOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Amenity order not found")
    
    order.status = "completed"
    order.staff_notes = completion.notes
    order.completed_at = datetime.utcnow()
    order.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(order)
    
    return order