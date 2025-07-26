# Frontend API Integration Guide

## User Management

### 1. Create User (Google OAuth)
**Endpoint:** `POST /api/users`

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "John Doe"  // optional
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00"
}
```

### 2. Google OAuth Login
**Endpoint:** `POST /api/auth/google`

**Request Body:**
```json
{
  "token": "google_id_token_here"
}
```

**Response:**
```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

## Chat API

### 3. Authenticated Chat
**Endpoint:** `POST /chat`

**Headers:**
```
Authorization: Bearer your_jwt_token
Content-Type: application/json
```

**Request Body:**
```json
{
  "message": "I have cramps and feel tired"
}
```

**Response:**
```json
{
  "response": "AI response here..."
}
```

### 4. Demo Chat (No Auth Required)
**Endpoint:** `POST /demo/chat`

**Request Body:**
```json
{
  "message": "I have cramps and feel tired"
}
```

**Response:**
```json
{
  "response": "AI response here..."
}
```

## Cycle Tracking

### 5. Log Cycle
**Endpoint:** `POST /api/cycles`

**Headers:**
```
Authorization: Bearer your_jwt_token
Content-Type: application/json
```

**Request Body:**
```json
{
  "start_date": "2024-01-01T00:00:00",
  "symptoms": "cramps, fatigue",
  "moods": "irritable, tired"
}
```

### 6. Get Cycles
**Endpoint:** `GET /api/cycles`

**Headers:**
```
Authorization: Bearer your_jwt_token
```

## Reminders

### 7. Create Reminder
**Endpoint:** `POST /api/reminders`

**Request Body:**
```json
{
  "type": "medication",
  "time": "09:00",
  "method": "notification"
}
```

### 8. Get Reminders
**Endpoint:** `GET /api/reminders`

## Partner Features

### 9. Invite Partner
**Endpoint:** `POST /api/invite-partner`

**Request Body:**
```json
{
  "partner_email": "partner@example.com",
  "consent_type": "cycle"
}
```

### 10. Get Shared Info
**Endpoint:** `GET /api/shared-info`

## Usage Examples

### Frontend Flow:
1. User clicks "Login with Google"
2. Frontend gets Google ID token
3. Frontend calls `/api/auth/google` with the token
4. Backend returns JWT token
5. Frontend stores JWT and uses it for all future requests

### Creating a New User:
```javascript
// After Google OAuth, if user doesn't exist
fetch('/api/users', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    email: 'user@example.com',
    name: 'User Name'
  })
})
```

### Chat Example:
```javascript
fetch('/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + jwt_token
  },
  body: JSON.stringify({
    message: 'I have cramps today'
  })
})
.then(response => response.json())
.then(data => console.log(data.response));
```

## Base URL
- **Development:** `http://localhost:8000`
- **Production:** Your deployed backend URL

## Error Handling
All endpoints return standard HTTP status codes:
- `200`: Success
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (invalid/missing token)
- `404`: Not Found
- `500`: Server Error 