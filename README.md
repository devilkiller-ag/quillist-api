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
- [ ] User model creation
- [ ] User registration endpoint
- [ ] Password hashing with Passlib
- [ ] JWT authentication with PyJWT
- [ ] User login endpoint
- [ ] HTTP Bearer authentication
- [ ] Refresh token implementation
- [ ] Token revocation using Redis
- [ ] Role-based access control
- [ ] Current user retrieval endpoint
- [ ] Role checker dependency

### Model & Schema Relationships
- [ ] User-book relationship modeling
- [ ] User-review relationship modeling
- [ ] Nested schema serialization

###  Middleware & Error Handling
- [ ] Custom exception classes
- [ ] Exception handlers registration
- [ ] Custom logging middleware
- [ ] CORS middleware integration
- [ ] Trusted hosts configuration

### Email Support
- [ ] FastAPI-Mail setup
- [ ] Email sending functionality
- [ ] User account verification via email
- [ ] Password reset emails

### Background Tasks
- [ ] FastAPI background tasks
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

6. **Run the application:**
    ```bash
    fastapi dev src/
    ```

The application should now be up and running within the virtual environment.
You can access the API documentation at `http://localhost:8000/docs`.

## Environment Variables
The application uses environment variables for configuration. Create a `.env` file in the root directory and add the following variables:

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost/dbname
```
Replace `username`, `password`, and `dbname` with your PostgreSQL credentials.
