from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg
from django.shortcuts import get_object_or_404
from .models import User, Team, Activity, Leaderboard, Workout, UserWorkout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer, UserWorkoutSerializer,
    ActivitySummarySerializer, TeamStatsSerializer
)

@api_view(['GET'])
def api_root(request):
    """API root endpoint"""
    # Get codespace name from environment or use placeholder
    import os
    codespace_name = os.environ.get('CODESPACE_NAME', '[REPLACE-THIS-WITH-YOUR-CODESPACE-NAME]')
    
    return Response({
        'message': 'Welcome to OctoFit Tracker API',
        'version': '1.0',
        'codespace_url': f'https://{codespace_name}-8000.app.github.dev',
        'codespace_name': codespace_name,
        'codespace_name_instructions': 'You can get the codespace name by running the following command in the terminal: echo $CODESPACE_NAME',
        'local_url': 'http://localhost:8000',
        'endpoints': {
            'users': '/api/users/',
            'teams': '/api/teams/',
            'activities': '/api/activities/',
            'leaderboard': '/api/leaderboard/',
            'workouts': '/api/workouts/',
            'user-workouts': '/api/user-workouts/',
        }
    })

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for managing users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user=user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get activity statistics for a user"""
        user = self.get_object()
        activities = Activity.objects.filter(user=user)
        
        stats = activities.aggregate(
            total_activities=Count('_id'),
            total_calories=Sum('calories_burned') or 0,
            total_distance=Sum('distance_km') or 0.0,
            total_duration=Sum('duration_minutes') or 0
        )
        
        # Get favorite activity type
        favorite_activity = activities.values('activity_type').annotate(
            count=Count('activity_type')
        ).order_by('-count').first()
        
        stats['favorite_activity'] = favorite_activity['activity_type'] if favorite_activity else 'None'
        
        serializer = ActivitySummarySerializer(stats)
        return Response(serializer.data)

class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for managing teams"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Set the creator as the current user (for now, using first user)
        # In a real app, this would be request.user
        creator = User.objects.first()
        serializer.save(created_by=creator)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(_id=user_id)
            team.members.add(user)
            return Response({'message': f'{user.username} joined {team.name}'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(_id=user_id)
            team.members.remove(user)
            return Response({'message': f'{user.username} left {team.name}'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get team statistics"""
        team = self.get_object()
        members = team.members.all()
        
        total_activities = Activity.objects.filter(user__in=members).count()
        total_calories = Activity.objects.filter(user__in=members).aggregate(
            total=Sum('calories_burned')
        )['total'] or 0
        
        stats = {
            'team_name': team.name,
            'total_members': members.count(),
            'total_activities': total_activities,
            'total_calories': total_calories,
            'average_calories_per_member': total_calories / members.count() if members.count() > 0 else 0
        }
        
        serializer = TeamStatsSerializer(stats)
        return Response(serializer.data)

class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for managing activities"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Set the user (for now, using first user)
        # In a real app, this would be request.user
        user = User.objects.first()
        serializer.save(user=user)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get activities grouped by type"""
        activity_type = request.query_params.get('type')
        if activity_type:
            activities = Activity.objects.filter(activity_type=activity_type)
        else:
            activities = Activity.objects.all()
        
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

class LeaderboardViewSet(viewsets.ModelViewSet):
    """ViewSet for managing leaderboard"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def top_users(self, request):
        """Get top users by points"""
        limit = int(request.query_params.get('limit', 10))
        top_users = Leaderboard.objects.order_by('-total_points')[:limit]
        serializer = self.get_serializer(top_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_team(self, request):
        """Get leaderboard filtered by team"""
        team_id = request.query_params.get('team_id')
        if team_id:
            leaderboard = Leaderboard.objects.filter(team___id=team_id)
        else:
            leaderboard = Leaderboard.objects.all()
        
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)

class WorkoutViewSet(viewsets.ModelViewSet):
    """ViewSet for managing workouts"""
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Set the creator (for now, using first user)
        # In a real app, this would be request.user
        creator = User.objects.first()
        serializer.save(created_by=creator)

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts filtered by difficulty"""
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            workouts = Workout.objects.filter(difficulty_level=difficulty)
        else:
            workouts = Workout.objects.all()
        
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def public(self, request):
        """Get only public workouts"""
        workouts = Workout.objects.filter(is_public=True)
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)

class UserWorkoutViewSet(viewsets.ModelViewSet):
    """ViewSet for managing user workout completions"""
    queryset = UserWorkout.objects.all()
    serializer_class = UserWorkoutSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # Set the user (for now, using first user)
        # In a real app, this would be request.user
        user = User.objects.first()
        serializer.save(user=user)

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get workout completions for a specific user"""
        user_id = request.query_params.get('user_id')
        if user_id:
            user_workouts = UserWorkout.objects.filter(user___id=user_id)
        else:
            user_workouts = UserWorkout.objects.all()
        
        serializer = self.get_serializer(user_workouts, many=True)
        return Response(serializer.data)
