# Create a virtual environment (optional but recommended)
python -m venv myenv
# Activate the virtual environment
# On Windows
myenv\Scripts\activate
# On macOS/Linux
source myenv/bin/activate

# Install required packages
pip install django djangorestframework

# Create a new Django project
django-admin startproject notes_project

# Change to the project directory
cd notes_project

# Create a new app within the project
python manage.py startapp notes

# Replace the content of notes_project/settings.py with your own settings
# Update INSTALLED_APPS to include 'rest_framework' and 'notes'
# Update DATABASES if needed
# Set ALLOWED_HOSTS

# Create database tables
python manage.py migrate

# Create a superuser (follow the prompts)
python manage.py createsuperuser

# Create initial migrations for your 'notes' app
python manage.py makemigrations notes

# Apply the initial migrations
python manage.py migrate

# Create your serializers, models, and views in the 'notes' app
# Replace the content of notes/serializers.py, notes/models.py, and notes/views.py with your code

# Run the development server
python manage.py runserver

# For Tests
python manage.py test notes.tests
