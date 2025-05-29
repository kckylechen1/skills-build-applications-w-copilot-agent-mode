from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(models.Model):
    id = models.AutoField(primary_key=True)
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
    id = models.AutoField(primary_key=True)
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
    
    id = models.AutoField(primary_key=True)
    activity_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
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
    id = models.AutoField(primary_key=True)
    leaderboard_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
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
    
    id = models.AutoField(primary_key=True)
    workout_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
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
    id = models.AutoField(primary_key=True)
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
