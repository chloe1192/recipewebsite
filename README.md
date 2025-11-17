# Recipe Sharing Platform

A Django web application for managing and sharing cooking recipes.

⚠️ **Work in Progress** — This project is under active development and not yet complete.

## Tech Stack

- Python 3.11+ / Django 5.x
- MySQL database
- Bootstrap 5 for UI
- SCSS with django-compressor
- Pillow for image processing

## Features

- User authentication and profiles
- Recipe CRUD with image uploads
- Category browsing and search
- Internationalization support (Unicode names)
- Responsive design

## Quick Setup

```bash
# Clone repository
git clone https://github.com/chloe1192/recipewebsite.git
cd recipewebsite

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Edit with your settings

# Setup database
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Environment Variables

Create a `.env` file with:

```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=recipewebsite
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

## Project Structure

```
recipewebsite/
├── models.py          # Database models
├── views.py           # Request handlers
├── forms.py           # Form validation
├── templates/         # HTML templates
└── static/            # CSS/JS/images
```

## Development Status

Current implementation includes basic recipe sharing functionality. Planned improvements:

- Complete test coverage
- Enhanced search filters
- Rating system
- Recipe collections
- API endpoints

## Notes

This is a learning project showcasing Django development practices. Feedback and suggestions are welcome.
