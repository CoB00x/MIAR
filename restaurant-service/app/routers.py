from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from .database import get_db
from . import models, schemas

router = APIRouter(prefix="/api", tags=["restaurant"])

# Menu Endpoints
@router.get("/menu", response_model=schemas.MenuResponse)
def get_menu(db: Session = Depends(get_db)):
    """Get restaurant menu with items grouped by categories"""
    items = db.query(models.MenuItem).filter(models.MenuItem.available == True).all()
    
    # Group items by category
    categories = {}
    for item in items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)
    
    return {"categories": categories}

@router.post("/menu/items", response_model=schemas.MenuItemResponse)
def create_menu_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    """Create new menu item (admin only)"""
    db_item = models.MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Order Endpoints
@router.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """Create new restaurant order"""
    total_amount = 0
    order_items = []
    max_preparation_time = 0
    
    for item in order.items:
        menu_item = db.query(models.MenuItem).filter(
            models.MenuItem.id == item.menu_item_id,
            models.MenuItem.available == True
        ).first()
        
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item {item.menu_item_id} not found or unavailable"
            )
        
        item_total = menu_item.price * item.quantity
        total_amount += item_total
        max_preparation_time = max(max_preparation_time, menu_item.preparation_time)
        
        order_items.append({
            "menu_item_id": menu_item.id,
            "name": menu_item.name,
            "quantity": item.quantity,
            "price": menu_item.price,
            "item_total": item_total
        })
    
    # Create order
    db_order = models.RestaurantOrder(
        guest_id=order.guest_id,
        room_number=order.room_number,
        order_type=order.order_type,
        items=order_items,
        total_amount=total_amount,
        special_requests=order.special_requests,
        status="received"
    )
    
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    return {
        "order_id": db_order.id,
        "status": db_order.status,
        "total_amount": total_amount,
        "estimated_preparation_time": max_preparation_time,
        "message": "Order received successfully"
    }

@router.get("/orders/{order_id}", response_model=schemas.OrderDetailResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    """Get order details"""
    order = db.query(models.RestaurantOrder).filter(models.RestaurantOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/orders/{order_id}/status", response_model=schemas.OrderDetailResponse)
def update_order_status(order_id: str, status_update: schemas.StatusUpdate, db: Session = Depends(get_db)):
    """Update order status"""
    order = db.query(models.RestaurantOrder).filter(models.RestaurantOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    valid_statuses = ["received", "in_progress", "ready", "delivered", "cancelled"]
    if status_update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    order.status = status_update.status
    order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(order)
    
    return order

@router.get("/orders", response_model=List[schemas.OrderDetailResponse])
def list_orders(
    guest_id: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """List orders with optional filtering"""
    query = db.query(models.RestaurantOrder)
    
    if guest_id:
        query = query.filter(models.RestaurantOrder.guest_id == guest_id)
    
    if status:
        query = query.filter(models.RestaurantOrder.status == status)
    
    return query.order_by(models.RestaurantOrder.created_at.desc()).all()

# Table Reservation Endpoints
@router.post("/table-reservations", response_model=schemas.TableReservationResponse)
def create_table_reservation(reservation: schemas.TableReservationCreate, db: Session = Depends(get_db)):
    """Create table reservation"""
    # Simple table assignment logic (in real app, check availability)
    table_number = (hash(f"{reservation.reservation_date}{reservation.reservation_time}") % 10) + 1
    
    db_reservation = models.TableReservation(
        **reservation.dict(),
        table_number=table_number
    )
    
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    
    return {
        "reservation_id": db_reservation.id,
        "table_number": table_number,
        "status": db_reservation.status,
        "message": "Table reserved successfully"
    }

@router.get("/table-reservations/{reservation_id}", response_model=schemas.TableReservationDetail)
def get_reservation(reservation_id: str, db: Session = Depends(get_db)):
    """Get reservation details"""
    reservation = db.query(models.TableReservation).filter(models.TableReservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.get("/table-reservations", response_model=List[schemas.TableReservationDetail])
def list_reservations(guest_id: str = None, db: Session = Depends(get_db)):
    """List table reservations"""
    query = db.query(models.TableReservation)
    
    if guest_id:
        query = query.filter(models.TableReservation.guest_id == guest_id)
    
    return query.order_by(models.TableReservation.reservation_date, models.TableReservation.reservation_time).all()