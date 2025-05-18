# Library Management System

A web-based library management system built with Django.

## Setup Instructions

1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit http://127.0.0.1:8000/ in your web browser

## Project Structure

- `/core` - Main application code
- `/templates` - HTML templates
- `/static` - Static files (CSS, JS, images)
- `/media` - User uploaded files (book covers)

## Important Notes

1. Make sure you have Python 3.x installed
2. The project uses SQLite as the database
3. Book cover images are stored in the `/media` directory
4. Static files (CSS, JS) are in the `/static` directory

## Common Issues

1. If you see a "no such table" error:
   - Run the database migrations (step 3 above)

2. If book covers are not showing:
   - Make sure the `/media` directory exists
   - Upload new book covers through the admin interface

3. If static files are not loading:
   - Run `python manage.py collectstatic`

## Features

- User authentication (login/signup)
- Book browsing and search
- Shopping cart functionality
- Favorites system
- Responsive design 