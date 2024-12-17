# Hello World Endpoint Task

Implement a GET endpoint at `/hello` that returns a JSON response with a "Hello, World!" message.

## Requirements
- Endpoint: GET `/hello`
- Response: JSON object with key "message" and value "Hello, World!"
- Status code: 200 OK

## Example Request/Response
```
GET /hello

Response:
{
    "message": "Hello, World!"
}
```

## Implementation Steps

1. **Create the Endpoint:**
   - Open the file where your API endpoints are defined, typically in `app/api/endpoints/`.
   - Define a new function for the `/hello` endpoint.

2. **Define the Route:**
   - Use the FastAPI `@app.get("/hello")` decorator to define the route.

3. **Return the Response:**
   - Inside the function, return a JSON response with the message "Hello, World!" using FastAPI's `JSONResponse`.

4. **Test the Endpoint:**
   - Write a test case to ensure the `/hello` endpoint returns the expected JSON response and status code.

### Example Code

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/hello")
async def read_hello():
    return JSONResponse(content={"message": "Hello, World!"})
```

### Example Test

```python
from fastapi.testclient import TestClient
from app.main import app  # Adjust the import based on your project structure

client = TestClient(app)

def test_read_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}
```

By following these steps, you will have implemented a simple `/hello` endpoint that returns a "Hello, World!" message in JSON format.
