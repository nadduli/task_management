# Task Management API

This is a **Task Management API** built with **FastAPI** and **SQLModel**. It provides endpoints for managing tasks and users, supporting features like task creation, updating, authentication, and more. The API can be integrated with a frontend for a full-featured task management system.

## Features

- User Authentication with JWT access tokens
- CRUD operations for tasks and users
- Support for task priorities, due dates, tags, and assignment to users
- Efficient database handling with SQLModel and PostgreSQL
- Automatic schema migrations using Alembic
- Custom middleware and exception handling for token validation and error responses

## Requirements

- **Python 3.9+**
- **PostgreSQL**
- **Docker** (optional, for containerization)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/nadduli/task_management.git
```

cd task_management

### 2. Set Up Virtual Environment
python3 -m venv env
source env/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Configure Environment Variables
Create a .env file in the project root:

* DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/task_db
* SECRET_KEY=your_secret_key
* ALGORITHM=HS256
* ACCESS_TOKEN_EXPIRE_MINUTES=30

### 5. Run Database Migrations
alembic upgrade head

### 6. Start the Application
fastapi dev api/

### The API will be available at http://localhost:8000.

## API Endpoints
### Authentication
* POST /auth/signup - Register a new user
* POST /auth/login - Login and receive an access token

### Users
* GET /users/{user_id} - Get user details by ID
* PUT /users/{user_id} - Update user details
* DELETE /users/{user_id} - Delete a user

### Tasks
* POST /tasks - Create a new task
* GET /tasks - Retrieve all tasks
* GET /tasks/{task_id} - Get task details by ID
* PUT /tasks/{task_id} - Update a task
* DELETE /tasks/{task_id} - Delete a task

### Models
* Task: Fields include title, description, due date, status, priority, assigned user, and tags.
* User: Fields include username, email, hashed password, and verification status.

### Authentication
After logging in, users receive an access token which should be included in the Authorization header for protected routes:

Authorization: Bearer your_jwt_token

### Seeding Data
* python3 seeds/seed_tasks.py
* python3 seeds/seed_users.py

### Testing
Run tests with pytest:

pytest

### Future Enhancements
Future goals include:

* Implementing refresh tokens
* Adding task comments and attachments
* Integrating notifications and reminders
* Creating a frontend interface

### Author
Nadduli Daniel <naddulidaniel94@gmail.com>

### License
This project is licensed under the MIT License