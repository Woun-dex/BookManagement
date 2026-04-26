# Library Management System

Welcome to the **Library Management System**! This is a modern, full-stack application designed to help librarians manage their book inventory and allow readers to browse, rent, and rate books.

---

## Quick Start

### Backend (FastAPI)
The backend handles the database, authentication, and business logic.

1. **Navigate to the directory:**
   ```bash
   cd BookManagement
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Setup Database:**
   Ensure you have PostgreSQL running and update the `.env` file with your `POSTGRES_URL`.
4. **Seed the Database:**
   If you want to start with a fresh set of 150+ books and users:
   ```bash
   python seed_db.py
   ```
5. **Run the server:**
   ```bash
   fastapi dev main.py
   ```

### Frontend (React + Vite)
The frontend provides a premium user interface built with Material UI.

1. **Navigate to the directory:**
   ```bash
   cd BooksLibrary
   ```
2. **Install dependencies:**
   ```bash
   npm install
   ```
3. **Run the app:**
   ```bash
   npm run dev
   ```

---

## Features

- **Rich Catalog**: Explore over 150 books across categories like Philosophy, Programming, Math, and Novels.
- **User Roles**:
  - **Readers**: Can browse books, request rentals, and leave ratings/reviews.
  - **Librarians**: Manage rental requests and update the book inventory.
  - **Admin**: Full control over users and the library system.
- **Real-time Dashboard**: Track borrowed history and rental states (Pending, Approved, Returned).
- **Interactive Ratings**: Share your thoughts on books with a built-in rating system.

---

## Tech Stack

- **Frontend**: React, Vite, Material UI (MUI), TypeScript.
- **Backend**: FastAPI, SQLAlchemy (ORM), Pydantic.
- **Database**: PostgreSQL.

