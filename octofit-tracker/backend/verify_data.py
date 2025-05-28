#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit.settings')
django.setup()

from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout, UserWorkout

print("=== OctoFit Database Verification ===")
print(f"Users: {User.objects.count()}")
print(f"Teams: {Team.objects.count()}")
print(f"Activities: {Activity.objects.count()}")
print(f"Leaderboard entries: {Leaderboard.objects.count()}")
print(f"Workouts: {Workout.objects.count()}")
print(f"User workout completions: {UserWorkout.objects.count()}")

print("\n=== Sample Data ===")
print("\nUsers:")
for user in User.objects.all()[:3]:
    print(f"  - {user.username} ({user.first_name} {user.last_name})")

print("\nTeams:")
for team in Team.objects.all():
    print(f"  - {team.name}: {team.members.count()} members")

print("\nRecent Activities:")
for activity in Activity.objects.all()[:3]:
    print(f"  - {activity.user.username}: {activity.activity_type} ({activity.duration_minutes} min)")

print("\nTop Leaderboard:")
for entry in Leaderboard.objects.order_by('-total_points')[:3]:
    print(f"  - {entry.user.username}: {entry.total_points} points")

print("\nWorkouts:")
for workout in Workout.objects.all()[:3]:
    print(f"  - {workout.name} ({workout.difficulty_level})")

print("\n=== Verification Complete ===")