"""
API Integration Examples and Use Cases
"""

# Example 1: Complete User Flow

## Registration and Login

POST /auth/register
{
  "email": "user@example.com",
  "username": "newuser",
  "full_name": "New User",
  "password": "SecurePassword123!"
}

Response:
{
  "id": "uuid-here",
  "email": "user@example.com",
  "username": "newuser",
  "full_name": "New User",
  "is_active": true,
  "is_verified": false,
  "subscription_tier": "free"
}

## Login

POST /auth/login
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}

--

# Example 2: Prompt Creation and Management

## Create a Prompt

POST /prompts
Headers: {
  "Authorization": "Bearer YOUR_TOKEN"
}
Body:
{
  "title": "Python Functions for Beginners",
  "description": "Learn Python functions with practical examples",
  "content": "Functions are reusable blocks of code...",
  "topic": "Python",
  "audience": "school",
  "skill_level": "beginner",
  "format": "tutorial",
  "category": "Programming",
  "tags": "python,functions,tutorial",
  "is_public": true
}

## Get My Prompts

GET /prompts/user/me?skip=0&limit=10
Headers: {
  "Authorization": "Bearer YOUR_TOKEN"
}

## Search Public Prompts

GET /prompts?topic=Python&audience=school&format=tutorial&skip=0&limit=10

## Interact with Prompt

POST /prompts/{prompt_id}/like

GET /prompts/{prompt_id}

--

# Example 3: User Profile

## Get Profile

GET /users/me
Headers: {
  "Authorization": "Bearer YOUR_TOKEN"
}

## Update Profile

PATCH /users/me
Headers: {
  "Authorization": "Bearer YOUR_TOKEN"
}
Body:
{
  "full_name": "Updated Name",
  "bio": "Python developer",
  "company": "Tech Company",
  "website": "https://example.com"
}

--

# Example 4: Integration with Applications

## Frontend Integration

const token = localStorage.getItem('token');
const response = await fetch('http://localhost:8000/prompts', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  }
});

## Mobile App Integration

Similar REST API can be consumed from iOS, Android, Flutter apps

## Third-party Services

The API can be integrated with:
- Learning management systems (LMS)
- Content management systems (CMS)
- Educational platforms
- AI/ML training systems
