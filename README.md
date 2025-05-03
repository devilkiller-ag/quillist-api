# Quillist API - Book Review API

Quillist API is a RESTful API built with FastAPI for managing book reviews. It provides endpoints for user authentication, book management, and review submission. The API is designed to be efficient, scalable, and easy to use. It leverages modern Python features and libraries to provide a robust backend solution for book review applications.

**Note:** This project is a work in progress and is not yet fully functional. The goal is to create a comprehensive API that can be used for book review applications.

## Features & Progress

### Core API Functionality

- [x] Project setup with FastAPI CLI
- [x] Basic web server implementation
- [x] API versioning
- [x] API routing with FastAPI routers

### Database Integration

- [x] Database setup with SQLModel and PostgreSQL
- [x] Asynchronous database connections
- [x] Database migrations using Alembic
- [x] Environment configuration with Pydantic settings
- [x] Lifespan events for database connection management

### CRUD Operations for Books

- [x] Book model creation
- [x] CURD operations for books

### Authentication & Authorization

- [x] User model creation
- [x] User registration endpoint
- [x] Password hashing with Passlib
- [x] JWT authentication with PyJWT
- [x] User login endpoint
- [x] HTTP Bearer authentication
- [x] Refresh token implementation
- [x] Token revocation using Redis
- [x] Role-based access control
- [x] Current user retrieval endpoint
- [x] Role checker dependency

### Model & Schema Relationships

- [x] User-book relationship modeling
- [x] User-review relationship modeling
- [x] Nested schema serialization

### Middleware & Error Handling

- [x] Custom exception classes
- [x] Exception handlers registration
- [x] Custom logging middleware
- [x] CORS middleware integration
- [x] Trusted hosts configuration

### Email Support

- [x] FastAPI-Mail setup
- [x] Email sending functionality
- [x] User account verification via email
- [x] Password reset emails

### Background Tasks

- [x] FastAPI background tasks
- [ ] Celery integration with Redis
- [ ] Celery worker setup
- [ ] Flower monitoring for Celery

### Testing & Documentation

- [ ] API documentation with SwaggerUI and ReDoc
- [ ] Unit testing with Unittest Mock and Pytest
- [ ] Document-driven testing with Schemathesis

### Deployment

- [ ] Dockerfile creation
- [ ] Docker Compose setup
- [ ] Deployment on Render.com

## Role Based Access Control

The API supports role-based access control (RBAC) to manage user permissions. The following roles are defined:

- `admin`: Full access to all endpoints.
- `user`: Limited access to user-specific endpoints.

The `admin` role can perform these actions:

- Add users
- Change user roles
- CURD on users
- CURD on books
- CURD on reviews
- Revoking access tokens

The `user` role can perform these actions:

- CURD on their own book submissions
- CURD on their own reviews
- CURD on their own account

## Project Setup

To set up the project, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/devilkiller-ag/quillist-api.git
   ```

2. **Navigate into the project directory:**

   ```bash
   cd quillist-api
   ```

3. **Create a virtual environment:**

   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     ```
   - On Windows:
     ```bash
     python -m venv venv
     ```

4. **Activate the virtual environment:**

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

5. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Define enviornment variables**
   Create a `.env` file in the root folder and define all required enviornment variables.

```
DOMAIN=

DATABASE_URL=
REDIS_URL=

JWT_SECRET=
JWT_ALGORITHM=

MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_SERVER=
MAIL_PORT=
MAIL_FROM=
MAIL_FROM_NAME=
```

7. **Run the application:**
   ```bash
   fastapi dev src/
   ```

The application should now be up and running within the virtual environment.
You can access the API documentation at `http://localhost:8000/docs`.

8. **Run Celery worker for background tasks:**
   Open a new terminal window, activate the virtual environment, and run the following command to start the Celery worker:
   ```bash
   celery  -A src.celery_tasks.celery_app worker
   ```

## Environment Variables

The application uses environment variables for configuration. Create a `.env` file in the root directory and add the following variables:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
```

Replace `username`, `password`, and `dbname` with your PostgreSQL credentials.
