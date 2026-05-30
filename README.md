Restaurant Management System

A server-side web application built with Flask and MySQL for managing restaurant operations including menu items, orders, and billing.
Features

Add, view, update and delete menu items
Manage customer orders and billing
Full CRUD operations with validation and error handling
Structured relational database with optimized SQL queries
Responsive HTML interface with inline styling

Technologies Used

Python 3.x
Flask
MySQL
HTML, CSS

Project Structure
RESTAURANT_APP/
├── app.py          # Main Flask application
├── schema.sql      # Database schema
├── templates/      # HTML templates
└── README.md
How to Run

Clone the repo
Install dependencies: pip install flask mysql-connector-python
Setup MySQL and run schema.sql to create tables
Update DB credentials in app.py
Run: python app.py
Open http://localhost:5000

Database

Designed with proper relational schema
Optimized SQL queries for data retrieval
Supports transaction handling for order and billing management
