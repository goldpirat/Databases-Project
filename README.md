# **BOOKed - Library Management System**

A comprehensive and modern **Library Management System** built with Flask, utilizing a MySQL database to manage books, users, and library activities like borrowing, reviewing, and administrative management. This project provides features for both regular users and librarians, with access control and efficient data management.

## **Table of Contents**

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Installation & Setup](#installation-setup)
5. [Usage](#usage)
6. [Database Schema](#database-schema)
7. [Contributing](#contributing)
8. [License](#license)

---

## **Project Overview**

**BOOKed** is a web-based library management system designed to streamline the management of books, user data, and library operations. Built using Flask as the backend framework and MySQL for data storage, it enables **librarians** to manage users, books, and system logs while providing **regular users** a seamless experience for browsing, borrowing, and reviewing books.

This application features robust authentication, efficient search functionality, and an intuitive admin interface to manage all aspects of the library system.

---

## **Features**

- **User Authentication & Role-Based Access**:
  - Login and registration system with roles for **Regular Users** and **Librarians**.
  - Librarians have additional privileges to manage users, books, and view logs.

- **Book Management**:
  - Regular users can browse books by title, genre, and author.
  - Librarians can add, update, or delete books from the system, including managing available copies.

- **Book Borrowing & Returning**:
  - Users can borrow and return books.
  - System tracks borrowing history and updates book availability in real-time.

- **Book Reviews & Ratings**:
  - Users can submit reviews and rate books they have borrowed, enhancing the user experience.

- **Log Management**:
  - Access and error logs are collected from Apache logs, visualized for easy monitoring and analysis.
  - Provides detailed IP statistics and browser usage reports for administrators.

- **Geolocation of Users**:
  - Geolocation feature for IPs in the access logs using external APIs (e.g., `ipinfo.io`) to map user locations.

---

## **Tech Stack**

- **Backend**: Flask (Python Web Framework)
- **Database**: MySQL (for persistent data storage)
- **Frontend**: HTML, CSS (Bootstrap for responsive design)
- **APIs**: ipinfo.io (for geolocation)
- **Authentication**: Flask-Login
- **Version Control**: Git (with GitHub for repository hosting)
- **Deployment**: Apache with WSGI (for hosting the Flask application)

---

## **Installation & Setup**

### **Prerequisites**

1. **Python 3.x** installed on your local machine.
2. **MySQL** (or another compatible database) setup on your system.
3. **Git** for version control.
4. **Virtual Environment** (recommended for Python projects).

### **Steps to Install**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/goldpirat/Databases-Project.git
   cd Databases-Project
## **Usage**

Once the application is up and running:

### **For Regular Users**:
- You can **register**, **login**, and then **browse books** by title or genre.
- **Borrow** and **return** books, and **leave reviews** on books you’ve read.

### **For Librarians**:
- After logging in, you can manage the library by **adding, updating, or deleting books**.
- **View logs**, including user access and error logs.
- **Manage users** (add, update, delete users).

---

## **Database Schema**

The database includes the following tables:

1. **User**: Manages user information (username, email, password, role).
2. **Book**: Stores book details (title, author, genre, ISBN, available copies).
3. **Borrowing**: Tracks borrowed books (user ID, book ID, borrow date, return date).
4. **Review**: Stores book reviews (user ID, book ID, review text, rating).
5. **Reservation**: Tracks active reservations (user ID, book ID, reservation date).
6. **Logs**: Captures user and error logs (IP addresses, timestamps, error messages).

---

## **Contributing**

We welcome contributions to the project! If you'd like to contribute, follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
Make your changes and commit them:
  git commit -am 'Add new feature'
Push to the branch:
  git push origin feature-branch


Enjoy!
