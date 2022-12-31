"""
WSGI config for el_moadin_pi project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "el_moadin_pi.settings")

application = get_wsgi_application()

try:
    call_command('crontab', 'remove')
except Exception as e:
    print(e)

call_command('crontab', 'add')
call_command('crontab', 'show')
