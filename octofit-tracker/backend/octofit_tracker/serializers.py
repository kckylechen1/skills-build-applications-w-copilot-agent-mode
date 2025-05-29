from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout, UserWorkout

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class TeamSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'created_by', 'members', 'member_count', 'created_at']

    def get_member_count(self, obj):
        return obj.members.count()

class ActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)

    class Meta:
        model = Activity
        fields = [
            'id', 'activity_id', 'user', 'activity_type', 'activity_type_display',
            'duration_minutes', 'calories_burned', 'distance_km', 'notes', 'date_logged'
        ]
        read_only_fields = ['activity_id', 'date_logged']

    def create(self, validated_data):
        # Auto-generate activity_id
        import uuid
        validated_data['activity_id'] = str(uuid.uuid4())
        return super().create(validated_data)

class LeaderboardSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Leaderboard
        fields = [
            'id', 'leaderboard_id', 'user', 'team', 'total_points',
            'total_activities', 'total_calories', 'total_distance', 'rank', 'last_updated'
        ]
        read_only_fields = ['leaderboard_id', 'last_updated']

class WorkoutSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    difficulty_level_display = serializers.CharField(source='get_difficulty_level_display', read_only=True)

    class Meta:
        model = Workout
        fields = [
            'id', 'workout_id', 'name', 'description', 'difficulty_level',
            'difficulty_level_display', 'duration_minutes', 'calories_target',
            'exercises', 'created_by', 'is_public', 'created_at'
        ]
        read_only_fields = ['workout_id', 'created_at']

    def create(self, validated_data):
        # Auto-generate workout_id
        import uuid
        validated_data['workout_id'] = str(uuid.uuid4())
        return super().create(validated_data)

class UserWorkoutSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    workout = WorkoutSerializer(read_only=True)
    workout_id = serializers.CharField(write_only=True)

    class Meta:
        model = UserWorkout
        fields = [
            'id', 'user', 'workout', 'workout_id', 'completed_at',
            'actual_duration', 'calories_burned', 'rating', 'notes'
        ]
        read_only_fields = ['completed_at']

    def create(self, validated_data):
        workout_id = validated_data.pop('workout_id')
        try:
            workout = Workout.objects.get(workout_id=workout_id)
            validated_data['workout'] = workout
        except Workout.DoesNotExist:
            raise serializers.ValidationError({'workout_id': 'Workout not found'})
        return super().create(validated_data)

class ActivitySummarySerializer(serializers.Serializer):
    """Serializer for activity summary statistics"""
    total_activities = serializers.IntegerField()
    total_calories = serializers.IntegerField()
    total_distance = serializers.FloatField()
    total_duration = serializers.IntegerField()
    favorite_activity = serializers.CharField()

class TeamStatsSerializer(serializers.Serializer):
    """Serializer for team statistics"""
    team_name = serializers.CharField()
    total_members = serializers.IntegerField()
    total_activities = serializers.IntegerField()
    total_calories = serializers.IntegerField()
    average_calories_per_member = serializers.FloatField()