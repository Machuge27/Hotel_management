# Django Authentication Project

## Project Overview
This is a Django-based authentication application that allows users to:
- Sign up with username, email, and password
- Log in using either email or username
- Automatically log in after signup
- Access a protected home page

## Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd auth_project
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

## Key Features
- Custom user model using email as unique identifier
- Signup with automatic login
- Login with email or username
- Bootstrap-styled forms
- Protected home page

## Project Structure
- `accounts/`: Custom authentication app
  - `models.py`: Custom user model
  - `forms.py`: Custom signup and login forms
  - `views.py`: Authentication views
- `auth_project/`: Main project directory
  - `settings.py`: Project configurations
  - `urls.py`: Project-level URL routing

## Optional Enhancements
- Add password reset functionality
- Implement email verification
- Add more robust form validation