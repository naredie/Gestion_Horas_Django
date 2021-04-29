from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("month/<str:monthindex>/", views.index, name="indexmonth"),
    path(
        "newevent/<str:year_url>/<str:month_url>/<str:day_url>/",
        views.create_event,
        name="createEvent",
    ),
    path("newevent/", views.create_event, name="createEventNodate"),
    path("calendar/", views.create_calendar, name="calendar"),
    path("event/<int:event_id>/", views.get_single_event, name="seeEvent"),
    path("event/edit/<int:event_id>/", views.edit_single_event, name="editEvent"),
    path("event/update/<int:event_id>/", views.update_single_event, name="updateEvent"),
    path("event/delete/<int:event_id>/", views.delete_event, name="deleteEvent"),
    path("event/save/", views.save_event, name="save"),
    path("creteproject/", views.create_project, name="createproject"),
    path("project/save/", views.save_project, name="saveproject"),
    path("manager/", views.index_manager, name="manager"),
    path(
        "confirm/hours/<str:month>/<str:year>/<int:user_id>/",
        views.confirm_hours,
        name="confirm_month_hours",
    ),
    path(
        "revision/hours/<str:month>/<str:year>/<int:user_id>/",
        views.revision_hours,
        name="revision_month_hours",
    ),
    path(
        "manager/confirm/user/hours/<int:monthhours_id>/",
        views.manager_accept_hours,
        name="accept_user_hours",
    ),
]
