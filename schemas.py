from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Schema for Creating Order Items (Input)
class OrderItemCreate(BaseModel):
    product_name: str  # Name of the product
    quantity: int      # Quantity ordered
    price: float       # Price per unit


# Schema for Creating an Order (Input)
class OrderCreate(BaseModel):
    customer_id: int                 # ID of the customer placing the order
    status: str                      # Initial order status (e.g., Draft, Confirmed)
    items: List[OrderItemCreate]     # List of order items to be included in the order



# Schema for Creating a Customer (Input)
class CustomerCreate(BaseModel):
    name: str   # Customer name
    email: str  # Customer email address


# Schema for Order Item (Response)
class OrderItemResponse(BaseModel):
    id: int             # Item ID
    product_name: str   # Product name
    quantity: int       # Quantity ordered
    price: float        # Price per unit

    # Enables ORM object compatibility (SQLAlchemy → Pydantic)
    class Config:
        orm_mode = True


# Schema for Order (Response)

class OrderResponse(BaseModel):
    id: int                        # Order ID
    customer_id: int               # Associated customer ID
    date: datetime                 # Date and time of order creation
    status: str                    # Current order status
    items: List[OrderItemResponse] # List of related order items

    class Config:
        orm_mode = True


# Schema for Customer (Response)
class CustomerResponse(BaseModel):
    id: int      # Customer ID
    name: str    # Customer name
    email: str   # Customer email

    class Config:
        orm_mode = True
