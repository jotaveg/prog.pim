from django.urls import path

from .views import DashboardView, LandingView, ProfileView, ProjectDetailView, ProjectListView

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('projects/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('profile/', ProfileView.as_view(), name='profile'),
]