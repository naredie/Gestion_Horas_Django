from django.test import TestCase
from django.urls import reverse

from horas.apps.accounts.tests.utils import create_user


class CalendarViewTest(TestCase):
    """Test to access calendar view."""

    def setUp(self):

        self.user = create_user("test")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_view_url_accessible(self):
        """Tests that calendar view is accessible"""
        self.client.force_login(self.user)
        resp = self.client.get(reverse("calendar"))
        self.assertEqual(resp.status_code, 200)


class NoUserTest(TestCase):
    """Test that a not loged-in user is redirected in views."""

    URLS_RESTRICTED = (
        reverse("index"),
        # reverse("createEvent"),
        reverse("createEventNodate"),
        reverse("calendar"),
        # reverse("seeEvent"),
        # reverse("editEvent"),
        # reverse("updateEvent"),
        reverse("save"),
    )

    def test_redirected_if_no_user(self):
        """
        Test that if there is not a user logged in, then the urls are
        redirected.
        """
        for url in self.URLS_RESTRICTED:
            resp = self.client.get(url)
            self.assertEqual(
                resp.status_code,
                302,  # redirected
                f"{url} must be redirected if user not logged in.",
            )


class IndexViewTest(TestCase):
    """Test to access index view."""

    def setUp(self):
        self.user = create_user("user_test")
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_view_url_accessible(self):
        """Tests that calendar view is accessible"""
        self.client.force_login(self.user)
        resp = self.client.get(reverse("index"))
        self.assertEqual(resp.status_code, 200)
