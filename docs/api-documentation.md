====================================================================================================
JOBBRIDGE — COMPLETE REST API DOCUMENTATION
====================================================================================================
Version: 1.0.0
Base URL: http://localhost:8000
Content-Type: application/json

The JobBridge API is built with Django REST Framework. It uses JWT (JSON Web Tokens) 
for authentication. All endpoints return JSON.

====================================================================================================
🔐 AUTHENTICATION
====================================================================================================
Most endpoints require a valid JWT in the request header.

Header Format:
Authorization: Bearer <your_access_token>

If you receive a 401 Unauthorized response, your token has expired. Use the Refresh 
Token endpoint to get a new one.

====================================================================================================
👤 ACCOUNTS & AUTH
====================================================================================================

----------------------------------------------------------------------------------------------------
1. REGISTER
----------------------------------------------------------------------------------------------------
Creates a new user account (Candidate or Employer) and returns JWT tokens.

• URL: /accounts/api/register/
• Method: POST
• Auth Required: No (Public)

Request Body:
--------------------------------------------------
Field               | Type      | Required | Description
--------------------------------------------------
email               | string    | Yes      | Unique email address
password            | string    | Yes      | Minimum 8 characters
password_confirm    | string    | Yes      | Must match `password`
first_name          | string    | Yes      | User's first name
last_name           | string    | Yes      | User's last name
role                | string    | Yes      | Either "candidate" or "employer"
company_name        | string    | No       | Required only if role="employer"
--------------------------------------------------

Example Request:
{
  "email": "jane.doe@example.com",
  "password": "StrongPass!123",
  "password_confirm": "StrongPass!123",
  "first_name": "Jane",
  "last_name": "Doe",
  "role": "candidate"
}

Success Response (201 Created):
{
  "user": {
    "id": 1,
    "email": "jane.doe@example.com",
    "full_name": "Jane Doe",
    "role": "candidate"
  },
  "tokens": {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5c...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5c..."
  }
}

----------------------------------------------------------------------------------------------------
2. LOGIN
----------------------------------------------------------------------------------------------------
Authenticates a user and returns a fresh set of JWT tokens.

• URL: /accounts/api/login/
• Method: POST
• Auth Required: No (Public)

Request Body:
--------------------------------------------------
Field               | Type      | Required | Description
--------------------------------------------------
identifier          | string    | Yes      | User's email or username
password            | string    | Yes      | User's password
--------------------------------------------------

Example Request:
{
  "identifier": "jane.doe@example.com",
  "password": "StrongPass!123"
}

Success Response (200 OK):
{
  "user": { ... },
  "tokens": {
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5c...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5c..."
  }
}

----------------------------------------------------------------------------------------------------
3. REFRESH TOKEN
----------------------------------------------------------------------------------------------------
Exchange a valid refresh token for a new access token (without logging in again).

• URL: /accounts/api/token/refresh/
• Method: POST
• Auth Required: No

Request Body:
{
  "refresh": "your_refresh_token_here"
}

Success Response (200 OK):
{
  "access": "new_access_token_here"
}

====================================================================================================
💼 JOBS
====================================================================================================

----------------------------------------------------------------------------------------------------
1. LIST JOBS
----------------------------------------------------------------------------------------------------
Retrieve a paginated list of job postings. Supports extensive filtering and search.

• URL: /api/
• Method: GET
• Auth Required: No (Public)

Query Parameters:
--------------------------------------------------
Parameter           | Type      | Description
--------------------------------------------------
q                   | string    | Search by job title or description
location            | string    | Filter by location (e.g., "Remote")
job_type            | string    | full_time, part_time, contract, internship, remote
category            | integer   | Filter by Category ID
is_remote           | boolean   | true or false
salary_min          | integer   | Minimum salary
page                | integer   | Pagination page number
--------------------------------------------------

Example Request:
GET /api/?q=python&location=remote&job_type=full_time

