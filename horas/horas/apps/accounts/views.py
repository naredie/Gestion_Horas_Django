from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .decorators import human_resources_required

from .forms import UserForm

User = get_user_model()


@method_decorator(human_resources_required, name="dispatch")
class UserListView(ListView):
    model = User
    context_object_name = "users"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(tenant=self.request.user.tenant)
        return queryset


@method_decorator(human_resources_required, name="dispatch")
class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("user-list")

    def form_valid(self, form):
        form.instance.tenant = self.request.user.tenant
        print(form.instance)
        return super().form_valid(form)


@method_decorator(human_resources_required, name="dispatch")
class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy("user-list")


@method_decorator(human_resources_required, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy("user-list")
