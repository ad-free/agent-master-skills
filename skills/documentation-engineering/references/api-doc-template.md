# API Reference: <Service>

## Base URL
`https://api.example.com/v1`

## Authentication
<Method: Bearer, API Key, etc.>

## Endpoints

### GET /resource
<Description>

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|

**Query Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|

**Response 200:**
```json
{
  "field": "type"
}
```

**Response 4xx/5xx:**
```json
{
  "error": "code",
  "message": "description"
}
```

**Example:**
```bash
curl -X GET "https://api.example.com/v1/resource" \
  -H "Authorization: Bearer <token>"
```

### POST /resource
<Description>

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|

**Request Body:**
```json
{
  "field": "type"
}
```

**Response 201:**
```json
{
  "field": "type"
}
```

**Example:**
```bash
curl -X POST "https://api.example.com/v1/resource" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```