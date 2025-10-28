from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


# Customer Table

class Customer(Base):
    __tablename__ = "customers"  # Table name in the database

    # Columns (Fields)
    id = Column(Integer, primary_key=True, index=True)  # Unique customer ID (Primary Key)
    name = Column(String, nullable=False)  # Customer name
    email = Column(String, unique=True, nullable=False)  # Customer email (must be unique)

    # Relationship: One Customer → Many Orders
    orders = relationship(
        "Order",
        back_populates="customer",
        cascade="all, delete"  # Delete all related orders if customer is deleted
    )



# Order Table

class Order(Base):
    __tablename__ = "orders"  # Table name in the database

    # Columns (Fields)
    id = Column(Integer, primary_key=True, index=True)  # Unique order ID (Primary Key)
    customer_id = Column(Integer, ForeignKey("customers.id"))  # Foreign Key → customers.id
    date = Column(DateTime, default=datetime.utcnow)  # Order date (default = current time)
    status = Column(String, default="Draft")  # Order status (Draft / Confirmed / Shipped)

    # Relationship: Many Orders → One Customer
    customer = relationship("Customer", back_populates="orders")

    # Relationship: One Order → Many OrderItems
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete"  # Delete all related items if order is deleted
    )



# OrderItem Table

class OrderItem(Base):
    __tablename__ = "order_items"  # Table name in the database

    # Columns (Fields)
    id = Column(Integer, primary_key=True, index=True)  # Unique item ID (Primary Key)
    order_id = Column(Integer, ForeignKey("orders.id"))  # Foreign Key → orders.id
    product_name = Column(String, nullable=False)  # Product name
    quantity = Column(Integer, nullable=False)  # Quantity of the product
    price = Column(Float, nullable=False)  # Price per unit of product

    # Relationship: Many OrderItems → One Order
    order = relationship("Order", back_populates="items")
