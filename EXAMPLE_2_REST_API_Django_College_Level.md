# REST API Development with Python Django - College Level Complete Guide

**Target Audience:** College/University Students (Computer Science Major, 2nd-3rd Year)  
**Skill Level:** Intermediate  
**Topic:** Building RESTful APIs with Django and Django REST Framework  
**Formats Included:** Complete Tutorial + Code Repository + Lab Assignment + Best Practices + Architecture Diagram  
**Created:** April 2026

---

## PART 1: COMPREHENSIVE TUTORIAL

### What is a REST API?

**REST** = Representational State Transfer

An API that allows applications to communicate over HTTP using standard methods:
- **GET** - Retrieve data
- **POST** - Create data
- **PUT/PATCH** - Update data
- **DELETE** - Remove data

**Real-world analogy:** Think of a REST API like a restaurant menu system:
- **GET /menu** - See all available dishes
- **POST /order** - Place a new order
- **PUT /order/123** - Modify order 123
- **DELETE /order/123** - Cancel order 123

---

### Architecture Overview

```
┌──────────────────────────────────────────────────┐
│  CLIENT (Mobile App, Web Browser, Another API)  │
└────────────────────┬─────────────────────────────┘
                     │ HTTP Requests
                     │ (GET, POST, PUT, DELETE)
                     ▼
┌──────────────────────────────────────────────────┐
│  DJANGO REST API SERVER                          │
│  ┌────────────────────────────────────────────┐  │
│  │  URLs (Routes)                             │  │
│  │  /api/users/ - Get all users               │  │
│  │  /api/users/{id}/ - Get specific user      │  │
│  └────────────────────────────────────────────┘  │
│                     ▼                             │
│  ┌────────────────────────────────────────────┐  │
│  │  Views (Logic)                             │  │
│  │  Handles requests, processes data          │  │
│  └────────────────────────────────────────────┘  │
│                     ▼                             │
│  ┌────────────────────────────────────────────┐  │
│  │  Serializers (Data Conversion)             │  │
│  │  Converts Python objects ↔ JSON            │  │
│  └────────────────────────────────────────────┘  │
│                     ▼                             │
│  ┌────────────────────────────────────────────┐  │
│  │  Models (Database)                         │  │
│  │  Stores actual data                        │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
                     │ HTTP Responses
                     │ (JSON data + Status codes)
                     ▼
┌──────────────────────────────────────────────────┐
│  CLIENT RECEIVES RESPONSE                        │
│  {                                               │
│    "id": 1,                                      │
│    "name": "John Doe",                           │
│    "email": "john@example.com"                   │
│  }                                               │
└──────────────────────────────────────────────────┘
```

---

### Step-by-Step: Build Your First API

#### Step 1: Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install django djangorestframework
pip install django-cors-headers  # For cross-origin requests

# Create Django project
django-admin startproject myapi
cd myapi

# Create Django app
python manage.py startapp api
```

---

#### Step 2: Create Models (Database Structure)

**File: api/models.py**

```python
from django.db import models

class Student(models.Model):
    """Model to store student information"""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=20, unique=True)
    gpa = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']  # Newest first
    
    def __str__(self):
        return f"{self.name} ({self.roll_number})"

