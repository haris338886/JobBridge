====================================================================================================
JOBBRIDGE — DATABASE DESIGN
====================================================================================================

OVERVIEW
----------------------------------------------------------------------------------------------------
The database is managed via Django's ORM. It is designed to be relational (PostgreSQL recommended for 
production, SQLite for local development).


CORE ENTITIES
----------------------------------------------------------------------------------------------------

1. USER (accounts.User)
Replaces Django's default user model.

* Fields: email (unique, primary identifier), password, first_name, last_name, role 
  (candidate, employer, admin), is_verified.
* Relationships:
  - OneToOne with Profile (Avatar, bio, location).
  - OneToOne with Candidate (if role is candidate).
  - OneToMany with Company (if role is employer).


2. COMPANY (companies.Company)

* Fields: name, slug, description, website, industry, size, logo.
* Relationships:
  - ForeignKey to User (Owner/Employer).
  - OneToMany with Job.


3. JOB (jobs.Job)

* Fields: title, slug, description, requirements, location, is_remote, salary_min, salary_max, 
  job_type, status.
* Relationships:
  - ForeignKey to Company.
  - ForeignKey to JobCategory.
  - OneToMany with Application.


4. CANDIDATE (candidates.Candidate)

* Fields: headline, summary, phone, location, resume, linkedin, portfolio.
* Relationships:
  - OneToOne to User.
  - OneToMany with Education, Experience, Skill, SavedJob, Application.


5. APPLICATION (applications.Application)

* Fields: cover_letter, resume, status (applied, reviewing, shortlisted, rejected, hired).
* Relationships:
  - ForeignKey to Job.
  - ForeignKey to Candidate.
  - Unique Together: A candidate can only apply once per job (job, candidate).


6. INTERVIEW (interviews.Interview)

* Fields: scheduled_at, duration_minutes, interview_type (video, phone, in-person), meeting_link, 
  notes, status.
* Relationships:
  - ForeignKey to Application.


INDEXING & PERFORMANCE
----------------------------------------------------------------------------------------------------
* User.email is indexed (used for login).
* Job.slug is indexed (used for SEO URLs).
* Application has a unique constraint on (job, candidate) to prevent duplicate applications.
* Jobs are indexed by (status, -created_at) for fast listing.