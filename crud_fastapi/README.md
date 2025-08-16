Below is a `README.md` file tailored to your FastAPI CRUD application (`crud_fastapi`) project, providing instructions on how to run the application, run all tests, and run individual test cases. This is based on your project structure and the updates made to `main.py` and `test_main.py`.

```markdown
# FastAPI CRUD Practice Test

This is a FastAPI application implementing CRUD (Create, Read, Update, Delete) operations on an SQLite database, along with Pytest tests. The project uses a virtual environment (`.venv`) for dependency management.

## Prerequisites
- Python 3.7+ (Python 3.13.5 recommended)
- pip (Python package manager)

## Setup

### 1. Create and Activate Virtual Environment
- Create a virtual environment:
  ```bash
  python -m venv .venv
  ```
- Activate it:
  - **Windows**: `.venv\Scripts\activate`
  - **macOS/Linux**: `source .venv/bin/activate`
- Verify activation by checking the prompt (e.g., `(.venv)`).

### 2. Install Dependencies
Install the required packages:
```bash
pip install -r requirements.txt
```
If `requirements.txt` is missing, install manually:
```bash
pip install fastapi sqlalchemy pytest httpx uvicorn pytest-asyncio pytest-cov python-dotenv
```

## Running the Application
Start the FastAPI application with Uvicorn:
```bash
uvicorn main:app --reload
```
- Access the app at `http://127.0.0.1:8000`.
- **API Endpoints**:
  - `GET /items`: List all items.
  - `GET /items/{item_id}`: Get a specific item.
  - `POST /items`: Create a new item (e.g., `{"name": "Test", "description": "Test item"}` or `{"id": 1, "name": "Test", "description": "Test item"}` to specify id).
  - `PUT /items/{item_id}`: Update an item.
  - `DELETE /items/{item_id}`: Delete an item.
- Stop the server with `Ctrl+C`.


## Running Tests
Run all tests with Pytest:
```bash
pytest test_main.py
```
- This executes all test cases in `test_main.py`.

## Running Individual Test Cases
To run a specific test case one by one (useful for debugging), use the following commands:
- **Run `test_create_item` only**:
  ```bash
  pytest test_main.py::test_create_item
  ```
- **Run `test_get_items` only**:
  ```bash
  pytest test_main.py::test_get_items
  ```
- **Run `test_get_item` only**:
  ```bash
  pytest test_main.py::test_get_item
  ```
- **Run `test_update_item` only**:
  ```bash
  pytest test_main.py::test_update_item
  ```
- **Run `test_delete_item` only**:
  ```bash
  pytest test_main.py::test_delete_item
  ```

## Notes
- The real database is `real.db`, and the test database is `test.db`, created automatically.
- The application supports specifying `id` when creating items via `POST /items`, with uniqueness validation.
- Each test case is isolated using a `reset_db` fixture to ensure a clean database state.
- Use `Ctrl+C` to stop the Uvicorn server or Pytest process.

## Troubleshooting
- **Activation Issues**: Ensure `.venv` exists and use the correct activation command.
- **Missing Dependencies**: Run `pip install -r requirements.txt` again.
- **Port Conflict**: Change the port with `uvicorn main:app --port 8001 --reload`.
- **Test Failures**: Check the test output for specific errors (e.g., 422 status) and adjust input data or endpoint logic accordingly.

