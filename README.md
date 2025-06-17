# Book Management Django REST API

## Overview

This is a Django REST API for managing books, users, and reading lists, built with Django REST Framework and JWT authentication. It fulfills all requirements of the assessment, including user management, book management, reading lists, interactions, and error handling. The API follows RESTful principles, implements secure authentication/authorization, and provides robust error handling.

## Setup Instructions

Follow these steps to set up and run the project locally:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/mijwad7/book_manager.git
   cd book_manager
   ```

2. **Create and Activate a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start the Development Server**:

   ```bash
   python manage.py runserver
   ```

   Access the API at `http://127.0.0.1:8000/api/`.

## API Endpoints

All endpoints are prefixed with `/api/`. Authentication uses JWT tokens obtained via `/api/token/`. Include the token in the `Authorization` header as `Bearer <access_token>` for protected endpoints.

### User Management

- **Register User**: `POST /users/`
  - **Description**: Create a new user with a unique username and email.
  - **Permissions**: None (public).
  - **Request Body**:
    ```json
    {
      "username": "testuser",
      "email": "test@example.com",
      "password": "securepass123"
    }
    ```
  - **Example**:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/users/ -d '{"username":"testuser","email":"test@example.com","password":"securepass123"}'
    ```
  - **Response**: `201 Created`
    ```json
    {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com"
    }
    ```
  - **Errors**:
    - `400 Bad Request`: Duplicate username/email or missing fields.
- **Login**: `POST /token/`
  - **Description**: Obtain JWT access and refresh tokens.
  - **Permissions**: None (public).
  - **Request Body**:
    ```json
    {
      "username": "testuser",
      "password": "securepass123"
    }
    ```
  - **Example**:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/token/ -d '{"username":"testuser","password":"securepass123"}'
    ```
  - **Response**: `200 OK`
    ```json
    {
      "refresh": "<refresh_token>",
      "access": "<access_token>"
    }
    ```
  - **Errors**:
    - `401 Unauthorized`: Invalid credentials.
- **Manage Profile**: `GET/PUT/DELETE /users/<id>/`
  - **Description**: Retrieve, update, or delete a user’s profile.
  - **Permissions**: Authenticated user (must be the user themselves).
  - **Example (GET)**:
    ```bash
    curl -X GET http://127.0.0.1:8000/api/users/1/ -H "Authorization: Bearer <access_token>"
    ```
  - **Response**: `200 OK`
    ```json
    {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com"
    }
    ```
  - **Errors**:
    - `401 Unauthorized`: Missing/invalid token.
    - `403 Forbidden`: Attempt to access another user’s profile.

### Book Management

- **List Books**: `GET /books/`
  - **Description**: Retrieve all books (public access).
  - **Permissions**: None (public).
  - **Example**:
    ```bash
    curl -X GET http://127.0.0.1:8000/api/books/
    ```
  - **Response**: `200 OK`
    ```json
    [
      {
        "id": 1,
        "title": "Sample Book",
        "authors": "John Doe",
        "genre": "Fiction",
        "publication_date": "2023-01-01",
        "description": "A sample book",
        "created_by": 1,
        "created_at": "2025-06-17T18:47:00Z"
      }
    ]
    ```
- **Create Book**: `POST /books/`
  - **Description**: Create a new book.
  - **Permissions**: Authenticated user.
  - **Request Body**:
    ```json
    {
      "title": "Sample Book",
      "authors": "John Doe",
      "genre": "Fiction",
      "publication_date": "2023-01-01",
      "description": "A sample book"
    }
    ```
  - **Example**:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/books/ -d '{"title":"Sample Book","authors":"John Doe","genre":"Fiction","publication_date":"2023-01-01","description":"A sample book"}' -H "Authorization: Bearer <access_token>"
    ```
  - **Response**: `201 Created`
  - **Errors**:
    - `400 Bad Request`: Missing/invalid fields (e.g., invalid `publication_date`).
    - `401 Unauthorized`: Missing/invalid token.
- **Retrieve Book**: `GET /books/<id>/`
  - **Description**: Get details of a specific book.
  - **Permissions**: None (public).
  - **Example**:
    ```bash
    curl -X GET http://127.0.0.1:8000/api/books/1/
    ```
- **Delete Book**: `DELETE /books/<id>/`
  - **Description**: Delete a book (only by the creator).
  - **Permissions**: Authenticated user (creator only).
  - **Example**:
    ```bash
    curl -X DELETE http://127.0.0.1:8000/api/books/1/ -H "Authorization: Bearer <access_token>"
    ```
  - **Response**: `204 No Content`
  - **Errors**:
    - `403 Forbidden`: User is not the book’s creator.
    - `404 Not Found`: Book does not exist.

### Reading Lists

- **Create/List Reading Lists**: `POST/GET /reading-lists/`
  - **Description**: Create or list reading lists for the authenticated testers.
  - **Permissions**: Authenticated user.
  - **Request Body (POST)**:
    ```json
    {
      "name": "My Favorites"
    }
    ```
  - **Example (POST)**:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/reading-lists/ -d '{"name":"My Favorites"}' -H "Authorization: Bearer <access_token>"
    ```
  - **Response**: `201 Created`
    ```json
    {
      "id": 1,
      "name": "My Favorites",
      "user": 1,
      "created_at": "2025-06-17T18:47:00Z"
    }
    ```
  - **Errors**:
    - `400 Bad Request`: Missing `name` field.
- **Manage Reading List**: `GET/PUT/DELETE /reading-lists/<id>/`
  - **Description**: Retrieve, update, or delete a specific reading list.
  - **Permissions**: Authenticated user (owner only).
  - **Example (GET)**:
    ```bash
    curl -X GET http://127.0.0.1:8000/api/reading-lists/1/ -H "Authorization: Bearer <access_token>"
    ```

### Reading List Items

- **Add/Remove Book**: `POST/DELETE /reading-list-items/`
  - **Description**: Add or remove a book from a reading list.
  - **Permissions**: Authenticated user (owner of the reading list).
  - **Request Body (POST)**:
    ```json
    {
      "reading_list": 1,
      "book_id": 1,
      "order": 1
    }
    ```
  - **Example (POST)**:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/reading-list-items/ -d '{"reading_list":1,"book_id":1,"order":1}' -H "Authorization: Bearer <access_token>"
    ```
  - **Response**: `201 Created`
    ```json
    {
      "id": 1,
      "reading_list": 1,
      "book": { ... },
      "book_id": 1,
      "order": 1,
      "added_at": "2025-06-17T18:47:00Z"
    }
    ```
  - **Errors**:
    - `400 Bad Request`: Duplicate book in list or invalid `book_id`/`reading_list`.
    - `403 Forbidden`: Reading list not owned by user.
- **Reorder Book**: `POST /reading-list-items/<id>/reorder/`
  - **Description**: Reorder a book in a reading list.
  - **Permissions**: Authenticated user (owner of the reading list).
  - **Request Body**:
    ```json
    {
      "order": 2
    }
    ```
  - **Example**:
    ```bash
    curl -X POST http://127.0.0.1:8000/api/reading-list-items/1/reorder/ -d '{"order":2}' -H "Authorization: Bearer <access_token>"
    ```
  - **Response**: `200 OK`
    ```json
    {
      "status": "order updated"
    }
    ```
  - **Errors**:
    - `400 Bad Request`: Missing `order` field.
