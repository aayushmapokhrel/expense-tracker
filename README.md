# 💸 Django Expense Tracker API

Welcome to the **Expense Tracker API** — a Django-powered RESTful API designed to help users manage income and expenses efficiently. Whether you're building a personal finance tool or exploring Django REST Framework, this project is a great starting point.

---

## 🚀 Project Overview

**Goal:** Build a secure REST API for tracking personal and business income/expenses with full CRUD support and JWT authentication.

### 🔐 User Access Control

- **Regular Users**: Can only manage their own records
- **Superusers**: Have access to all users' records
- **Authentication**: All endpoints require JWT tokens

---

## 🔑 Key Features

- ✅ User registration & login with JWT authentication
- ✅ Personal income/expense tracking
- ✅ Automatic tax calculation (flat or percentage)
- ✅ Paginated API responses
- ✅ Full CRUD (Create, Read, Update, Delete)
- ✅ Permissions based on user type

---

## 🧩 Database Models

### 👤 User

- Uses Django’s built-in `User` model

### 💰 ExpenseIncome

| Field           | Type         | Notes                                           |
|----------------|--------------|-------------------------------------------------|
| `user`         | ForeignKey   | Links to Django `User`                         |
| `title`        | CharField    | Max 200 characters                             |
| `description`  | TextField    | Optional                                       |
| `amount`       | DecimalField | Max digits=10, decimal_places=2                |
| `transaction_type` | CharField | Choices: `credit`, `debit`                    |
| `tax`          | DecimalField | Default = 0                                    |
| `tax_type`     | CharField    | Choices: `flat`, `percentage`; default = `flat`|
| `created_at`   | DateTimeField| Auto-generated                                 |
| `updated_at`   | DateTimeField| Auto-generated                                 |

### 💡 Business Logic

- **Flat Tax**: `total = amount + tax`
- **Percentage Tax**: `total = amount + (amount * tax / 100)`

---

## 🔗 API Endpoints

### 🔒 Authentication

| Method | Endpoint              | Description           |
|--------|-----------------------|-----------------------|
| POST   | `/api/auth/register/` | Register a new user   |
| POST   | `/api/auth/login/`    | Log in, get JWT tokens|
| POST   | `/api/auth/refresh/`  | Refresh access token  |

### 💼 Expense/Income

| Method | Endpoint               | Description                    |
|--------|------------------------|--------------------------------|
| GET    | `/api/expenses/`       | List all user records (paginated) |
| POST   | `/api/expenses/`       | Create a new record            |
| GET    | `/api/expenses/{id}/`  | Retrieve a specific record     |
| PUT    | `/api/expenses/{id}/`  | Update an existing record      |
| DELETE | `/api/expenses/{id}/`  | Delete a record                |

---

## 📦 Expected API Response Formats

### 🔹 Single Record
```json
{
  "id": 1,
  "title": "shoes shopping",
  "description": "monthly groceries",
  "amount": 2200.00,
  "transaction_type": "debit",
  "tax": 0.00,
  "tax_type": "flat",
  "total": 2200.00,
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}


