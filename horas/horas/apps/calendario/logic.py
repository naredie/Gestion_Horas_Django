import datetime
from datetime import date, timedelta

import requests
from django.contrib.auth import get_user_model
from .config import DECIMALS_HOUR
from .models import Project, TimeEntry, MonthHours


User = get_user_model()


def _get_city_weather(user):
    """Gets weather information."""
    # get current user city
    city = user.get_user_city()
    if city is None:
        city = "Valencia"
    url = (
        f"http://api.openweathermap.org/data/2.5/weather?q={city}"
        f"&units=imperial&appid=ab89686b88101b7d39b06806a16d7ea4"
    )
    # request the API data and convert the JSON to Python data types
    city_weather = requests.get(url).json()
    # fahrenheit to celsius grad
    temp_celsius = round(((city_weather["main"]["temp"] - 32) * 5 / 9), 1)

    weather = {
        "city": city,
        "temperature": temp_celsius,
        "icon": city_weather["weather"][0]["icon"],
    }
    return weather


def _sum_hours(time_entries):
    """
    Sums worked hours in time_entries.

    :return: The sum of worked hours.
    """
    hours = sum(map(lambda x: x.duration, time_entries), 0)
    hours = round(hours, DECIMALS_HOUR)
    return hours


def _get_current_week_entries(today, user):
    """Gets current week entries."""
    some_day = today + timedelta(days=1)
    monday_of_week = some_day - timedelta(days=(some_day.isocalendar()[2] - 1))
    sunday_of_week = monday_of_week + timedelta(days=6)
    weekevents = TimeEntry.objects.filter(
        booking_date__gte=monday_of_week, booking_date__lt=sunday_of_week, user=user
    )
    return weekevents


def _get_hours_pro_entry(time_entries):
    """
    Get worked hours in a single time_entrie.

    :return: event with property worked_hours with the worked hours in a entry.
    """
    events = []
    for event in time_entries:
        start_time = datetime.datetime(
            date.today().year,
            date.today().month,
            date.today().day,
            event.start_at.hour,
            event.start_at.minute,
            event.start_at.second,
        )
        end_time = datetime.datetime(
            date.today().year,
            date.today().month,
            date.today().day,
            event.finish_at.hour,
            event.finish_at.minute,
            event.finish_at.second,
        )

        timediff = end_time - start_time
        events.append(
            {
                "worked_hours": round(timediff.total_seconds() / 3600, DECIMALS_HOUR),
                "event": event,
            }
        )
    return events


def _calculate_hours_percent(used_hours, estimated_hours):
    """Calculate procent of hours"""
    percent = (used_hours * 100) / estimated_hours
    return percent


def _get_timeentry_user(user):
    return TimeEntry.objects.filter(user=user)


def _get_open_projects_info():
    """Gets open projects and sum the used hours"""
    projects = Project.objects.filter(project_open=True).order_by("created_at")
    projects_sum_hours = []
    for project in projects:
        time_entries_pro_project = TimeEntry.objects.filter(project=project)
        used_hours = _sum_hours(time_entries_pro_project)
        hours_percent = _calculate_hours_percent(used_hours, project.stimated_hours)
        projects_sum_hours.append(
            {
                "hours_percent_number": hours_percent,
                "hours_percent": f"{hours_percent}%",
                "worked_hours": used_hours,
                "project": project,
            }
        )
    return projects_sum_hours


def _get_user_pro_manager(managerid):
    """Get users by manager."""
    users_manager = User.objects.filter(manager=managerid)
    return users_manager


def _get_total_hours_pro_user(users_manager):
    """Get sum of hours for every user from a manager"""
    result = []
    for user in users_manager:
        time_entries_user = TimeEntry.objects.filter(user=user)
        sum_hours = _sum_hours(time_entries_user)
        hours_percent = _calculate_hours_percent(sum_hours, user.weekly_hours * 4)
        result.append(
            {
                "sum_hours": sum_hours,
                "user": user,
                "hours_percent_number": hours_percent,
                "hours_percent": f"{hours_percent}%",
                "stimated_month_hours": user.weekly_hours * 4,
                "current_year": datetime.date.today().year,
            }
        )
    return result


def _get_project_by_manager(userid):
    """Gets project by manager id."""
    return Project.objects.filter(project_open=True, manager=userid).order_by(
        "created_at"
    )


def _get_entries_by_month(user, monthindex):
    if monthindex is None:
        today = date.today()
    else:
        today = datetime.datetime(date.today().year, int(monthindex), date.today().day)

    time_entries_pro_month = TimeEntry.objects.filter(
        booking_date__year=today.year, booking_date__month=today.month, user=user
    ).order_by("booking_date")
    return time_entries_pro_month


def _save_month_user_hours(month, year, user_id):
    entries_month = _get_entries_by_month(user_id, month)
    # we can also get that value in the url
    sum_hours = _sum_hours(entries_month)
    employee = User.objects.get(id=user_id)
    define_date = datetime.datetime(int(year), int(month), 1)

    month_hours_exist = MonthHours.objects.filter(
        employee=user_id, month=define_date, year=define_date
    )
    if not month_hours_exist and sum_hours > 0:
        mont_hours = MonthHours(
            employee=employee,
            month=define_date,
            year=define_date,
            hours=sum_hours,
            team_manager=employee.get_user_manager(),
        )
        mont_hours.save()
    return month_hours_exist


def _get_hours_to_confirm(user):
    return MonthHours.objects.filter(
        team_manager=user, acepted_hours=False, pendent_to_acept_hours=True
    )


