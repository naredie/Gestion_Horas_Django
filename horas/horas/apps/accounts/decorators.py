from django.contrib.auth.decorators import user_passes_test


def maganager_required(function=None, redirect_field_name=None, login_url=None):
    """
    Decorator for views that checks that the user is a manager, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_manager,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def human_resources_required(function=None, redirect_field_name=None, login_url=None):
    """
    Decorator for views that checks that the user is a human resources,
    redirecting to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated and u.is_human_resources,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
