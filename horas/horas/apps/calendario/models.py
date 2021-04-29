import datetime as dt
from django import forms
from django.conf import settings
from django.db import models


class Project(models.Model):
    """Project model

    Project to associate time entries with.
    """

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stimated_hours = models.IntegerField(blank=True, null=True)
    project_open = models.BooleanField(default=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class MonthHours(models.Model):
    """Month model

    Month model to associate monthly time
    entries with user and confirmate it by manager.
    """

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="employees"
    )
    team_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="managers",
        blank=True,
        null=True,
    )
    month = models.DateField(blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    hours = models.FloatField(null=False)
    pendent_to_acept_hours = models.BooleanField(default=True)
    acepted_hours = models.BooleanField(default=False)
    paid_hours = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Hora Mensual"
        verbose_name_plural = "Horas Mensuales"
        ordering = ["-created_at"]

    def get_manager(self):
        return self.employee.get_user_manager()

    def __str__(self):
        employee_name = f"{self.employee.first_name} {self.employee.last_name}"
        month_year = f"{self.month.strftime('%B')} de {self.month.year}"
        return f"{employee_name} - Horas del mes de {month_year}"

    # def save(self, *args, **kwargs):
    #     if self.team_manager is None:  # Set default reference
    #         self.team_manager = self.get_manager()
    #     super(MonthHours, self).save(*args, **kwargs)


class TimeEntry(models.Model):
    """
    Model to store individual entries per day.

    :param user: User associated to.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    start_at = models.TimeField(blank=False)
    finish_at = models.TimeField(blank=False)
    booking_date = models.DateField()
    project = models.ForeignKey(
        Project, editable=True, on_delete=models.CASCADE, blank=True, null=True
    )

    @property
    def duration(self):
        """Duration in hours."""
        finish_at = dt.datetime.combine(dt.date.today(), self.finish_at)
        start_at = dt.datetime.combine(dt.date.today(), self.start_at)
        duration = finish_at - start_at
        return duration.total_seconds() / 3600

    class Meta:
        verbose_name = "Hora_de_trabajo"
        verbose_name_plural = "Horas de trabajo"
        ordering = ["-created_at"]


class TimeEntryForm(forms.ModelForm):
    """Form for time entries."""

    class Meta:
        model = TimeEntry
        fields = ["start_at", "finish_at"]
        widgets = {
            "start_at": forms.TimeInput(
                attrs={"placeholder": "Select start time", "type": "time"},
            ),
            "finish_at": forms.TimeInput(
                attrs={"placeholder": "Select finish time", "type": "time"},
            ),
        }