def _manager_accept_user_hours(monthhoursid):
    return MonthHours.objects.filter(id=monthhoursid).update(
        pendent_to_acept_hours=False, acepted_hours=True
    )


def _get_user_month_hours_to_confirm(user, month, year):
    hours_send_to_manager = True

    send_to_manager = MonthHours.objects.filter(
        employee=user,
        month__month=month,
        year__year=year,
    )

    if not send_to_manager:
        hours_send_to_manager = False
    return hours_send_to_manager

def _get_user_hours_send_to_manager(user, month, year):
    total_hours_send_to_manager = 0.0
    send_to_manager = MonthHours.objects.filter(
        employee=user,
        month__month=month,
        year__year=year,
    )
    if send_to_manager:
        total_hours_send_to_manager = send_to_manager[0].hours
    return total_hours_send_to_manager

def _get_user_hours_to_confirm_general(user, year):
    general_user_hours = MonthHours.objects.filter(
        pendent_to_acept_hours=False,
        acepted_hours=True,
        year__year=year,
        team_manager=user,
    ).order_by("month")
    result = []
    for user_hours in general_user_hours:
        name = f"{user_hours.employee.first_name} {user_hours.employee.last_name}"
        result.append(
            {
                "month": user_hours.month.strftime("%B"),
                "year": user_hours.year.year,
                "hours": user_hours.hours,
                "employee_name": name,
                "employeeId": user_hours.employee.id,
            }
        )
    return result


def _revision_hours_to_manager(month, year, user_id):
    entries_month = _get_entries_by_month(user_id, month)
    sum_hours = _sum_hours(entries_month)
    define_date = datetime.datetime(int(year), int(month), 1)

    month_hours_exist = MonthHours.objects.filter(
        employee=user_id, month=define_date, year=define_date
    )
    if month_hours_exist:
        month_hours_exist.update(
            pendent_to_acept_hours=True,
            acepted_hours=False,
            hours=sum_hours,
        )

    return month_hours_exist


def compute_dashboard_stats(time_entries, user):
    """
    Compute statistics needed for the dashboard.

    :param time_entries: List of TimeEntry.
    :return: Dict with stats.
    """
    today = date.today()
    year = today.year
    month = today.month
    week_events = _get_current_week_entries(today, user)
    weekly_hours = user.get_user_weekly_hours()
    entries_month = filter(
        lambda entry: entry.booking_date.year == year
        and entry.booking_date.month == month,
        time_entries,
    )
    entries_today = TimeEntry.objects.filter(booking_date=today, user=user)
    return {
        "total_hours_month": _sum_hours(entries_month),
        "total_hours_week": _sum_hours(week_events),
        "total_hours_today": _sum_hours(entries_today),
        "hours_week_left": round(weekly_hours - _sum_hours(week_events), DECIMALS_HOUR),
        "weekly_hours": weekly_hours,
    }


def get_projects():
    """Gets all projects."""
    return Project.objects.all()


def get_project(project_id):
    """Gets project by id."""
    return Project.objects.get(id=project_id)


def get_dashboard_data(user, monthindex):
    """Gets all dashboard data"""
    time_entries = _get_timeentry_user(user)
    last_events = time_entries.order_by("-created_at")[:5]
    events_with_single_entry_hours = _get_hours_pro_entry(last_events)

    stats = compute_dashboard_stats(time_entries, user)

    entries_month = _get_entries_by_month(user, monthindex)
    month_single_entry_hours = _get_hours_pro_entry(entries_month)
    sum_total_month_hours = _sum_hours(entries_month)
    if monthindex is None:
        today = date.today()
    else:
        today = datetime.datetime(date.today().year, int(monthindex), date.today().day)

    current_hour = datetime.datetime.now().time()

    weather = _get_city_weather(user)

    projects = _get_open_projects_info()
    # show if the user already send the month hours to the manager or not
    # used to disable or enable the button
    hours_send_to_manager = _get_user_month_hours_to_confirm(
        user, today.month, today.year
    )
    hours_send_to_confirm=_get_user_hours_send_to_manager(
        user, today.month, today.year
    )

    context = {
        "stats": stats,
        "todayDate": today,
        "currentHour": current_hour,
        "weather": weather,
        "projects": projects,
        "events": events_with_single_entry_hours,
        "month_entry_hours": month_single_entry_hours,
        "hours_send_to_manager": hours_send_to_manager,
        "sum_total_month_hours": sum_total_month_hours,
        "hours_send_to_confirm":hours_send_to_confirm
    }

    return context


def get_manager_dashboard_data(user):
    open_projects = _get_project_by_manager(user)
    users_pro_manager = _get_user_pro_manager(user)
    users_pro_manager_hours = _get_total_hours_pro_user(users_pro_manager)
    hours_to_confirm = _get_hours_to_confirm(user)
    general_acepted_hours = _get_user_hours_to_confirm_general(
        user, datetime.date.today().year
    )
    context = {
        "title": "Panel de Manager",
        "projects": open_projects,
        "users_manager": users_pro_manager_hours,
        "hours_to_confirm": hours_to_confirm,
        "general_acepted_hours": general_acepted_hours,
    }

    return context


def confirm_hours_to_manager(month, year, user_id):
    _ = _save_month_user_hours(month, year, user_id)


def manager_accept_user_hours(monthhoursid):
    _ = _manager_accept_user_hours(monthhoursid)


def revision_hours_to_manager(month, year, user_id):
    _ = _revision_hours_to_manager(month, year, user_id)
