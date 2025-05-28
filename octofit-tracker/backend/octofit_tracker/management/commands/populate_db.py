from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout, UserWorkout
from django.conf import settings
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId
import uuid

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections to start fresh
        self.stdout.write('Clearing existing data...')
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        db.user_workouts.drop()

        # Create users (Merington High School students)
        self.stdout.write('Creating users...')
        users_data = [
            {
                'username': 'thundergod',
                'email': 'thundergod@merington.edu',
                'first_name': 'Thor',
                'last_name': 'Odinson',
                'password': 'password123'
            },
            {
                'username': 'metalgeek',
                'email': 'metalgeek@merington.edu',
                'first_name': 'Tony',
                'last_name': 'Stark',
                'password': 'password123'
            },
            {
                'username': 'zerocool',
                'email': 'zerocool@merington.edu',
                'first_name': 'Dade',
                'last_name': 'Murphy',
                'password': 'password123'
            },
            {
                'username': 'crashoverride',
                'email': 'crashoverride@merington.edu',
                'first_name': 'Kate',
                'last_name': 'Libby',
                'password': 'password123'
            },
            {
                'username': 'sleeptoken',
                'email': 'sleeptoken@merington.edu',
                'first_name': 'Vessel',
                'last_name': 'Anonymous',
                'password': 'password123'
            },
            {
                'username': 'acidburn',
                'email': 'acidburn@merington.edu',
                'first_name': 'Acid',
                'last_name': 'Burn',
                'password': 'password123'
            }
        ]

        users = []
        for user_data in users_data:
            user = User(
                _id=ObjectId(),
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                date_joined=datetime.now()
            )
            users.append(user)
        
        User.objects.bulk_create(users)
        self.stdout.write(f'Created {len(users)} users')

        # Create teams
        self.stdout.write('Creating teams...')
        blue_team = Team(
            _id=ObjectId(),
            name='Blue Octopus',
            description='The mighty blue team of Merington High',
            created_by=users[0],
            created_at=datetime.now()
        )
        blue_team.save()
        blue_team.members.add(users[0], users[1], users[2])

        gold_team = Team(
            _id=ObjectId(),
            name='Gold Kraken',
            description='The legendary gold team of Merington High',
            created_by=users[3],
            created_at=datetime.now()
        )
        gold_team.save()
        gold_team.members.add(users[3], users[4], users[5])

        self.stdout.write('Created 2 teams')

        # Create activities
        self.stdout.write('Creating activities...')
        activities_data = [
            {
                'user': users[0],
                'activity_type': 'running',
                'duration_minutes': 60,
                'calories_burned': 500,
                'distance_km': 8.0,
                'notes': 'Great morning run around the school track'
            },
            {
                'user': users[1],
                'activity_type': 'cycling',
                'duration_minutes': 90,
                'calories_burned': 600,
                'distance_km': 25.0,
                'notes': 'Bike ride through the city park'
            },
            {
                'user': users[2],
                'activity_type': 'swimming',
                'duration_minutes': 45,
                'calories_burned': 400,
                'distance_km': 2.0,
                'notes': 'Pool training session'
            },
            {
                'user': users[3],
                'activity_type': 'strength_training',
                'duration_minutes': 75,
                'calories_burned': 350,
                'distance_km': 0.0,
                'notes': 'Weight lifting and resistance training'
            },
            {
                'user': users[4],
                'activity_type': 'yoga',
                'duration_minutes': 60,
                'calories_burned': 200,
                'distance_km': 0.0,
                'notes': 'Relaxing yoga session for flexibility'
            },
            {
                'user': users[5],
                'activity_type': 'basketball',
                'duration_minutes': 120,
                'calories_burned': 700,
                'distance_km': 0.0,
                'notes': 'Pickup game with friends'
            },
            {
                'user': users[0],
                'activity_type': 'hiking',
                'duration_minutes': 180,
                'calories_burned': 800,
                'distance_km': 12.0,
                'notes': 'Mountain trail hike'
            },
            {
                'user': users[1],
                'activity_type': 'tennis',
                'duration_minutes': 90,
                'calories_burned': 450,
                'distance_km': 0.0,
                'notes': 'Singles match practice'
            }
        ]

        activities = []
        for activity_data in activities_data:
            activity = Activity(
                _id=ObjectId(),
                activity_id=str(uuid.uuid4()),
                user=activity_data['user'],
                activity_type=activity_data['activity_type'],
                duration_minutes=activity_data['duration_minutes'],
                calories_burned=activity_data['calories_burned'],
                distance_km=activity_data['distance_km'],
                notes=activity_data['notes'],
                date_logged=datetime.now() - timedelta(days=len(activities))
            )
            activities.append(activity)
        
        Activity.objects.bulk_create(activities)
        self.stdout.write(f'Created {len(activities)} activities')

        # Create leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        leaderboard_data = [
            {
                'user': users[0],
                'team': blue_team,
                'total_points': 1250,
                'total_activities': 15,
                'total_calories': 8500,
                'total_distance': 45.0,
                'rank': 1
            },
            {
                'user': users[1],
                'team': blue_team,
                'total_points': 1100,
                'total_activities': 12,
                'total_calories': 7200,
                'total_distance': 38.0,
                'rank': 2
            },
            {
                'user': users[2],
                'team': blue_team,
                'total_points': 950,
                'total_activities': 10,
                'total_calories': 6000,
                'total_distance': 25.0,
                'rank': 5
            },
            {
                'user': users[3],
                'team': gold_team,
                'total_points': 1180,
                'total_activities': 14,
                'total_calories': 7800,
                'total_distance': 42.0,
                'rank': 3
            },
            {
                'user': users[4],
                'team': gold_team,
                'total_points': 1050,
                'total_activities': 11,
                'total_calories': 6800,
                'total_distance': 30.0,
                'rank': 4
            },
            {
                'user': users[5],
                'team': gold_team,
                'total_points': 890,
                'total_activities': 9,
                'total_calories': 5500,
                'total_distance': 20.0,
                'rank': 6
            }
        ]

        leaderboard_entries = []
        for lb_data in leaderboard_data:
            leaderboard = Leaderboard(
                _id=ObjectId(),
                leaderboard_id=str(uuid.uuid4()),
                user=lb_data['user'],
                team=lb_data['team'],
                total_points=lb_data['total_points'],
                total_activities=lb_data['total_activities'],
                total_calories=lb_data['total_calories'],
                total_distance=lb_data['total_distance'],
                rank=lb_data['rank'],
                last_updated=datetime.now()
            )
            leaderboard_entries.append(leaderboard)
        
        Leaderboard.objects.bulk_create(leaderboard_entries)
        self.stdout.write(f'Created {len(leaderboard_entries)} leaderboard entries')

        # Create workouts
        self.stdout.write('Creating workouts...')
        workouts_data = [
            {
                'name': 'Morning Cardio Blast',
                'description': 'High-intensity cardio workout to start your day',
                'difficulty_level': 'intermediate',
                'duration_minutes': 45,
                'calories_target': 400,
                'exercises': ['Jumping Jacks', 'Burpees', 'Mountain Climbers', 'High Knees', 'Plank'],
                'created_by': users[0],
                'is_public': True
            },
            {
                'name': 'Strength Builder',
                'description': 'Build muscle and strength with this comprehensive workout',
                'difficulty_level': 'advanced',
                'duration_minutes': 60,
                'calories_target': 500,
                'exercises': ['Squats', 'Deadlifts', 'Bench Press', 'Pull-ups', 'Overhead Press'],
                'created_by': users[1],
                'is_public': True
            },
            {
                'name': 'Beginner Friendly Flow',
                'description': 'Perfect workout for fitness beginners',
                'difficulty_level': 'beginner',
                'duration_minutes': 30,
                'calories_target': 200,
                'exercises': ['Wall Push-ups', 'Bodyweight Squats', 'Lunges', 'Planks', 'Stretching'],
                'created_by': users[2],
                'is_public': True
            },
            {
                'name': 'HIIT Thunder',
                'description': 'High-intensity interval training for maximum results',
                'difficulty_level': 'advanced',
                'duration_minutes': 30,
                'calories_target': 450,
                'exercises': ['Sprint Intervals', 'Burpees', 'Jump Squats', 'Push-up Variations', 'Core Blaster'],
                'created_by': users[3],
                'is_public': True
            },
            {
                'name': 'Flexibility & Recovery',
                'description': 'Gentle stretching and recovery workout',
                'difficulty_level': 'beginner',
                'duration_minutes': 25,
                'calories_target': 150,
                'exercises': ['Dynamic Stretching', 'Yoga Poses', 'Foam Rolling', 'Deep Breathing', 'Meditation'],
                'created_by': users[4],
                'is_public': True
            },
            {
                'name': 'Team Sports Prep',
                'description': 'Prepare for team sports with agility and coordination',
                'difficulty_level': 'intermediate',
                'duration_minutes': 50,
                'calories_target': 350,
                'exercises': ['Ladder Drills', 'Cone Weaving', 'Plyometric Jumps', 'Sport-specific Moves', 'Cool Down'],
                'created_by': users[5],
                'is_public': False
            }
        ]

        workouts = []
        for workout_data in workouts_data:
            workout = Workout(
                _id=ObjectId(),
                workout_id=str(uuid.uuid4()),
                name=workout_data['name'],
                description=workout_data['description'],
                difficulty_level=workout_data['difficulty_level'],
                duration_minutes=workout_data['duration_minutes'],
                calories_target=workout_data['calories_target'],
                exercises=workout_data['exercises'],
                created_by=workout_data['created_by'],
                is_public=workout_data['is_public'],
                created_at=datetime.now() - timedelta(days=len(workouts))
            )
            workouts.append(workout)
        
        Workout.objects.bulk_create(workouts)
        self.stdout.write(f'Created {len(workouts)} workouts')

        # Create user workout completions
        self.stdout.write('Creating user workout completions...')
        user_workouts_data = [
            {
                'user': users[0],
                'workout': workouts[0],
                'actual_duration': 42,
                'calories_burned': 380,
                'rating': 5,
                'notes': 'Excellent workout! Felt energized all day.'
            },
            {
                'user': users[1],
                'workout': workouts[1],
                'actual_duration': 65,
                'calories_burned': 450,
                'rating': 4,
                'notes': 'Challenging but rewarding strength session.'
            },
            {
                'user': users[2],
                'workout': workouts[2],
                'actual_duration': 28,
                'calories_burned': 150,
                'rating': 5,
                'notes': 'Perfect for my fitness level!'
            },
            {
                'user': users[3],
                'workout': workouts[3],
                'actual_duration': 32,
                'calories_burned': 420,
                'rating': 5,
                'notes': 'Intense HIIT session, loved every minute!'
            },
            {
                'user': users[4],
                'workout': workouts[4],
                'actual_duration': 30,
                'calories_burned': 120,
                'rating': 4,
                'notes': 'Very relaxing and helped with recovery.'
            },
            {
                'user': users[0],
                'workout': workouts[1],
                'actual_duration': 58,
                'calories_burned': 425,
                'rating': 4,
                'notes': 'Great strength workout, will do again.'
            }
        ]

        user_workouts = []
        for uw_data in user_workouts_data:
            user_workout = UserWorkout(
                _id=ObjectId(),
                user=uw_data['user'],
                workout=uw_data['workout'],
                completed_at=datetime.now() - timedelta(days=len(user_workouts)),
                actual_duration=uw_data['actual_duration'],
                calories_burned=uw_data['calories_burned'],
                rating=uw_data['rating'],
                notes=uw_data['notes']
            )
            user_workouts.append(user_workout)
        
        UserWorkout.objects.bulk_create(user_workouts)
        self.stdout.write(f'Created {len(user_workouts)} user workout completions')

        self.stdout.write(self.style.SUCCESS('Successfully populated the OctoFit database with test data!'))
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(f'  - {len(users)} users created')
        self.stdout.write(f'  - 2 teams created')
        self.stdout.write(f'  - {len(activities)} activities created')
        self.stdout.write(f'  - {len(leaderboard_entries)} leaderboard entries created')
        self.stdout.write(f'  - {len(workouts)} workouts created')
        self.stdout.write(f'  - {len(user_workouts)} user workout completions created')