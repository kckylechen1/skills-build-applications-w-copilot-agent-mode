from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'teams', views.TeamViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'leaderboard', views.LeaderboardViewSet)
router.register(r'workouts', views.WorkoutViewSet)
router.register(r'user-workouts', views.UserWorkoutViewSet)

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('api/', views.api_root, name='api_root'),
    path('api/', include(router.urls)),
]