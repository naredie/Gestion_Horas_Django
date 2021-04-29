from django.urls import include, path
from . import views

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/add/", views.UserCreateView.as_view(), name="user-add"),
    path("users/<int:pk>/", views.UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
]
