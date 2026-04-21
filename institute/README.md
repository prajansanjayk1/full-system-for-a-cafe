# Tuition Institute Django Website

Production-ready Django project for a tuition/coaching institute with full admin CMS control.

## Features
- Multi-app architecture: `core`, `courses`, `subjects`, `results`, `testimonials`, `blog`, `contact`, `registration`
- Full Django admin management for all content
- Responsive modern UI with Tailwind CSS (CDN setup)
- Registration form that saves to DB and sends email notification
- Contact form that saves to DB
- SEO-ready slug URLs, meta fields, heading hierarchy, alt text, internal links
- SQLite by default, PostgreSQL-ready settings structure

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Email (Gmail SMTP Example)
Set environment variables:

```bash
export EMAIL_HOST="smtp.gmail.com"
export EMAIL_PORT="587"
export EMAIL_HOST_USER="yourgmail@gmail.com"
export EMAIL_HOST_PASSWORD="your-app-password"
export EMAIL_USE_TLS="True"
export DEFAULT_FROM_EMAIL="yourgmail@gmail.com"
export ADMIN_NOTIFICATION_EMAIL="prajansanjayk@gmail.com"
```

When the registration form is submitted, an email with all student details is sent to `ADMIN_NOTIFICATION_EMAIL`.

## Media
- `MEDIA_URL = /media/`
- `MEDIA_ROOT = BASE_DIR / 'media'`

Upload images for courses, subjects, and blog posts directly from Django admin.

## Apps Overview
- **core**: Home, About, global Site Settings
- **courses**: Course list/detail pages
- **subjects**: Subject list/detail pages
- **results**: Academic improvement showcase
- **testimonials**: Parent/student trust signals
- **blog**: SEO blog listing and detail
- **contact**: Contact form + admin submissions
- **registration**: Demo booking + email notifications
