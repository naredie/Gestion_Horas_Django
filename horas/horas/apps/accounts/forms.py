from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Custom UserCreationForm"""

    class Meta:
        model = User
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    """Custom UserChangeForm"""

    class Meta:
        model = User
        fields = "__all__"


class UserForm(UserCreationForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        ),
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={"placeholder": "Repeat password", "class": "form-control"}
        ),
    )

    class Meta:
        model = get_user_model()

        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "is_user",
            "is_manager",
            "is_human_resources",
            "password1",
            "password2",
        ]

        localized_fields = "__all__"

        labels = {
            "is_user": "Es usuario",
            "is_manager": "Es manager",
            "is_human_resources": "Es recursos humanos",
        }

        widgets = {
            "username": forms.TextInput(
                attrs={"placeholder": "Nombre de usuario", "class": "form-control"}
            ),
            "email": forms.TextInput(
                attrs={"placeholder": "E-Mail", "class": "form-control"}
            ),
            "first_name": forms.TextInput(
                attrs={"placeholder": "Nombre", "class": "form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"placeholder": "Apellidos", "class": "form-control"}
            ),
        }
