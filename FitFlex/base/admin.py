from django.contrib import admin
from .models import client, workoutplan, progress_tracker
from datetime import date

@admin.register(client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'gender', 'age', 'joining_date', 'due_date', 'is_expired_status')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('gender', 'joining_date', 'due_date')
    ordering = ('-joining_date',)

    def is_expired_status(self, obj):
        """Show if the client subscription is expired"""
        if obj.due_date:
            return "Expired" if obj.due_date < date.today() else "Active"
        return "No Due Date"
    is_expired_status.short_description = "Status"


@admin.register(workoutplan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'client', 'duration_weeks')
    search_fields = ('plan_name', 'client__name')
    list_filter = ('duration_weeks',)
    ordering = ('-duration_weeks',)


@admin.register(progress_tracker)
class ProgressTrackerAdmin(admin.ModelAdmin):
    list_display = ('client', 'date', 'weight', 'bmi')
    search_fields = ('client__name',)
    list_filter = ('date',)
    ordering = ('-date',)
