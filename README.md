# FastAPI-CRUD-Application-for-Customer-Order-Order-Item-Management-with-Nested-Order-Creation-


🏗️ Project Structure
📁 fastapi_orders_app
│
├── app.py                # Main FastAPI application
├── models.py             # SQLAlchemy ORM models
├── schemas.py            # Pydantic schemas (validation & serialization)
├── database.py           # Database connection setup
└── orders.db   



⚙️ Tech Stack

FastAPI — Web framework for building APIs

SQLAlchemy ORM — Database ORM for Python

Pydantic — Data validation and serialization

SQLite — Lightweight database for simplicity

Uvicorn — ASGI server to run FastAPI apps



🚀 Features

✅ Create, Read, Update, and Delete (CRUD) for:

Customers

Orders

Order Items

✅ Business logic implemented:

Create order with multiple items in one request

Get total customer spending

Update order status (Draft → Confirmed → Shipped)

Prevent deletion of shipped orders

✅ Follows RESTful design principles
✅ Built using clean and modular code structure











🧩 Database Design

Relationships:

Customer → Order → OrderItem

One customer can have multiple orders

One order can contain multiple items

Table	Description
customers	Stores customer details (id, name, email)
orders	Stores order info (id, customer_id, date, status)
order_items	Stores product details for each order (product_name, quantity, price)









📦 Installation Guide
1️⃣ Clone the Repository
git clone https://github.com/yourusername/fastapi-orders-api.git
cd fastapi-orders-api

2️⃣ Create a Virtual Environment
python -m venv venv

3️⃣ Activate the Virtual Environment

Windows

venv\Scripts\activate


Mac/Linux

source venv/bin/activate

4️⃣ Install Dependencies
pip install fastapi sqlalchemy uvicorn pydantic

5️⃣ Run the Application
uvicorn app:app --reload

🌐 API Endpoints Documentation
🏠 Root Route

GET /

{
  "message": "Welcome to the Orders API 🚀",
  "available_routes": {
    "POST /customers": "Create a new customer",
    "POST /orders": "Create a new order with items",
    "GET /customers/{id}/total-spend": "Get total spending of a customer",
    "PUT /orders/{id}/status": "Update order status",
    "DELETE /orders/{id}": "Delete order (blocked if shipped)"
  }
}

👤 Create Customer

POST /customers

{
  "name": "Rudradeb Das",
  "email": "rudra@example.com"
}


Response

{
  "id": 1,
  "name": "Rudradeb Das",
  "email": "rudra@example.com"
}

📦 Create Order with Items

POST /orders

{
  "customer_id": 1,
  "status": "Draft",
  "items": [
    { "product_name": "Laptop", "quantity": 1, "price": 75000 },
    { "product_name": "Mouse", "quantity": 2, "price": 1000 }
  ]
}


Response

{
  "id": 1,
  "customer_id": 1,
  "date": "2025-10-28T18:00:00",
  "status": "Draft",
  "items": [
    { "id": 1, "product_name": "Laptop", "quantity": 1, "price": 75000 },
    { "id": 2, "product_name": "Mouse", "quantity": 2, "price": 1000 }
  ]
}

💰 Get Customer Total Spend

GET /customers/{customer_id}/total-spend

{
  "customer_id": 1,
  "total_spend": 77000
}

🔁 Update Order Status

PUT /orders/{order_id}/status

{
  "status": "Confirmed"
}


Response

{
  "order_id": 1,
  "new_status": "Confirmed"
}

❌ Delete Order

DELETE /orders/{order_id}

{
  "message": "Order deleted successfully"
}


⚠️ Cannot delete an order with status “Shipped”.
