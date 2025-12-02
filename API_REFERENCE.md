# API Reference

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.bugghost.ai` (example)

## Authentication

Currently no authentication required (MVP). Future versions will support:
- API key authentication
- OAuth2 / JWT tokens

---

## Endpoints

### Health & Info

#### GET `/`
Get API information.

**Response:**
```json
{
  "name": "Bug Ghost AI",
  "version": "0.1.0",
  "status": "running"
}
```

#### GET `/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Debug Sessions

#### POST `/api/debug-sessions`
Create a new debug session and generate reproduction.

**Request Body:**
```json
{
  "language": "javascript",
  "runtime_info": "Node 18.x",
  "error_text": "TypeError: Cannot read property 'x' of undefined\n  at main.js:5:12",
  "code_snippet": "const obj = {};\nconsole.log(obj.x.y);",
  "context_description": "This happens when I click the submit button on the login form"
}
```

**Parameters:**
- `language` (string, required): Programming language (e.g., "javascript", "python", "java")
- `runtime_info` (string, optional): Runtime version (e.g., "Node 18", "Python 3.11")
- `error_text` (string, required): Error message or stack trace
- `code_snippet` (string, optional): Relevant code where error occurs
- `context_description` (string, optional): Additional context about when error happens

**Response (201 Created):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-12-01T10:30:00Z",
  "updated_at": "2024-12-01T10:30:15Z",
  "language": "javascript",
  "runtime_info": "Node 18.x",
  "error_text": "TypeError: Cannot read property 'x' of undefined...",
  "code_snippet": "const obj = {};\nconsole.log(obj.x.y);",
  "context_description": "This happens when I click the submit button...",
  "status": "completed",
  "repro_code": "// Minimal reproduction\nconst obj = {};\ntry {\n  console.log(obj.x.y);\n} catch (e) {\n  console.error(e);\n}",
  "test_code": "// Jest test\ntest('should throw TypeError when accessing nested property of undefined', () => {\n  const obj = {};\n  expect(() => obj.x.y).toThrow(TypeError);\n});",
  "explanation": "The error occurs because you're trying to access property 'y' on 'obj.x', but 'obj.x' is undefined. In JavaScript, you cannot read properties of undefined values.",
  "fix_suggestion": "Use optional chaining (?.) to safely access nested properties:\n\nconst value = obj?.x?.y;\n\nOr check if the property exists:\n\nif (obj.x && obj.x.y) {\n  console.log(obj.x.y);\n}",
  "llm_model": "gpt-4-turbo-preview",
  "error_message": null
}
```

**Error Responses:**

*422 Validation Error:*
```json
{
  "detail": [
    {
      "loc": ["body", "language"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

*500 Internal Server Error:*
```json
{
  "detail": "Failed to generate reproduction: API key invalid"
}
```

---

#### GET `/api/debug-sessions/{session_id}`
Get a specific debug session by ID.

**Path Parameters:**
- `session_id` (UUID, required): The session ID

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-12-01T10:30:00Z",
  "updated_at": "2024-12-01T10:30:15Z",
  "language": "python",
  "runtime_info": "Python 3.11",
  "error_text": "NameError: name 'x' is not defined",
  "code_snippet": "print(x)",
  "context_description": null,
  "status": "completed",
  "repro_code": "# This will raise NameError\nprint(x)",
  "test_code": "# pytest test\nimport pytest\n\ndef test_undefined_variable():\n    with pytest.raises(NameError):\n        print(x)",
  "explanation": "The variable 'x' is used before being defined...",
  "fix_suggestion": "Define the variable before using it:\n\nx = 'some value'\nprint(x)",
  "llm_model": "gpt-4-turbo-preview",
  "error_message": null
}
```

**Error Responses:**

*404 Not Found:*
```json
{
  "detail": "Session not found"
}
```

---

#### GET `/api/debug-sessions`
List all debug sessions with pagination.

**Query Parameters:**
- `skip` (integer, optional, default=0): Number of records to skip
- `limit` (integer, optional, default=20): Maximum number of records to return

**Example:**
```
GET /api/debug-sessions?skip=0&limit=10
```

**Response (200 OK):**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2024-12-01T10:30:00Z",
    "language": "javascript",
    "error_snippet": "TypeError: Cannot read property 'x' of undefined",
    "status": "completed"
  },
  {
    "id": "660e9511-f30c-52e5-b827-557766551111",
    "created_at": "2024-12-01T09:15:00Z",
    "language": "python",
    "error_snippet": "NameError: name 'x' is not defined",
    "status": "completed"
  }
]
```

---

## Data Models

### DebugSessionCreate

Request body for creating a session.

```typescript
interface DebugSessionCreate {
  language: string;              // Required
  runtime_info?: string;         // Optional
  error_text: string;            // Required
  code_snippet?: string;         // Optional
  context_description?: string;  // Optional
}
```

### DebugSessionResponse

Full session object.

```typescript
interface DebugSessionResponse {
  id: string;                    // UUID
  created_at: string;            // ISO 8601 datetime
  updated_at: string;            // ISO 8601 datetime
  
  // Input
  language: string;
  runtime_info?: string;
  error_text: string;
  code_snippet?: string;
  context_description?: string;
  
  // Status
  status: "processing" | "completed" | "failed";
  
  // Output
  repro_code?: string;
  test_code?: string;
  explanation?: string;
  fix_suggestion?: string;
  
  // Metadata
  llm_model?: string;
  error_message?: string;        // Only if status is "failed"
}
```

### DebugSessionListItem

Simplified session object for list views.

```typescript
interface DebugSessionListItem {
  id: string;                    // UUID
  created_at: string;            // ISO 8601 datetime
  language: string;
  error_snippet: string;         // First 100 chars of error
  status: "processing" | "completed" | "failed";
}
```

---

## Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request
- **404 Not Found**: Resource not found
- **422 Unprocessable Entity**: Validation error
- **500 Internal Server Error**: Server error

---

## Rate Limiting

Currently no rate limiting in MVP. Future versions will implement:
- 10 requests per minute per IP
- 100 requests per hour per API key

---

## CORS

Allowed origins configured in backend:
- `http://localhost:3000` (development)
- `http://localhost:3001` (development)
- Production domains (configured via environment)

---

## Interactive Documentation

When backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Examples

### cURL

**Create session:**
```bash
curl -X POST "http://localhost:8000/api/debug-sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "javascript",
    "error_text": "TypeError: Cannot read property '\''x'\'' of undefined",
    "code_snippet": "const obj = {};\nconsole.log(obj.x.y);"
  }'
```

**Get session:**
```bash
curl "http://localhost:8000/api/debug-sessions/550e8400-e29b-41d4-a716-446655440000"
```

**List sessions:**
```bash
curl "http://localhost:8000/api/debug-sessions?skip=0&limit=10"
```

### JavaScript (Axios)

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' }
});

// Create session
const response = await api.post('/api/debug-sessions', {
  language: 'python',
  error_text: 'NameError: name "x" is not defined',
  code_snippet: 'print(x)'
});

console.log(response.data);

// Get session
const session = await api.get(`/api/debug-sessions/${response.data.id}`);
console.log(session.data);

// List sessions
const sessions = await api.get('/api/debug-sessions');
console.log(sessions.data);
```

### Python (httpx)

```python
import httpx
import asyncio

async def main():
    async with httpx.AsyncClient() as client:
        # Create session
        response = await client.post(
            "http://localhost:8000/api/debug-sessions",
            json={
                "language": "javascript",
                "error_text": "TypeError: Cannot read property 'x' of undefined",
                "code_snippet": "const obj = {};\nconsole.log(obj.x.y);"
            }
        )
        session = response.json()
        print(session)
        
        # Get session
        response = await client.get(
            f"http://localhost:8000/api/debug-sessions/{session['id']}"
        )
        print(response.json())

asyncio.run(main())
```

---

## Changelog

### v0.1.0 (Current)
- Initial release
- Basic CRUD for debug sessions
- LLM-powered reproduction generation
- Multi-language support

### Future
- Authentication
- Rate limiting
- Webhooks
- Batch operations
