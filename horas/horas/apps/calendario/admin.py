from django.contrib import admin

from .models import Project, TimeEntry, MonthHours


class TimeEntryAdmin(admin.ModelAdmin):
    """ModelAdmin for TimeEntryAdmin"""

    readonly_fields = ("created_at",)
    list_display = ("title", "booking_date", "start_at", "finish_at", "project")


class ProjectAdmin(admin.ModelAdmin):
    """ModelAdmin for ProjectAdmin"""

    readonly_fields = ("created_at",)
    list_display = ("name", "created_at")


class MonthHoursAdmin(admin.ModelAdmin):
    """Custom MonthHours."""


admin.site.register(TimeEntry, TimeEntryAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(MonthHours, MonthHoursAdmin)
