# JobBridge 🌉

**Connecting Talent with Opportunity**

JobBridge is a modern, full-stack job portal platform built with
**Python, Django 5, Django REST Framework (DRF), HTML5, CSS3, and
Vanilla JavaScript**.

The platform connects job seekers with employers through dedicated
candidate and employer experiences, while providing administrators with
tools to manage the recruitment ecosystem.

JobBridge uses a modular Django backend, a responsive frontend, RESTful
APIs, and a relational database to provide a scalable foundation for
recruitment and job management.

------------------------------------------------------------------------

## 📖 Table of Contents

1.  [Project Overview](#-project-overview)
2.  [Features](#-features)
3.  [Technology Stack](#️-technology-stack)
4.  [System Architecture](#️-system-architecture)
5.  [Project Structure](#-project-structure)
6.  [Database Design](#️-database-design)
7.  [Authentication and
    Authorization](#-authentication-and-authorization)
8.  [API Documentation](#-api-documentation)
9.  [Installation and Setup](#-installation-and-setup)
10. [Environment Variables](#-environment-variables)
11. [Running the Application](#-running-the-application)
12. [Testing](#-testing)
13. [Deployment](#-deployment)
14. [Security](#-security)
15. [Future Improvements](#-future-improvements)
16. [License](#-license)

------------------------------------------------------------------------

## 🌟 Project Overview

JobBridge is designed to simplify the recruitment process by bringing
candidates and employers together on a single platform.

Candidates can create professional profiles, upload resumes, discover
job opportunities, submit applications, and track their recruitment
progress.

Employers can create company profiles, publish job vacancies, manage job
listings, review applications, shortlist candidates, and organize
interviews.

Administrators can oversee platform activities, manage users, moderate
job listings, and monitor overall system performance.

### Main User Roles

  -----------------------------------------------------------------------
  Role                                Responsibilities
  ----------------------------------- -----------------------------------
  Candidate                           Create profiles, search jobs,
                                      apply, and track applications

  Employer                            Manage companies, publish jobs, and
                                      review applicants

  Administrator                       Manage users, jobs, companies, and
                                      platform operations
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## ✨ Features

### 👨‍💻 Candidate Features

-   Candidate registration and login.
-   Professional candidate profile management.
-   Profile picture and resume uploads.
-   Education and work experience management.
-   Technical and professional skills management.
-   Job searching and filtering.
-   Job details and company information.
-   Save jobs for later.
-   Apply for job opportunities.
-   Submit cover letters.
-   Track application progress.
-   View application history.
-   Receive application notifications.

### 🏢 Employer Features

-   Employer registration and authentication.
-   Company profile creation and management.
-   Company logo and information management.
-   Create and publish job vacancies.
-   Edit, update, and delete job listings.
-   Manage active and inactive vacancies.
-   View applications received.
-   Search and filter applicants.
-   Review candidate profiles and resumes.
-   Shortlist or reject applicants.
-   Manage recruitment statuses.
-   Schedule candidate interviews.

### 🛡️ Administrator Features

-   Secure Django administration.
-   User management.
-   Candidate and employer management.
-   Company verification and moderation.
-   Job listing management.
-   Application monitoring.
-   Category management.
-   Platform statistics and reports.
-   Administrative oversight.

### 🌐 General Platform Features

-   Responsive and modern user interface.
-   Reusable HTML components and layouts.
-   Custom CSS design system.
-   Vanilla JavaScript interactions.
-   Django REST Framework APIs.
-   JWT-based API authentication.
-   Django session authentication for web pages.
-   Email verification workflows.
-   Password reset functionality.
-   Role-based permissions.
-   In-app notifications.
-   Secure file uploads.
-   Search, filtering, and pagination.

> Feature availability depends on the implementation of the
> corresponding backend and frontend modules.

------------------------------------------------------------------------

## 🛠️ Technology Stack

### Backend

  Technology              Purpose
  ----------------------- ---------------------------
  Python 3.11+            Main programming language
  Django 5.x              Backend web framework
  Django REST Framework   REST API development
  Simple JWT              JWT authentication
  django-filter           API filtering
  Gunicorn                Production WSGI server

### Frontend

  Technology           Purpose
  -------------------- --------------------------------
  HTML5                Website structure
  CSS3                 Styling and responsive layouts
  Vanilla JavaScript   Frontend functionality
  Fetch API            Backend API communication
  CSS Variables        Reusable design system
  Google Fonts         Typography

### Database and Storage

  Technology            Purpose
  --------------------- -----------------------------------
  PostgreSQL            Production relational database
  SQLite                Local development database option
  Django ORM            Database operations
  Django File Storage   Resume and media management

### Development and Deployment

  Technology       Purpose
  ---------------- ---------------------------------------
  Git              Version control
  GitHub           Source code management
  Docker           Application containerization
  Docker Compose   Multi-container management
  Nginx            Reverse proxy and static file serving
  Pytest           Automated testing
  Playwright       End-to-end browser testing

------------------------------------------------------------------------

## 🏗️ System Architecture

JobBridge follows a **modular Django monolithic architecture** with a
separate presentation layer and REST API layer.

The same Django project handles both HTML page rendering and API
requests.

### Architecture Components

**1. Frontend Layer**

-   HTML pages rendered through Django templates.
-   Custom CSS for styling and responsive layouts.
-   Vanilla JavaScript for dynamic interactions.
-   Fetch API for asynchronous communication with backend endpoints.

**2. Backend Layer**

-   Django handles application logic and server-side rendering.
-   Django REST Framework handles API requests and responses.
-   Serializers validate and transform API data.
-   Models define database entities.
-   Views and services handle application operations.
-   Permissions enforce user access restrictions.

**3. Database Layer**

-   PostgreSQL for production.
-   SQLite as an optional development database.
-   Django ORM for database queries and relationships.

**4. Authentication Layer**

-   Django sessions for browser-based authentication.
-   JWT access and refresh tokens for REST API authentication.
-   Role-based permissions for candidates, employers, and
    administrators.

### Request Flow

``` text
             USER
               |
               v
       FRONTEND INTERFACE
       HTML + CSS + JavaScript
               |
               v
        DJANGO APPLICATION
               |
        +------+------+
        |             |
        v             v
    HTML VIEWS     REST API
        |             |
        |             v
        |           DRF
        |             |
        |        SERIALIZERS
        |             |
        +------+------+
               |
               v
          DJANGO ORM
               |
               v
          DATABASE
        PostgreSQL
```

------------------------------------------------------------------------

## 📂 Project Structure

The following structure represents the recommended organization of the
JobBridge application.

``` text
JobBridge/
│
├── backend/
│   │
│   ├── apps/
│   │   │
│   │   ├── accounts/
│   │   │   ├── migrations/
│   │   │   ├── api/
│   │   │   ├── services/
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── urls.py
│   │   │   ├── views.py
│   │   │   └── tests.py
│   │   │
│   │   ├── candidates/
│   │   ├── companies/
│   │   ├── jobs/
│   │   ├── applications/
│   │   ├── interviews/
│   │   ├── notifications/
│   │   ├── reviews/
│   │   └── admin_panel/
│   │
│   ├── common/
│   │   ├── permissions/
│   │   ├── mixins/
│   │   ├── middleware/
│   │   ├── exceptions/
│   │   ├── utils/
│   │   └── validators/
│   │
│   ├── config/
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   │
│   │   ├── __init__.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── templates/
│   │   ├── base/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── accounts/
│   │   ├── candidates/
│   │   ├── companies/
│   │   ├── jobs/
│   │   ├── applications/
│   │   └── dashboards/
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   │
│   ├── media/
│   │   ├── resumes/
│   │   ├── profiles/
│   │   └── companies/
│   │
│   ├── tests/
│   │   ├── test_accounts.py
│   │   ├── test_candidates.py
│   │   ├── test_companies.py
│   │   ├── test_jobs.py
│   │   └── test_applications.py
│   │
│   ├── manage.py
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── .env.example
│   └── .gitignore
│
├── docker/
│   ├── Dockerfile
│   └── nginx/
│       └── default.conf
│
├── docker-compose.yml
├── .gitignore
├── LICENSE
└── README.md
```

### Main Django Applications

  Application     Responsibility
  --------------- ---------------------------------------------------
  accounts        Custom user model, authentication, registration
  candidates      Candidate profiles, skills, education, experience
  companies       Employer and company management
  jobs            Job postings, categories, search and filtering
  applications    Job applications and application statuses
  interviews      Interview scheduling and management
  notifications   In-app notification management
  reviews         Company reviews and ratings
  admin_panel     Custom administrative functionality

------------------------------------------------------------------------

## 🗄️ Database Design

JobBridge uses Django ORM to manage database operations and
relationships.

### Core Database Models

**1. User (`accounts.User`)**

Custom user model extending Django's authentication system.

Fields may include:

-   id
-   email
-   password
-   first_name
-   last_name
-   role
-   is_active
-   is_staff
-   date_joined

Email is used as the primary login identifier.

Roles include Candidate and Employer. Administrative access should be
controlled through Django staff and superuser permissions.

**2. CandidateProfile (`candidates.CandidateProfile`)**

One-to-one relationship with User.

Stores:

-   Profile information.
-   Resume.
-   Profile picture.
-   Biography.
-   Skills.
-   Education.
-   Work experience.
-   Portfolio URL.

**3. Company (`companies.Company`)**

Stores:

-   Company name.
-   Company description.
-   Logo.
-   Website.
-   Industry.
-   Location.
-   Employer relationship.

**4. Job (`jobs.Job`)**

Stores:

-   Job title.
-   Description.
-   Requirements.
-   Responsibilities.
-   Salary range.
-   Location.
-   Employment type.
-   Experience level.
-   Company relationship.
-   Category relationship.
-   Publication status.

**5. Application (`applications.Application`)**

Connects a CandidateProfile to a Job.

Stores:

-   Candidate.
-   Job.
-   Cover letter.
-   Resume snapshot, if implemented.
-   Application status.
-   Application date.

A unique database constraint should prevent the same candidate from
applying to the same job more than once.

**6. Interview (`interviews.Interview`)**

Connects an interview to an application.

Stores:

-   Application.
-   Interview date and time.
-   Meeting link.
-   Interview type.
-   Interview status.
-   Interview notes.

**7. Notification (`notifications.Notification`)**

Stores user notifications, including:

-   Notification title.
-   Notification message.
-   Notification type.
-   Read/unread status.
-   Creation timestamp.

### Main Database Relationships

``` text
User
 |
 +---- CandidateProfile
 |           |
 |           +---- Applications
 |                    |
 |                    +---- Job
 |                    |      |
 |                    |      +---- Company
 |                    |
 |                    +---- Interview
 |
 +---- Employer / Company
                |
                +---- Jobs
                       |
                       +---- Applications
```

------------------------------------------------------------------------

## 🔐 Authentication and Authorization

JobBridge uses two authentication mechanisms.

### Django Session Authentication

Used for browser-based pages and dashboards.

-   Login creates an authenticated session.
-   Protected pages require authentication.
-   Logout terminates the session.
-   CSRF protection is enabled for unsafe requests.

### JWT Authentication

Used for REST API authentication through Django REST Framework and
Simple JWT.

JWT consists of:

-   Access token.
-   Refresh token.

Example API request:

``` http
GET /api/v1/jobs/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Role-Based Access Control

  Permission              Candidate   Employer   Admin
  ----------------------- ----------- ---------- ---------------
  View public jobs        Yes         Yes        Yes
  Apply for jobs          Yes         No         As authorized
  Save jobs               Yes         No         As authorized
  Create job listings     No          Yes        Yes
  Manage company          No          Yes        Yes
  View applicants         No          Yes        Yes
  Manage platform users   No          No         Yes

All permissions must also be enforced on the backend, not just hidden in
the frontend.

------------------------------------------------------------------------

## 🔌 API Documentation

JobBridge uses Django REST Framework to expose RESTful API endpoints.

**Base API URL:**

``` text
http://127.0.0.1:8000/api/v1/
```

The following is the recommended API endpoint convention. Actual
endpoint availability depends on the project's URL configuration.

### Authentication Endpoints

  Method   Endpoint                              Description
  -------- ------------------------------------- -----------------------------
  POST     `/accounts/register/`                 Register an account
  POST     `/accounts/login/`                    Authenticate user
  POST     `/accounts/token/refresh/`            Refresh JWT token
  POST     `/accounts/logout/`                   Logout / token invalidation
  POST     `/accounts/password/reset/`           Request password reset
  POST     `/accounts/password/reset/confirm/`   Confirm password reset

### Job Endpoints

  Method      Endpoint              Description
  ----------- --------------------- ----------------------
  GET         `/jobs/`              List available jobs
  GET         `/jobs/{id}/`         Retrieve job details
  POST        `/jobs/`              Create a job
  PUT/PATCH   `/jobs/{id}/`         Update a job
  DELETE      `/jobs/{id}/`         Delete a job
  GET         `/jobs/categories/`   List job categories
  POST        `/jobs/{id}/save/`    Save a job

### Application Endpoints

  Method   Endpoint                       Description
  -------- ------------------------------ ---------------------------
  POST     `/applications/`               Submit a job application
  GET      `/applications/`               List applications
  GET      `/applications/{id}/`          View application details
  PATCH    `/applications/{id}/status/`   Update application status

### Candidate Endpoints

  Method      Endpoint                 Description
  ----------- ------------------------ ------------------------
  GET         `/candidates/profile/`   View candidate profile
  PUT/PATCH   `/candidates/profile/`   Update profile
  POST        `/candidates/resume/`    Upload resume

### Company Endpoints

  Method   Endpoint             Description
  -------- -------------------- ------------------------
  GET      `/companies/`        List companies
  GET      `/companies/{id}/`   View company details
  POST     `/companies/`        Create company profile
  PATCH    `/companies/{id}/`   Update company profile

### API Filtering and Pagination

Job listings should support query parameters such as:

``` text
/api/v1/jobs/?search=python
/api/v1/jobs/?location=Berlin
/api/v1/jobs/?job_type=full_time
/api/v1/jobs/?search=developer&location=Germany
/api/v1/jobs/?page=2
```

### Standard API Response

Example successful response:

``` json
{
    "success": true,
    "message": "Jobs retrieved successfully.",
    "data": []
}
```

Example validation error:

``` json
{
    "success": false,
    "message": "Validation failed.",
    "errors": {
        "email": [
            "This field is required."
        ]
    }
}
```

> Response formats should follow the actual serializers, views, and
> exception handlers implemented in the project.

------------------------------------------------------------------------

## 🚀 Installation and Setup

### Prerequisites

Install the following:

-   Python 3.11 or later.
-   Git.
-   pip.
-   PostgreSQL (if using PostgreSQL locally).
-   A code editor such as Visual Studio Code.

### 1. Clone the Repository

``` bash
git clone https://github.com/YOUR_USERNAME/JobBridge.git
cd JobBridge
```

### 2. Navigate to Backend

``` bash
cd backend
```

### 3. Create Virtual Environment

**Windows PowerShell:**

``` powershell
python -m venv .venv
```

Activate it:

``` powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create your local environment file.

**Windows PowerShell:**

``` powershell
Copy-Item .env.example .env
```

**Linux/macOS:**

``` bash
cp .env.example .env
```

Update the environment variables according to your local configuration.

### 6. Run Database Migrations

For development settings:

``` bash
python manage.py makemigrations
python manage.py migrate
```

If migrations are already included in the repository, running `migrate`
is normally sufficient.

### 7. Create Administrator Account

``` bash
python manage.py createsuperuser
```

Follow the instructions to create an administrator.

### 8. Run Development Server

``` bash
python manage.py runserver
```

The application should now be accessible at:

-   Website: http://127.0.0.1:8000/
-   Django Admin: http://127.0.0.1:8000/admin/
-   API: http://127.0.0.1:8000/api/v1/

------------------------------------------------------------------------

## ⚙️ Environment Variables

The `.env` file stores sensitive configuration values.

Example `.env.example`:

``` env
# Django Configuration
DJANGO_SECRET_KEY=replace-with-a-secure-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Django Settings Module
DJANGO_SETTINGS_MODULE=config.settings.development

# Database Configuration
DATABASE_URL=sqlite:///db.sqlite3

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
DEFAULT_FROM_EMAIL=

# Frontend Configuration
FRONTEND_URL=http://127.0.0.1:8000

# JWT Configuration
JWT_ACCESS_TOKEN_LIFETIME=15
JWT_REFRESH_TOKEN_LIFETIME=7
```

For PostgreSQL, configure `DATABASE_URL` using your actual database
credentials and a compatible database URL parser.

**Important:**

-   Never commit your actual `.env` file.
-   Never expose your Django secret key.
-   Never upload production database credentials to GitHub.
-   Use separate development and production configurations.
-   Set `DJANGO_DEBUG=False` in production.

------------------------------------------------------------------------

## ▶️ Running the Application

### Development Mode

Make sure your virtual environment is activated.

``` powershell
$env:DJANGO_SETTINGS_MODULE="config.settings.development"
python manage.py runserver
```

### Django System Checks

``` bash
python manage.py check
```

### Check Database Migrations

``` bash
python manage.py showmigrations
```

### Collect Static Files

``` bash
python manage.py collectstatic --noinput
```

------------------------------------------------------------------------

## 🧪 Testing

JobBridge uses automated testing to verify application functionality and
prevent regressions.

### Run Django Tests

``` bash
python manage.py test
```

### Run Pytest

If Pytest and pytest-django are configured:

``` bash
pytest
```

### Run a Specific Test File

``` bash
pytest apps/jobs/tests.py
```

### End-to-End Testing

If the Playwright test script is included and configured:

``` bash
python e2e_bot.py
```

### Recommended Testing Areas

-   User registration and login.
-   JWT authentication.
-   Role-based permissions.
-   Candidate profile management.
-   Company profile management.
-   Job creation and updating.
-   Job searching and filtering.
-   Job application submission.
-   Duplicate application prevention.
-   Application status updates.
-   Resume uploads.
-   Password reset.
-   API validation and error handling.

------------------------------------------------------------------------

## 🐳 Deployment

JobBridge is designed to support deployment using Docker, Gunicorn,
PostgreSQL, and Nginx.

### Recommended Production Architecture

``` text
             INTERNET
                 |
                 v
              NGINX
                 |
                 v
             GUNICORN
                 |
                 v
          DJANGO APPLICATION
                 |
          +------+------+
          |             |
          v             v
      POSTGRESQL      MEDIA
          |
          v
       DATABASE
```

### Docker Deployment

From the project root:

``` bash
docker compose up -d --build
```

Check running containers:

``` bash
docker compose ps
```

View application logs:

``` bash
docker compose logs -f
```

Stop containers:

``` bash
docker compose down
```

> These commands require a correctly configured Dockerfile and
> docker-compose.yml.

### Manual Deployment (Ubuntu)

1.  Install Python and required system packages.
2.  Install and configure PostgreSQL.
3.  Create a production database and database user.
4.  Configure production environment variables.
5.  Install Python dependencies.
6.  Run Django migrations.
7.  Collect static files.
8.  Configure Gunicorn.
9.  Configure Nginx as a reverse proxy.
10. Enable HTTPS using a valid SSL certificate.

Example Gunicorn command:

``` bash
gunicorn --workers 3 --bind 127.0.0.1:8000 config.wsgi:application
```

Configure a process manager such as systemd to keep Gunicorn running.

------------------------------------------------------------------------

## 🔒 Security

Security is an important part of JobBridge.

Recommended production security configurations:

-   Set `DEBUG=False`.
-   Use a strong and private `SECRET_KEY`.
-   Configure `ALLOWED_HOSTS`.
-   Enable HTTPS.
-   Set `SECURE_SSL_REDIRECT=True` when HTTPS is correctly configured.
-   Enable secure session cookies.
-   Enable secure CSRF cookies.
-   Use Django's CSRF protection.
-   Validate uploaded files.
-   Restrict resume and media file access.
-   Apply role-based permissions on every protected API.
-   Use environment variables for credentials.
-   Apply authentication rate limiting.
-   Keep dependencies updated.
-   Use database constraints to prevent duplicate applications.

Run the Django deployment security checks:

``` bash
python manage.py check --deploy
```

------------------------------------------------------------------------

## 🚧 Future Improvements

Potential future enhancements include:

-   Advanced job recommendation system.
-   AI-powered resume analysis.
-   Resume-to-job matching.
-   Intelligent candidate ranking.
-   AI-assisted job description generation.
-   Real-time notifications.
-   Email notification integration.
-   Advanced recruitment analytics.
-   Interview calendar integration.
-   Company verification workflows.
-   Advanced search and filtering.
-   Application tracking analytics.

------------------------------------------------------------------------

## 📄 License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

------------------------------------------------------------------------

## 👨‍💻 Author

**JobBridge --- Connecting Talent with Opportunity**

Built with Python, Django, Django REST Framework, HTML, CSS, and
JavaScript.

**GitHub:** https://github.com/YOUR_USERNAME/JobBridge

------------------------------------------------------------------------

⭐ If you find this project useful, consider giving it a star on GitHub.

**JobBridge --- Your Career. Your Opportunity. Your Future.**