class Assignment(models.Model):
    """Model to store assignments"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted = models.BooleanField(default=False)
    grade = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.student.name}"
```

**What each field means:**
- `CharField` - Text field (limited length)
- `EmailField` - Email validation included
- `FloatField` - Decimal numbers
- `DateField` - Dates
- `ForeignKey` - Link to another model
- `auto_now_add=True` - Auto-set on creation

---

#### Step 3: Create Serializers (Convert to JSON)

**File: api/serializers.py**

```python
from rest_framework import serializers
from .models import Student, Assignment

class AssignmentSerializer(serializers.ModelSerializer):
    """Serializer for Assignment model"""
    
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'due_date', 'submitted', 'grade']

class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    
    # Include nested assignments
    assignments = AssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'roll_number', 'gpa', 'assignments']
    
    def validate_email(self, value):
        """Custom validation for email"""
        if Student.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered")
        return value
```

---

#### Step 4: Create Views (Handle Requests)

**File: api/views.py**

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Assignment
from .serializers import StudentSerializer, AssignmentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Student operations
    Handles: GET, POST, PUT, DELETE
    """
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        """Get all assignments for a student"""
        student = self.get_object()
        assignments = student.assignment_set.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get students with GPA > 3.5"""
        students = Student.objects.filter(gpa__gt=3.5)
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)

class AssignmentViewSet(viewsets.ModelViewSet):
    """API endpoint for Assignment operations"""
    
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    
    def get_queryset(self):
        """Filter assignments by student if student_id provided"""
        queryset = Assignment.objects.all()
        student_id = self.request.query_params.get('student_id')
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        return queryset
```

---

#### Step 5: Configure URLs (Routes)

**File: api/urls.py**

```python
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for automatic URL generation
router = DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'assignments', views.AssignmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```

**File: myapi/urls.py**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include API URLs
]
```

---

#### Step 6: Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (for admin)
python manage.py createsuperuser

# Run server
python manage.py runserver
# API is now at: http://127.0.0.1:8000/api/
```

---

### Complete API Examples (Request & Response)

#### GET All Students
**Request:**
```
GET /api/students/
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "roll_number": "CS-2023-001",
    "gpa": 3.8,
    "assignments": [
      {
        "id": 1,
        "title": "Python Project",
        "description": "Build a todo app",
        "due_date": "2026-05-01",
        "submitted": true,
        "grade": 95
      }
    ]
  },
  {
    "id": 2,
    "name": "Bob Smith",
    "email": "bob@example.com",
    "roll_number": "CS-2023-002",
    "gpa": 3.5,
    "assignments": []
  }
]
```

---

#### POST Create New Student
**Request:**
```
POST /api/students/
Content-Type: application/json

{
  "name": "Charlie Davis",
  "email": "charlie@example.com",
  "roll_number": "CS-2023-003",
  "gpa": 3.7
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "Charlie Davis",
  "email": "charlie@example.com",
  "roll_number": "CS-2023-003",
  "gpa": 3.7,
  "assignments": []
}
```

---

#### PUT Update Student
**Request:**
```
PUT /api/students/1/
Content-Type: application/json

{
  "name": "Alice Johnson Updated",
  "gpa": 3.9
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Alice Johnson Updated",
  "email": "alice@example.com",
  "roll_number": "CS-2023-001",
  "gpa": 3.9,
  "assignments": []
}
```

---

#### DELETE Student
**Request:**
```
DELETE /api/students/2/
```

**Response (204 No Content):**
```
No content returned
(Student successfully deleted)
```

---

## PART 2: BEST PRACTICES

### 1. Authentication & Permissions

```python
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    # Only authenticated users can access
```

### 2. Pagination (For Large Results)

```python
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    
# In views.py:
pagination_class = StandardPagination
```

### 3. Filtering & Search

```python
from django_filters import rest_framework
from rest_framework.filters import SearchFilter

class StudentViewSet(viewsets.ModelViewSet):
    filter_backends = [rest_framework.DjangoFilterBackend, SearchFilter]
    filterset_fields = ['gpa']
    search_fields = ['name', 'email']
    
# Usage: /api/students/?gpa__gt=3.5&search=alice
```

### 4. Caching

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def get_students(request):
    # Returns cached response
    pass
```

---

## PART 3: LAB ASSIGNMENT

### Assignment: Build a Blog API

**Objective:** Create a complete REST API for a blogging platform

**Requirements:**

1. **Models:**
   - `Author` - Name, bio, email
   - `BlogPost` - Title, content, author, date_created, published
   - `Comment` - Text, author, post, date_created

2. **API Endpoints:**
   - GET /api/posts/ - List all posts
   - POST /api/posts/ - Create new post
   - GET /api/posts/{id}/ - Get specific post
   - PUT /api/posts/{id}/ - Update post
   - DELETE /api/posts/{id}/ - Delete post
   - GET /api/posts/{id}/comments/ - Get comments for post
   - POST /api/comments/ - Create comment

3. **Features:**
   - Only authenticated users can create/edit posts
   - Filter posts by author
   - Search posts by title/content
   - Pagination for large result sets
   - Custom action to get published posts only

**Starter Code:**
```python
# models.py - Create Author, BlogPost, Comment models
# serializers.py - Create serializers for each model
# views.py - Create ViewSets for CRUD operations
# urls.py - Configure API routes
# Implement all requirements above
```

**Submission Checklist:**
- [ ] All models created correctly
- [ ] All serializers working
- [ ] All endpoints functional
- [ ] Tested with Postman/curl
- [ ] Authentication implemented
- [ ] Documentation included

**Grading:**
- Models & serializers: 30%
- API endpoints: 40%
- Features & extras: 20%
- Code quality: 10%

---

## PART 4: TESTING API WITH CURL

```bash
# Get all students
curl http://127.0.0.1:8000/api/students/

# Create new student
curl -X POST http://127.0.0.1:8000/api/students/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Student",
    "email": "new@example.com",
    "roll_number": "CS-2023-999",
    "gpa": 3.6
  }'

# Update student (ID=1)
curl -X PUT http://127.0.0.1:8000/api/students/1/ \
  -H "Content-Type: application/json" \
  -d '{"gpa": 3.95}'

# Delete student (ID=2)
curl -X DELETE http://127.0.0.1:8000/api/students/2/

# Filter: Get with GPA > 3.5
curl "http://127.0.0.1:8000/api/students/?gpa__gt=3.5"

# Search: Find students with "alice" in name
curl "http://127.0.0.1:8000/api/students/?search=alice"
```

---

## PART 5: COMMON ERRORS & SOLUTIONS

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError: No module named 'rest_framework'` | DRF not installed | `pip install djangorestframework` |
| `Page not found (404)` | Wrong URL | Check urls.py configuration |
| `IntegrityError - duplicate email` | Email already exists | Add unique validation |
| `PermissionDenied` | Not authenticated | Add authentication token |
| `ValidationError` | Invalid data | Check serializer validation |

---

## NEXT STEPS

1. ✓ Understand REST API concepts
2. ✓ Build basic CRUD API
3. → Add authentication
4. → Add advanced filtering
5. → Deploy to production
6. → Add API documentation

---

*Complete College-Level Tutorial | Intermediate | Production Examples Included*  
*Created: April 2026 | Ready to Teach/Learn*
