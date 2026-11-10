====================================================================================================
JOBBRIDGE — INSTALLATION GUIDE
====================================================================================================

Follow these steps to get JobBridge running on your local machine.

PREREQUISITES
----------------------------------------------------------------------------------------------------
* Python: Version 3.10 or higher.
* PostgreSQL: (Optional, but recommended for production). SQLite works out of the box for development.
* Node.js / npm: (Optional, only if modifying frontend assets, though this project uses pure CSS/JS).


STEP-BY-STEP SETUP
----------------------------------------------------------------------------------------------------

1. CLONE THE REPOSITORY
git clone https://github.com/yourusername/JobBridge.git
cd JobBridge/backend

2. CREATE A VIRTUAL ENVIRONMENT
Windows:
python -m venv .venv
.venv\Scripts\activate

macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

3. INSTALL DEPENDENCIES
pip install -r requirements.txt

4. CONFIGURE ENVIRONMENT VARIABLES
Copy the example env file:
cp .env.example .env

(Open .env and fill in your secret key, database URL, etc. If using SQLite, leave DATABASE_URL blank or remove it).

5. RUN MIGRATIONS
Initialize the database schema:
python manage.py migrate

6. CREATE A SUPERUSER
Create an admin account to access the Django admin panel:
python manage.py createsuperuser
(Enter your email and password when prompted).

7. COLLECT STATIC FILES (OPTIONAL FOR DEV)
python manage.py collectstatic

8. RUN THE SERVER
python manage.py runserver

The application is now running at http://127.0.0.1:8000.


TESTING THE APP
----------------------------------------------------------------------------------------------------
* Homepage: http://127.0.0.1:8000
* Admin Panel: http://127.0.0.1:8000/admin/
* Login: http://127.0.0.1:8000/accounts/login/