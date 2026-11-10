====================================================================================================
JOBBRIDGE — DEPLOYMENT GUIDE
====================================================================================================

This guide covers deploying JobBridge to production using Docker, Nginx, and Gunicorn.

ARCHITECTURE FOR PRODUCTION
----------------------------------------------------------------------------------------------------
* Web Server: Nginx (serves static files, reverse proxy).
* App Server: Gunicorn (runs Django).
* Database: PostgreSQL.
* Cache/Sessions: Redis.


1. DOCKER DEPLOYMENT (RECOMMENDED)
----------------------------------------------------------------------------------------------------
The project includes a docker-compose.yml file for easy deployment.

Setup:
1. Ensure Docker and Docker Compose are installed on your server.
2. Clone the repository to your server.
3. Update backend/.env with production values:
   - DJANGO_DEBUG=False
   - DJANGO_ALLOWED_HOSTS=yourdomain.com
   - DATABASE_URL=postgres://user:password@db:5432/jobbridge
   - REDIS_URL=redis://redis:6379/1

Build and Run:
docker-compose up -d --build

Run Migrations:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser


2. MANUAL DEPLOYMENT (UBUNTU/DEBIAN)
----------------------------------------------------------------------------------------------------
If not using Docker, follow these steps:

Install Packages:
sudo apt update
sudo apt install python3-pip python3-venv nginx postgresql redis-server

Set up the App:
1. Clone the code to /var/www/jobbridge.
2. Create a venv and install requirements: pip install -r requirements.txt.
3. Set DEBUG=False in .env.

Configure Gunicorn:
Create /etc/systemd/system/jobbridge.service:
[Unit]
Description=JobBridge Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/jobbridge/backend
ExecStart=/var/www/jobbridge/backend/.venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/jobbridge.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target

Start it: sudo systemctl start jobbridge

Configure Nginx:
Create /etc/nginx/sites-available/jobbridge:
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/jobbridge/backend;
    }

    location /media/ {
        root /var/www/jobbridge/backend;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/jobbridge.sock;
    }
}

Enable it: sudo ln -s /etc/nginx/sites-available/jobbridge /etc/nginx/sites-enabled/
Restart Nginx: sudo systemctl restart nginx


SECURITY CHECKLIST FOR PRODUCTION
----------------------------------------------------------------------------------------------------
[ ] Ensure DJANGO_DEBUG=False.
[ ] Use a strong, unique DJANGO_SECRET_KEY.
[ ] Enable HTTPS (Let's Encrypt / Certbot).
[ ] Ensure SECURE_SSL_REDIRECT = True.
[ ] Ensure SESSION_COOKIE_SECURE = True and CSRF_COOKIE_SECURE = True.
[ ] Configure regular database backups.