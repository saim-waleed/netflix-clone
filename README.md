# Netflix Clone

A functional clone of Netflix with an integrated chatbot built using Django, HTML, CSS, and JavaScript.

## Features

- User Authentication (Sign Up/Sign In)
- Browse Movies and TV Shows
- Responsive Design
- AI-powered Chatbot for Netflix-related queries
- Movie/Show Details and Trailers
- Search Functionality
- User Profile Management

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Project Structure

- `main/`: Main application for movie/show listings
- `accounts/`: User authentication and profile management
- `chatbot/`: AI-powered chatbot functionality
- `static/`: Static files (CSS, JavaScript, Images)
- `templates/`: HTML templates

## Technologies Used

- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite (default)
- Authentication: Django Authentication System
- Styling: Custom CSS + Bootstrap
- Icons: Font Awesome
# netflix-clone
