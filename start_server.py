#!/usr/bin/env python3
"""
Cross-platform server startup script for Railway deployment
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    django.setup()
    
    # Check if we're on Railway (production)
    if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT'):
        # Use gunicorn for production
        try:
            import gunicorn.app.wsgiapp as wsgi
            port = os.environ.get('PORT', '8000')
            sys.argv = ['gunicorn', 'backend.wsgi:application', '--bind', f'0.0.0.0:{port}', '--workers', '3', '--timeout', '120']
            wsgi.run()
        except ImportError:
            # Fallback to Django dev server
            port = os.environ.get('PORT', '8000')
            sys.argv = ['manage.py', 'runserver', f'0.0.0.0:{port}']
            execute_from_command_line(sys.argv)
    else:
        # Use Django dev server for local development
        sys.argv = ['manage.py', 'runserver', '0.0.0.0:8000']
        execute_from_command_line(sys.argv)
