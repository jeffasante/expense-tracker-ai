#!/bin/bash

echo "Setting up AI-Powered Expense Tracker API..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python manage.py makemigrations users
python manage.py makemigrations expenses
python manage.py migrate

# Create superuser (optional)
echo "Creating superuser (optional)..."
python manage.py createsuperuser --noinput --email admin@example.com --username admin || true

# Run tests
echo "Running tests..."
python manage.py test

echo "Setup complete! Run 'python manage.py runserver' to start the development server."
echo "API documentation will be available at: http://localhost:8000/api/docs/"