from djongo import models
from django.contrib.auth.models import AbstractUser
from django.db import models as django_models

class User(models.Model):
    _id = models.ObjectIdField()
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'users'

class Team(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teams'

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('walking', 'Walking'),
        ('weightlifting', 'Weight Lifting'),
        ('yoga', 'Yoga'),
        ('other', 'Other'),
    ]
    
    _id = models.ObjectIdField()
    activity_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    duration_minutes = models.IntegerField()
    calories_burned = models.IntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)
    date_logged = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activity'
        ordering = ['-date_logged']

class Leaderboard(models.Model):
    _id = models.ObjectIdField()
    leaderboard_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    total_points = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    total_calories = models.IntegerField(default=0)
    total_distance = models.FloatField(default=0.0)
    rank = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leaderboard'
        ordering = ['-total_points']

class Workout(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    _id = models.ObjectIdField()
    workout_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration_minutes = models.IntegerField()
    calories_target = models.IntegerField()
    exercises = models.JSONField(default=list)  # List of exercises with reps/sets
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_workouts')
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'workouts'
        ordering = ['-created_at']

class UserWorkout(models.Model):
    """Track user's completed workouts"""
    _id = models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_workouts')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    actual_duration = models.IntegerField()  # Actual time taken
    calories_burned = models.IntegerField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)  # 1-5 stars
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'user_workouts'
        ordering = ['-completed_at']
