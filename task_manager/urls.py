from django.http import HttpResponse
from django.urls import path
from django.contrib import admin


def index(request):
    return HttpResponse("Hello from Task Manager!")


urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
]
