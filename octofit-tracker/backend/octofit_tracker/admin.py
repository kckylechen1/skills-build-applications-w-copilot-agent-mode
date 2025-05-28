from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout, UserWorkout

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for User model"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_joined')
    list_filter = ('date_joined',)
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('_id', 'date_joined')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('System Information', {
            'fields': ('_id', 'date_joined'),
            'classes': ('collapse',)
        })
    )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin configuration for Team model"""
    list_display = ('name', 'created_by', 'member_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description', 'created_by__username')
    ordering = ('-created_at',)
    readonly_fields = ('_id', 'created_at')
    filter_horizontal = ('members',)
    
    def member_count(self, obj):
        """Display member count"""
        return obj.members.count()
    member_count.short_description = 'Members'
    
    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'description', 'created_by')
        }),
        ('Members', {
            'fields': ('members',)
        }),
        ('System Information', {
            'fields': ('_id', 'created_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin configuration for Activity model"""
    list_display = ('user', 'activity_type', 'duration_minutes', 'calories_burned', 'distance_km', 'date_logged')
    list_filter = ('activity_type', 'date_logged')
    search_fields = ('user__username', 'activity_type', 'notes')
    ordering = ('-date_logged',)
    readonly_fields = ('_id', 'activity_id', 'date_logged')
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('user', 'activity_type', 'duration_minutes', 'calories_burned', 'distance_km')
        }),
        ('Additional Details', {
            'fields': ('notes',)
        }),
        ('System Information', {
            'fields': ('_id', 'activity_id', 'date_logged'),
            'classes': ('collapse',)
        })
    )

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin configuration for Leaderboard model"""
    list_display = ('user', 'team', 'total_points', 'total_activities', 'total_calories', 'last_updated')
    list_filter = ('team', 'last_updated')
    search_fields = ('user__username', 'team__name')
    ordering = ('-total_points',)
    readonly_fields = ('_id', 'leaderboard_id', 'last_updated')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'team')
        }),
        ('Statistics', {
            'fields': ('total_points', 'total_activities', 'total_calories', 'total_distance', 'rank')
        }),
        ('System Information', {
            'fields': ('_id', 'leaderboard_id', 'last_updated'),
            'classes': ('collapse',)
        })
    )

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin configuration for Workout model"""
    list_display = ('name', 'difficulty_level', 'duration_minutes', 'created_by', 'is_public', 'created_at')
    list_filter = ('difficulty_level', 'is_public', 'created_at')
    search_fields = ('name', 'description', 'created_by__username')
    ordering = ('-created_at',)
    readonly_fields = ('_id', 'workout_id', 'created_at')
    
    fieldsets = (
        ('Workout Information', {
            'fields': ('name', 'description', 'difficulty_level', 'duration_minutes', 'calories_target')
        }),
        ('Exercises', {
            'fields': ('exercises',)
        }),
        ('Settings', {
            'fields': ('created_by', 'is_public')
        }),
        ('System Information', {
            'fields': ('_id', 'workout_id', 'created_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(UserWorkout)
class UserWorkoutAdmin(admin.ModelAdmin):
    """Admin configuration for UserWorkout model"""
    list_display = ('user', 'workout', 'actual_duration', 'calories_burned', 'rating', 'completed_at')
    list_filter = ('rating', 'completed_at')
    search_fields = ('user__username', 'workout__name', 'notes')
    ordering = ('-completed_at',)
    readonly_fields = ('_id', 'completed_at')
    
    fieldsets = (
        ('Workout Completion', {
            'fields': ('user', 'workout')
        }),
        ('Performance', {
            'fields': ('actual_duration', 'calories_burned', 'rating')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('System Information', {
            'fields': ('_id',),
            'classes': ('collapse',)
        })
    )
