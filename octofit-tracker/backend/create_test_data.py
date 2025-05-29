#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit.settings')
django.setup()

from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
import uuid
from datetime import datetime

def create_test_data():
    print('Creating OctoFit Tracker test data for Mergington High School...')
    
    # Create PE teacher Paul Octo
    print('Creating PE teacher and students...')
    paul_octo = User.objects.create(
        username='paul_octo',
        email='paul.octo@mergington.edu',
        first_name='Paul',
        last_name='Octo',
        password='teacher_password'
    )
    
    # Create Mergington High School students with engaging usernames
    student_data = [
        {'username': 'thundergod', 'email': 'thundergod@mergington.edu', 'first_name': 'Alex', 'last_name': 'Thunder'},
        {'username': 'metalgeek', 'email': 'metalgeek@mergington.edu', 'first_name': 'Sam', 'last_name': 'Steel'},
        {'username': 'zerocool', 'email': 'zerocool@mergington.edu', 'first_name': 'Jordan', 'last_name': 'Zero'},
        {'username': 'crashoverride', 'email': 'crashoverride@mergington.edu', 'first_name': 'Casey', 'last_name': 'Override'},
        {'username': 'sleeptoken', 'email': 'sleeptoken@mergington.edu', 'first_name': 'Riley', 'last_name': 'Token'},
        {'username': 'phoenixrising', 'email': 'phoenixrising@mergington.edu', 'first_name': 'Phoenix', 'last_name': 'Rising'},
        {'username': 'stormchaser', 'email': 'stormchaser@mergington.edu', 'first_name': 'Storm', 'last_name': 'Chase'},
        {'username': 'nightwolf', 'email': 'nightwolf@mergington.edu', 'first_name': 'Luna', 'last_name': 'Wolf'}
    ]
    
    students = []
    for data in student_data:
        student = User.objects.create(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password='student_password'
        )
        students.append(student)
    
    # Create competitive teams for monthly challenges
    print('Creating competitive teams...')
    teams_data = [
        {'name': 'Lightning Bolts', 'description': 'Fast and fierce - we strike like lightning in every challenge!'},
        {'name': 'Iron Warriors', 'description': 'Strong and determined - forged through dedication and teamwork!'},
        {'name': 'Storm Runners', 'description': 'Unstoppable force - we run through any storm to victory!'}
    ]
    
    teams = []
    for i, team_data in enumerate(teams_data):
        team = Team.objects.create(
            name=team_data['name'],
            description=team_data['description'],
            created_by=paul_octo
        )
        # Distribute students across teams
        team_students = students[i*3:(i+1)*3] if i < 2 else students[6:]
        for student in team_students:
            team.members.add(student)
        teams.append(team)
    
    # Create diverse activity logs showing different fitness interests
    print('Creating activity logs...')
    activities_data = [
        {'user': students[0], 'type': 'running', 'duration': 45, 'calories': 350, 'distance': 5.2, 'notes': 'Morning jog around the school track - feeling great!'},
        {'user': students[1], 'type': 'weightlifting', 'duration': 60, 'calories': 280, 'notes': 'Strength training session - new personal record on bench press!'},
        {'user': students[2], 'type': 'cycling', 'duration': 90, 'calories': 520, 'distance': 15.8, 'notes': 'Bike ride to the park and back - beautiful weather today'},
        {'user': students[3], 'type': 'swimming', 'duration': 30, 'calories': 240, 'distance': 1.2, 'notes': 'Pool workout - working on freestyle technique'},
        {'user': students[4], 'type': 'yoga', 'duration': 45, 'calories': 150, 'notes': 'Relaxing yoga session - great for flexibility and mindfulness'},
        {'user': students[5], 'type': 'running', 'duration': 35, 'calories': 280, 'distance': 4.1, 'notes': 'Quick run before homework - helps me focus better'},
        {'user': students[6], 'type': 'walking', 'duration': 60, 'calories': 200, 'distance': 4.5, 'notes': 'Nature walk with friends - counted as cardio!'},
        {'user': students[7], 'type': 'other', 'duration': 75, 'calories': 320, 'notes': 'Basketball practice - working on three-point shots'}
    ]
    
    activities = []
    for activity_data in activities_data:
        activity = Activity.objects.create(
            user=activity_data['user'],
            activity_type=activity_data['type'],
            duration_minutes=activity_data['duration'],
            calories_burned=activity_data['calories'],
            distance_km=activity_data.get('distance'),
            notes=activity_data['notes']
        )
        activities.append(activity)
    
    # Create leaderboard entries reflecting competitive spirit
    print('Creating leaderboard entries...')
    leaderboard_data = [
        {'user': students[0], 'team': teams[0], 'points': 285, 'activities': 8},  # thundergod - top performer
        {'user': students[2], 'team': teams[0], 'points': 270, 'activities': 7},  # zerocool - close second
        {'user': students[1], 'team': teams[1], 'points': 255, 'activities': 6},  # metalgeek - consistent
        {'user': students[4], 'team': teams[1], 'points': 240, 'activities': 9},  # sleeptoken - many activities
        {'user': students[3], 'team': teams[1], 'points': 225, 'activities': 5},  # crashoverride - quality over quantity
        {'user': students[6], 'team': teams[2], 'points': 210, 'activities': 7},  # stormchaser - steady progress
        {'user': students[5], 'team': teams[2], 'points': 195, 'activities': 6},  # phoenixrising - rising up
        {'user': students[7], 'team': teams[2], 'points': 180, 'activities': 4}   # nightwolf - getting started
    ]
    
    leaderboard = []
    for entry_data in leaderboard_data:
        entry = Leaderboard.objects.create(
            user=entry_data['user'],
            team=entry_data['team'],
            total_points=entry_data['points'],
            total_activities=entry_data['activities']
        )
        leaderboard.append(entry)
    
    # Create personalized workout suggestions
    print('Creating personalized workout suggestions...')
    workouts_data = [
        {
            'name': 'Beginner Cardio Blast', 
            'description': 'Perfect for students just starting their fitness journey. 20-minute mix of walking, light jogging, and basic exercises.', 
            'difficulty': 'beginner', 
            'duration': 20, 
            'calories_target': 150,
            'exercises': [{'name': 'Walking', 'duration': '5 min'}, {'name': 'Light Jogging', 'duration': '10 min'}, {'name': 'Jumping Jacks', 'reps': '20'}]
        },
        {
            'name': 'Strength Builder Challenge', 
            'description': 'Build muscle and confidence with bodyweight exercises. Push-ups, squats, and planks progression.', 
            'difficulty': 'intermediate', 
            'duration': 30, 
            'calories_target': 200,
            'exercises': [{'name': 'Push-ups', 'sets': '3', 'reps': '10-15'}, {'name': 'Squats', 'sets': '3', 'reps': '15-20'}, {'name': 'Plank', 'duration': '30-60 sec'}]
        },
        {
            'name': 'Endurance Runner Program', 
            'description': 'For students ready to push their limits. Interval training and distance building for serious runners.', 
            'difficulty': 'advanced', 
            'duration': 45, 
            'calories_target': 400,
            'exercises': [{'name': 'Warm-up Jog', 'duration': '10 min'}, {'name': 'Sprint Intervals', 'sets': '8', 'duration': '30 sec on, 90 sec rest'}, {'name': 'Cool-down Walk', 'duration': '10 min'}]
        },
        {
            'name': 'Flexibility & Mindfulness', 
            'description': 'Yoga-inspired routine focusing on flexibility, balance, and mental wellness. Great for recovery days.', 
            'difficulty': 'beginner', 
            'duration': 25, 
            'calories_target': 100,
            'exercises': [{'name': 'Sun Salutation', 'reps': '5'}, {'name': 'Warrior Poses', 'duration': '2 min each'}, {'name': 'Meditation', 'duration': '5 min'}]
        },
        {
            'name': 'Team Sports Prep', 
            'description': 'Dynamic warm-up and conditioning exercises perfect for basketball, soccer, and other team sports.', 
            'difficulty': 'intermediate', 
            'duration': 35, 
            'calories_target': 250,
            'exercises': [{'name': 'Dynamic Stretching', 'duration': '10 min'}, {'name': 'Agility Ladder', 'sets': '3'}, {'name': 'Plyometric Jumps', 'sets': '3', 'reps': '10'}]
        }
    ]
    
    workouts = []
    for workout_data in workouts_data:
        workout = Workout.objects.create(
            name=workout_data['name'],
            description=workout_data['description'],
            difficulty_level=workout_data['difficulty'],
            duration_minutes=workout_data['duration'],
            calories_target=workout_data['calories_target'],
            exercises=workout_data['exercises'],
            created_by=paul_octo
        )
        workouts.append(workout)
    
    print(f'\n🎉 Successfully created OctoFit Tracker test data:')
    print(f'  - 1 PE teacher (Paul Octo)')
    print(f'  - {len(students)} Mergington High School students')
    print(f'  - {len(teams)} competitive teams')
    print(f'  - {len(activities)} diverse activity logs')
    print(f'  - {len(leaderboard)} leaderboard entries')
    print(f'  - {len(workouts)} personalized workout suggestions')
    print(f'\n🏫 Ready for Paul Octo\'s PE classes at Mergington High School!')

if __name__ == '__main__':
    create_test_data()