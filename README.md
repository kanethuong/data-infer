# Data Inference - Rhombus
## Overview
This project is part of the assessment for the Full Stack Software Engineering role at Rhombus AI. It demonstrates a web application that allows users to upload CSV or Excel files and infers the data types of each column.

## Table of Contents
1. [Setup Instructions](#setup-instructions)
2. [Running the Application](#running-the-application)
3. [Additional Notes](#additional-notes)
4. [Technologies Used](#technologies-used)

## Setup Instructions
### Prerequisites
Ensure you have the following installed on your system:

- [Python](https://www.python.org/downloads/)
- [Node.js](https://nodejs.org/en/download/prebuilt-installer/current)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Django](https://www.djangoproject.com/download/)
- [React](https://react.dev/)

## Backend Setup
1. Clone the repository:
```
git clone https://github.com/kanethuong/data-infer.git
cd data-infer
```

2. Create and activate a virtual environment:
```
python -m venv env
source env/bin/activate   # On Windows use `env\Scripts\activate`
```

3. Install backend dependencies:
```
pip install -r requirements.txt
```

4. Configure PostgreSQL database:
- Create a PostgreSQL database named your_database_name.
- Update the database configuration in backend/backend/settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
5. Run database migrations:
```
cd .\backend\
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```
python manage.py createsuperuser
```

7. Start the Django development server:
```
python manage.py runserver
```
## Frontend Setup
1. Navigate to the frontend directory:
```
cd frontend
```
2. Install frontend dependencies:
```
npm install
```
3. Start the React development server:
```
npm start
```
The frontend server should now be running at http://localhost:3000 and the backend server at http://localhost:8000.
## Running the Application
1. Upload a File:
- Navigate to http://localhost:3000.
- Drag and drop a CSV or Excel file into the designated area or click "Browse" to select a file from your computer.
- Click "Upload" to process the file.

2. View Inferred Data Types:
- Once the file is processed, the inferred data types for each column will be displayed on the screen.

## Additional Notes
- Ensure that your CSV or Excel files are well-formatted and contain consistent data types within each column to achieve the best inference results.
- The application currently supports the following data types: Text, Integer, Float, Boolean, Date, Time Delta, Category, and Complex.
## Technologies Used
- Backend:
  - Django
  - Django REST Framework
  - PostgreSQL

- Frontend:
  - React
  - Axios
