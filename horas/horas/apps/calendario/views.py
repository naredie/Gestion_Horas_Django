import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from horas.apps.accounts.decorators import maganager_required

from .logic import (
    confirm_hours_to_manager,
    get_dashboard_data,
    get_manager_dashboard_data,
    get_project,
    get_projects,
    manager_accept_user_hours,
    revision_hours_to_manager,
)
from .models import Project, TimeEntry

User = get_user_model()


########---- CALENDAR ----########
@login_required
def create_calendar(request):
    """Calendar view."""
    # read timeEntryForm from database
    # eventos = TimeEntry.objects.all()
    eventos = TimeEntry.objects.filter(user=request.user)
    return render(
        request,
        "calendario/calendar.html",
        {
            "eventos": eventos,
        },
    )


########---- EVENT ----########
@login_required
def get_single_event(request, event_id):
    """View to get a single event."""
    event = get_object_or_404(TimeEntry, id=event_id)
    return render(
        request,
        "calendario/singleEvent.html",
        {
            "Event": event,
        },
    )


@login_required
def edit_single_event(request, event_id):
    """View to edit a single event."""
    event = get_object_or_404(TimeEntry, id=event_id)
    projects = get_projects()
    return render(
        request,
        "calendario/editSingleEvent.html",
        {"Event": event, "projects": projects, "selectedproject": event.project},
    )


@login_required
def update_single_event(request, event_id):
    """View to update a single event."""
    if request.method == "POST":
        # read data from form
        project_id = request.POST.get("project")
        booking_date = request.POST["bookingdate"]
        start_time = request.POST["starttime"]
        finish_time = request.POST["finishtime"]
        even_title = request.POST["eventitle"]

        # get project by id
        project = get_project(project_id)

        # if we dont find the project, we could have an exception so first look
        # if we update project or not
        if project:
            # get the event by id and update Event - with project
            _ = TimeEntry.objects.filter(id=event_id).update(
                booking_date=booking_date,
                start_at=start_time,
                finish_at=finish_time,
                project=project,
                title=even_title,
            )
        else:
            # get the event by id and update event - without Project
            _ = TimeEntry.objects.filter(id=event_id).update(
                booking_date=booking_date,
                start_at=start_time,
                finish_at=finish_time,
                title=even_title,
            )

    # redirect to calendar
    # maybe in the future add some message like "Event updated correctly"
    return redirect("calendar")


@login_required
def create_event(request, year_url=None, month_url=None, day_url=None):
    """Create event view"""
    if year_url is not None and month_url is not None and day_url is not None:
        date_ = datetime.datetime(int(year_url), int(month_url), int(day_url))
    else:
        date_ = None
    projects = get_projects()
    return render(
        request,
        "calendario/createEvent.html",
        {
            "date": date_,
            "projects": projects,
        },
    )


@login_required
def save_event(request):
    """View to save an event."""
    if request.method == "POST":
        # read data from form
        project_id = request.POST.get("project")
        bookingdate = request.POST["bookingdate"]
        starttime = request.POST["starttime"]
        finishtime = request.POST["finishtime"]
        eventitle = request.POST["eventitle"]

        project = get_project(project_id)

        event = TimeEntry(
            title=eventitle,
            start_at=starttime,
            finish_at=finishtime,
            booking_date=bookingdate,
            user=request.user,
            project=project,
        )

        # Event save
        event.save()

    return redirect("calendar")


@login_required
def delete_event(request, event_id):
    """Delete event"""
    _ = TimeEntry.objects.filter(id=event_id).delete()
    return redirect("calendar")


@login_required
def create_project(request):
    """Create project view"""
    managers = User.objects.filter(is_manager=True)
    return render(
        request,
        "calendario/createProject.html",
        {
            "title": "Crear nuevo proyecto",
            "managers": managers,
        },
    )


@login_required
def save_project(request):
    """View to save a project."""
    if request.method == "POST":
        # read data from form
        manager_id = request.POST.get("projectManager")
        projectname = request.POST["projectname"]
        projectdescription = request.POST["projectdescription"]
        projecthours = request.POST["projecthours"]

        manager = User.objects.get(id=manager_id)

        project = Project(
            name=projectname,
            description=projectdescription,
            stimated_hours=projecthours,
            project_open=True,
            manager=manager,
        )

        # Event save
        project.save()

    return redirect("calendar")


########---- DASHBOARD ----########
@login_required
def index(request, monthindex=None):
    """Index view"""
    user = request.user
    dashboard_data = get_dashboard_data(user, monthindex)
    return render(request, "calendario/index.html", dashboard_data)


@login_required
def confirm_hours(request, month, year, user_id):
    confirm_hours_to_manager(month, year, user_id)
    return redirect("index")


@login_required
def revision_hours(request, month, year, user_id):
    revision_hours_to_manager(month, year, user_id)
    return redirect("index")


########---- MANAGER ----########
@maganager_required(login_url="calendar")
def index_manager(request):
    """Manager view."""
    user = request.user
    manager_dashboard_data = get_manager_dashboard_data(user)
    return render(request, "calendario/manager.html", manager_dashboard_data)


def manager_accept_hours(request, monthhours_id):
    """Manager accept user hours."""
    manager_accept_user_hours(monthhours_id)
    return redirect("manager")
