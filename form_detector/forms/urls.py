from django.urls import path

from .views import get_form

urlpatterns = [
    path('get_form/', get_form, name='get_form'),
]
