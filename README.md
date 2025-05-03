# Quillist API - Book Review API

Quillist API is a RESTful API built with FastAPI for managing book reviews. It provides endpoints for user authentication, book management, and review submission. The API is designed to be efficient, scalable, and easy to use. It leverages modern Python features and libraries to provide a robust backend solution for book review applications.

- Quillist API is live at [https://quillist-api.onrender.com/auth/v1](https://quillist-api.onrender.com/auth/v1)
- Quillist API Swagger UI documentation is live at [https://quillist-api.onrender.com/auth/v1/docs](https://quillist-api.onrender.com/auth/v1/docs)
- Quillist API ReDoc documentation is live at [https://quillist-api.onrender.com/auth/v1/redoc](https://quillist-api.onrender.com/auth/v1/redoc)
- Quillist API OpenAPI specification is live at [https://quillist-api.onrender.com/auth/v1/openapi.json](https://quillist-api.onrender.com/auth/v1/openapi.json)

**NOTE:** User Signup, password reset, email verification and other email related features are not available in the live version of the API as it requires **paid background worker service hosting**. You can test these features locally by running the API on your machine.

For testing purposes, you can use the following credentials:

```
"user": {
        "uid": "4e66ac0d-0e61-408d-974d-9e8d6a5b6ba6",
        "username": "quillist",
        "email": "testuser@quillist.com",
        "first_name": "Quillist",
        "last_name": "Ray",
        "is_verified": true,
        "created_at": "2025-05-04T03:21:40.610001",
        "updated_at": "2025-05-04T03:21:40.610011"
    }
```

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
- [x] Celery integration with Redis
- [x] Celery worker setup
- [x] Flower monitoring for Celery

### Testing & Documentation

- [x] API documentation with SwaggerUI and ReDoc
- [x] Unit testing with Unittest Mock and Pytest
- [x] Document-driven testing with Schemathesis

### Deployment

- [x] Deployment on Render.com

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
API_URL=

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

- You can access the API at `http://localhost:8000`.
- You can access the API documentation in **Swagger UI** at `http://localhost:8000/docs`.
- You can access the API documentation in **ReDoc** at `http://localhost:8000/redoc`.
- You can access the API documentation in **OpenAPI specification** at `http://localhost:8000/openapi.json`.

8. **Run Celery worker for background tasks:**
   Open a new terminal window, activate the virtual environment, and run the following command to start the Celery worker:

   ```bash
   celery  -A src.celery_tasks.celery_app worker
   ```

9. **Run Flower for monitoring Celery tasks (Optional):**
   Open another terminal window, activate the virtual environment, and run the following command to start Flower:

   ```bash
   celery -A src.celery_tasks.celery_app flower
   ```

   Flower will be accessible at `http://localhost:5555`.

10. **Run Alembic migrations:**
    To apply database migrations, run the following command:

    ```bash
    alembic upgrade head
    ```

    This will apply all pending migrations to the database.

11. **Run tests:**
    To run the tests, use the following command:

    ```bash
    pytest
    ```

    This will execute all the tests in the `tests` directory.
    You can also run a specific test file or test case by specifying the path:

    ```bash
      pytest tests/test_file.py
    ```

    or

    ```bash
       pytest tests/test_file.py::test_case_name
    ```

    This will run only the specified test case.

12. **Generate and run tests with Schemathesis (Document Driven Testing):**

    - To generate tests using Schemathesis, use the following command:

    ```bash
    st run http://127.0.0.1:8000/api/v1/openapi.json --experimental=openapi-3.1
    ```

    This will generate and run tests based on the OpenAPI specification.

    - You can also specify a specific endpoint to test:

    ```bash
    st run http://127.0.0.1:8000/api/v1/openapi.json --experimental=openapi-3.1 --endpoint /api/v1/books
    ```

    This will generate and run tests only for the specified endpoint.

## Technologies Used

- **FastAPI** for building the API.
- **PostgreSQL** (NeonDB) for database.
- **SQLAlchemy** and **SQLModel** for database ORM.
- **Alembic** for database migrations.
- **Pydantic** for data validation.
- **UUID** for generating unique identifiers.
- **JWT** for authentication.
- **Passlib** for password hashing.
- **itsdangerous** for generating and verifying tokens.
- **FastAPI-Mail** for sending emails.
- **Logging** for logging.
- **Redis** for Token blacklisting, and Background Task queue (ex: sending emails).
- **Celery** for background tasks (ex: sending emails).
- **Flower** for background task monitoring.
- **Asgiref** for async function to sync function conversion.
- **Pytest** for testing.
- **Schemathesis** for document driven testing.
- **OpenAPI Specification**, **Swagger UI** and **Redoc** for API documentation.
- **Python-dotenv** for environment variable management.
- **Render** for deploying the API.
