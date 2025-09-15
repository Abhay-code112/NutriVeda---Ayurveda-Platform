#!/usr/bin/env python
"""
Windows-compatible server startup script
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()
    
    # Check if we're on Railway (production)
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        # Use gunicorn for production
        try:
            import gunicorn.app.wsgiapp as wsgi
            sys.argv = ['gunicorn', 'backend.wsgi:application', '--bind', f'0.0.0.0:{os.environ.get("PORT", "8000")}', '--workers', '3']
            wsgi.run()
        except ImportError:
            # Fallback to Django dev server
            sys.argv = ['manage.py', 'runserver', f'0.0.0.0:{os.environ.get("PORT", "8000")}']
            execute_from_command_line(sys.argv)
    else:
        # Use Django dev server for local development
        sys.argv = ['manage.py', 'runserver', '0.0.0.0:8000']
        execute_from_command_line(sys.argv)
