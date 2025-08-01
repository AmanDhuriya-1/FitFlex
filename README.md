# FitFlex
FitFlex – Fitness Trainer Management System A Django-based web application to manage clients, workout plans, and progress tracking for fitness trainers.
Key Features:

Client Management: Add, view, update, and delete clients with search functionality.

Workout Plans: Assign customized plans with duration and fitness goals.

Progress Tracking: Log weight, BMI, and notes over time for each client.

Admin Panel: Enhanced with list_display and search_fields for easy management.

UI: Responsive design using Bootstrap with reusable base templates.

Extras: Flash messages, search, and optional authentication for secure access.

Tech Stack: Django, SQLite, Bootstrap

A clean, fully functional CRUD-based Django project – ideal for fitness management systems, portfolio showcases, and interview preparation.

Setup

Steps to Run
python -m venv myenv

source myenv/bin/activate

Copy the downloaded project files and paste them next to the myenv folder

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py runserver 4467

Important Note:
Do NOT use the default port (8000).

Always run the server on port 4456 (or the one specified in settings), otherwise CSS and static files will not load properly.
