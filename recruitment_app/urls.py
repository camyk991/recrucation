from django.urls import path
from . import views

urlpatterns = [
    path('', views.candidates_list, name='candidates_list'),
    path('candidate/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('candidate/add/', views.add_candidate, name='add_candidate'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
