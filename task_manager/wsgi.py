"""
WSGI config for task_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'index.html'