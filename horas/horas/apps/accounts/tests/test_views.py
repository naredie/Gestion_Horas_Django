from django.test import TestCase
from django.urls import reverse_lazy

from horas.apps.accounts.tests.utils import create_user
from horas.apps.accounts.enums import UserRole


USER_URLS = tuple(map(reverse_lazy, ["user-add", "user-list"]))


class HumanResourcesEmployeeViewTest(TestCase):
    """Test to access human resources view with an employee."""

    def setUp(self):
        self.user = create_user("user_test", roles=[UserRole.EMPLOYEE])
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_view_url_not_accessible(self):
        self.client.force_login(self.user)
        for url in USER_URLS:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 302)


class HumanResourcesManagerViewTest(TestCase):
    """Test to access human resources view with a manager."""

    def setUp(self):
        self.user = create_user("user_test", roles=[UserRole.MANAGER])
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_view_url_not_accessible(self):
        self.client.force_login(self.user)
        for url in USER_URLS:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 302)


class HumanResourcesHRViewTest(TestCase):
    """Test to access human resources view with an human resources."""

    def setUp(self):
        self.user = create_user("user_test", roles=[UserRole.HUMAN_RESOURCES])
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_view_url_accessible(self):
        self.client.force_login(self.user)
        for url in USER_URLS:
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)
