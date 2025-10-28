from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models, schemas

# Initialize FastAPI app
app = FastAPI(title="Orders REST API ")


# Database setup


# Create all tables defined in models.py
Base.metadata.create_all(bind=engine)

# Dependency for getting a database session
def get_db():
    db = SessionLocal()
    try:
        yield db  # Provide the DB session for request
    finally:
        db.close()  # Close session after request ends

# Root Route (Welcome Message)
@app.get("/")
def root():
    return {
        "message": "Welcome to the Orders API",
        "available_routes": {
            "POST /customers": "Create a new customer",
            "POST /orders": "Create a new order with items",
            "GET /customers/{id}/total-spend": "Get total spending of a customer",
            "PUT /orders/{id}/status": "Update order status",
            "DELETE /orders/{id}": "Delete order (blocked if shipped)"
        }
    }



# Create a Customer
@app.post("/customers", response_model=schemas.CustomerResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    # Create a new customer record
    db_customer = models.Customer(name=customer.name, email=customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)  # Refresh to get auto-generated ID
    return db_customer



# Create Order with Multiple Items
@app.post("/orders", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Check if customer exists
    db_customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Create new order
    db_order = models.Order(customer_id=order.customer_id, status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # Add multiple order items
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_name=item.product_name,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
    db.commit()
    db.refresh(db_order)
    return db_order



# Get Total Spending of a Customer
@app.get("/customers/{customer_id}/total-spend")
def get_total_spend(customer_id: int, db: Session = Depends(get_db)):
    # Check if customer exists
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Get all orders of the customer
    orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).all()

    # Calculate total spend = sum of price * quantity for all order items
    total_spend = sum(item.price * item.quantity for order in orders for item in order.items)
    return {"customer_id": customer_id, "total_spend": total_spend}



# Update Order Status (Draft → Confirmed → Shipped)
@app.put("/orders/{order_id}/status")
def update_order_status(order_id: int, new_status: dict, db: Session = Depends(get_db)):
    # Fetch order by ID
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Validate new status
    valid_status = ["Draft", "Confirmed", "Shipped"]
    if new_status["status"] not in valid_status:
        raise HTTPException(status_code=400, detail="Invalid status value")

    # Update order status
    order.status = new_status["status"]
    db.commit()
    db.refresh(order)
    return {"order_id": order.id, "new_status": order.status}



# Delete Order (Blocked if Shipped)
@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    # Fetch order by ID
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Prevent deletion if order is already shipped
    if order.status == "Shipped":
        raise HTTPException(status_code=400, detail="Cannot delete shipped order")

    # Delete the order
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
