# API Documentation

## JWT Authentication
- `POST /api/token/` - Get access/refresh tokens
- `POST /api/token/refresh/` - Refresh access token

## Course Endpoints  
- `GET /api/education/courses/` - List courses
- `POST /api/education/courses/` - Create course
- `GET /api/education/courses/{id}/` - Get course details
- `PUT /api/education/courses/{id}/` - Update course
- `DELETE /api/education/courses/{id}/` - Delete course
- `POST /api/education/courses/{id}/activate/` - Activate course
- `POST /api/education/courses/{id}/deactivate/` - Deactivate course  
- `GET /api/education/courses/{id}/lessons/` - List course lessons

## Lesson Endpoints
- `POST /api/education/lessons/` - Create lesson
- `PUT /api/education/lessons/{id}/move/` - Move lesson
- `DELETE /api/education/lessons/{id}/` - Delete lesson
- `POST /api/education/lessons/{id}/publish/` - Publish lesson
- `POST /api/education/lessons/{id}/unpublish/` - Unpublish lesson