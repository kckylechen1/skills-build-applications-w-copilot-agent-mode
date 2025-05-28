from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User, Team, Activity, Leaderboard, Workout, UserWorkout
import uuid
from datetime import datetime, date

class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            grade_level='10',
            fitness_level='intermediate'
        )
    
    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.grade_level, '10')
        self.assertEqual(self.user.fitness_level, 'intermediate')
    
    def test_user_str_method(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'testuser')

class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='creator',
            email='creator@example.com'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            created_by=self.user
        )
    
    def test_team_creation(self):
        """Test team creation"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.description, 'A test team')
        self.assertEqual(self.team.created_by, self.user)
    
    def test_team_str_method(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')

class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='athlete',
            email='athlete@example.com'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration_minutes=30,
            calories_burned=300,
            distance_km=5.0,
            notes='Great run!'
        )
    
    def test_activity_creation(self):
        """Test activity creation"""
        self.assertEqual(self.activity.user, self.user)
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration_minutes, 30)
        self.assertEqual(self.activity.calories_burned, 300)
        self.assertEqual(self.activity.distance_km, 5.0)
        self.assertIsNotNone(self.activity.activity_id)
    
    def test_activity_str_method(self):
        """Test activity string representation"""
        expected = f'{self.user.username} - running'
        self.assertEqual(str(self.activity), expected)

class LeaderboardModelTest(TestCase):
    """Test cases for Leaderboard model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='competitor',
            email='competitor@example.com'
        )
        self.team = Team.objects.create(
            name='Competitors',
            created_by=self.user
        )
        self.leaderboard = Leaderboard.objects.create(
            user=self.user,
            team=self.team,
            total_points=100,
            activities_completed=5,
            total_calories_burned=1500
        )
    
    def test_leaderboard_creation(self):
        """Test leaderboard creation"""
        self.assertEqual(self.leaderboard.user, self.user)
        self.assertEqual(self.leaderboard.team, self.team)
        self.assertEqual(self.leaderboard.total_points, 100)
        self.assertEqual(self.leaderboard.activities_completed, 5)
        self.assertIsNotNone(self.leaderboard.leaderboard_id)

class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='trainer',
            email='trainer@example.com'
        )
        self.workout = Workout.objects.create(
            name='Morning Cardio',
            description='A great morning workout',
            difficulty_level='intermediate',
            estimated_duration=45,
            exercises=['Push-ups', 'Squats', 'Jumping Jacks'],
            created_by=self.user,
            is_public=True
        )
    
    def test_workout_creation(self):
        """Test workout creation"""
        self.assertEqual(self.workout.name, 'Morning Cardio')
        self.assertEqual(self.workout.difficulty_level, 'intermediate')
        self.assertEqual(self.workout.estimated_duration, 45)
        self.assertTrue(self.workout.is_public)
        self.assertIsNotNone(self.workout.workout_id)

class UserWorkoutModelTest(TestCase):
    """Test cases for UserWorkout model"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='exerciser',
            email='exerciser@example.com'
        )
        self.workout = Workout.objects.create(
            name='Test Workout',
            created_by=self.user
        )
        self.user_workout = UserWorkout.objects.create(
            user=self.user,
            workout=self.workout,
            completed_at=datetime.now(),
            duration_minutes=30,
            calories_burned=250,
            rating=4,
            notes='Good workout!'
        )
    
    def test_user_workout_creation(self):
        """Test user workout creation"""
        self.assertEqual(self.user_workout.user, self.user)
        self.assertEqual(self.user_workout.workout, self.workout)
        self.assertEqual(self.user_workout.duration_minutes, 30)
        self.assertEqual(self.user_workout.rating, 4)

class APITestCase(APITestCase):
    """Test cases for API endpoints"""
    
    def setUp(self):
        self.user = User.objects.create(
            username='apiuser',
            email='api@example.com'
        )
        self.team = Team.objects.create(
            name='API Team',
            created_by=self.user
        )
    
    def test_api_root(self):
        """Test API root endpoint"""
        url = reverse('api_root')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
    
    def test_user_list(self):
        """Test user list endpoint"""
        url = '/api/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_team_list(self):
        """Test team list endpoint"""
        url = '/api/teams/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_activity_list(self):
        """Test activity list endpoint"""
        url = '/api/activities/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_leaderboard_list(self):
        """Test leaderboard list endpoint"""
        url = '/api/leaderboard/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_workout_list(self):
        """Test workout list endpoint"""
        url = '/api/workouts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_workout_list(self):
        """Test user workout list endpoint"""
        url = '/api/user-workouts/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_user(self):
        """Test creating a new user"""
        url = '/api/users/'
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'grade_level': '11',
            'fitness_level': 'beginner'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_team(self):
        """Test creating a new team"""
        url = '/api/teams/'
        data = {
            'name': 'New Team',
            'description': 'A brand new team'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_activity(self):
        """Test creating a new activity"""
        url = '/api/activities/'
        data = {
            'activity_type': 'cycling',
            'duration_minutes': 60,
            'calories_burned': 400,
            'distance_km': 15.0,
            'notes': 'Great bike ride!'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_workout(self):
        """Test creating a new workout"""
        url = '/api/workouts/'
        data = {
            'name': 'Evening Strength',
            'description': 'Strength training workout',
            'difficulty_level': 'advanced',
            'estimated_duration': 60,
            'exercises': ['Deadlifts', 'Bench Press', 'Squats'],
            'is_public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
