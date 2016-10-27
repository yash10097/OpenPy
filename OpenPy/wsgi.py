"""      Please refer to the license file for complete details. 
  *      Project: OpenPy
  *      Developer: Yash Lamba
  *      Institute: Indraprastha Institute of Information Technology, Delhi
  *      Advisor: Pandarasamy Arjunan, Dr. Pushpendra Singh
"""

"""
WSGI config for open project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OpenPy.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