Success Response (200 OK):
{
  "count": 45,
  "next": "http://localhost:8000/api/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Senior Python Developer",
      "company_name": "Tech Corp",
      "location": "Remote",
      "salary_range": "$100k - $130k",
      "job_type": "full_time",
      "is_featured": true
    }
  ]
}

----------------------------------------------------------------------------------------------------
2. RETRIEVE JOB DETAILS
----------------------------------------------------------------------------------------------------
Get the complete details of a specific job.

• URL: /api/<id>/
• Method: GET
• Auth Required: No

Success Response (200 OK):
{
  "id": 1,
  "title": "Senior Python Developer",
  "description": "We are looking for...",
  "requirements": "5+ years experience...",
  "responsibilities": "Build REST APIs...",
  "company_name": "Tech Corp",
  "salary_min": 100000,
  "salary_max": 130000
}

----------------------------------------------------------------------------------------------------
3. CREATE JOB
----------------------------------------------------------------------------------------------------
Post a new job opening.

• URL: /api/
• Method: POST
• Auth Required: Yes (Bearer <token>) - Role: Employer

Request Body:
--------------------------------------------------
Field               | Type      | Required | Description
--------------------------------------------------
title               | string    | Yes      | Job title
description         | string    | Yes      | Full job description
requirements        | string    | No       | Job requirements
responsibilities    | string    | No       | Job responsibilities
category            | integer   | No       | Job Category ID
job_type            | string    | Yes      | e.g., full_time
location            | string    | Yes      | e.g., "New York, NY"
is_remote           | boolean   | No       | Default: false
salary_min          | decimal   | No       | e.g., 80000
salary_max          | decimal   | No       | e.g., 120000
--------------------------------------------------

Example Request:
{
  "title": "Frontend React Developer",
  "description": "We need a React expert...",
  "job_type": "full_time",
  "location": "Remote",
  "is_remote": true,
  "salary_min": 85000,
  "salary_max": 110000
}

Success Response (201 Created):
Returns the newly created Job object.

====================================================================================================
📄 APPLICATIONS
====================================================================================================

----------------------------------------------------------------------------------------------------
1. APPLY TO JOB
----------------------------------------------------------------------------------------------------
Submit an application for a specific job.

• URL: /applications/api/
• Method: POST
• Auth Required: Yes (Bearer <token>) - Role: Candidate

Request Body:
--------------------------------------------------
Field               | Type      | Required | Description
--------------------------------------------------
job                 | integer   | Yes      | The ID of the job you are applying to
cover_letter        | string    | No       | Your cover letter text
resume              | file      | No       | Optional resume file (PDF/DOCX)
--------------------------------------------------

Example Request:
{
  "job": 5,
  "cover_letter": "I am very interested in this role..."
}

Success Response (201 Created):
{
  "id": 12,
  "job_title": "Senior Python Developer",
  "status": "applied",
  "created_at": "2026-11-10T12:00:00Z"
}

----------------------------------------------------------------------------------------------------
2. GET MY APPLICATIONS
----------------------------------------------------------------------------------------------------
Retrieve a list of all applications submitted by the logged-in Candidate.

• URL: /applications/api/
• Method: GET
• Auth Required: Yes (Bearer <token>) - Role: Candidate

Success Response (200 OK):
[
  {
    "id": 12,
    "job_title": "Senior Python Developer",
    "company_name": "Tech Corp",
    "status": "shortlisted",
    "created_at": "2026-11-10T12:00:00Z"
  }
]

====================================================================================================
⚠️ ERROR HANDLING
====================================================================================================
All errors return a consistent JSON structure to make error handling easy on the frontend.

Validation Error (400 Bad Request):
{
  "detail": "Validation failed.",
  "errors": {
    "email": ["A user with that email already exists."],
    "password": ["This password is too short."]
  }
}

Authentication Error (401 Unauthorized):
{
  "detail": "Authentication credentials were not provided."
}

Permission Error (403 Forbidden):
{
  "detail": "You do not have permission to perform this action."
}