from django.urls import path
from . import views

urlpatterns = [
    path('api/reporters/', views.reporters_view, name='reporters'),
    path('api/issues/', views.issues_view, name='issues'),
]
