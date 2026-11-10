====================================================================================================
JOBBRIDGE — SYSTEM ARCHITECTURE
====================================================================================================

OVERVIEW
----------------------------------------------------------------------------------------------------
JobBridge is a modern, full-stack job board platform built with Django 5 and Vanilla JavaScript. 
It connects Candidates with Employers through a seamless, responsive interface.

The backend is a monolithic Django application that serves both Server-Side Rendered (SSR) HTML 
and a REST API via Django REST Framework (DRF).


HIGH-LEVEL DIAGRAM
----------------------------------------------------------------------------------------------------
[ Client (Browser) ]
       |
       |-- HTML/CSS/JS (Vanilla) ---> [ Django Templates & Views ]
       |                                    |
       |-- Fetch / AJAX (JWT) ------> [ Django REST Framework (API) ]
                                            |
                                   [ PostgreSQL Database ]


CORE COMPONENTS
----------------------------------------------------------------------------------------------------
1. BACKEND (DJANGO)
The project is split into modular Django apps, each handling a specific domain:

* apps/accounts: Custom User model (email-based login), Profiles, JWT Auth.
* apps/candidates: Candidate profiles, Education, Experience, Skills, Saved Jobs.
* apps/employers / apps/companies: Company profiles, Employer dashboards.
* apps/jobs: Job postings, Categories, Search, Public Marketing pages.
* apps/applications: Tracking applications, Status updates (Shortlisted, Hired, etc.).
* apps/interviews: Interview scheduling for employers and candidates.
* apps/notifications: In-app notifications.
* apps/reviews: Company reviews by candidates.
* apps/admin_panel: A custom staff-only dashboard for platform administration.


2. FRONTEND ARCHITECTURE
We use a hybrid approach:

* Marketing & Auth Pages: Standard Django templates using a global base.html. Forms submit via AJAX 
  (fetch) to DRF endpoints to prevent page reloads and provide instant validation.

* Dashboards: Protected by LoginRequiredMixin and Role-based mixins. They use a separate 
  dashboard_base.html layout (Sidebar + Topbar).

* Styling: A custom design system using CSS Variables (variables.css). No heavy frameworks like 
  Bootstrap or Tailwind are used, ensuring lightweight, bespoke UI components.

* Interactivity: Vanilla JavaScript (static/js/) handles dropdowns, form validation, password strength 
  meters, and API calls.


3. AUTHENTICATION
* Session Auth: Used for the main HTML dashboard views (Django's default).
* JWT (JSON Web Tokens): Used for the API. The frontend stores the access and refresh tokens 
  in localStorage and sends them via the Authorization: Bearer <token> header.


DIRECTORY STRUCTURE
----------------------------------------------------------------------------------------------------
Refer to project_structure.txt for a complete tree. Key directories:

* backend/apps/: All Django applications.
* backend/config/: Project settings and root URLs.
* backend/static/: CSS, JS, and Images.
* backend/templates/: HTML files (base, includes, pages).