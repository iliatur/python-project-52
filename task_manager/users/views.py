from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from task_manager.users.forms import (
    UserLoginForm,
    UserRegistrationForm,
    UserUpdateForm,
)

User = get_user_model()


# 🔹 Миксин для обработки отсутствия прав
class PermissionDeniedMixin:
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                _("You are not logged in! Please log in.")
            )
            return redirect(
                f"{reverse_lazy('login')}?next={self.request.path}"
            )

        messages.error(
            self.request,
            _("You do not have permission to perform this action.")
        )
        return redirect('users_index')


# 🔹 Список пользователей
class UsersIndexView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


# 🔹 Регистрация пользователя
class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = _('User created successfully')


# 🔹 Обновление пользователя
class UserUpdateView(
    PermissionDeniedMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    UpdateView
):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_index')
    success_message = _('User updated successfully')

    def test_func(self):
        return self.request.user == self.get_object()

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, self.object)
        return response


# 🔹 Удаление пользователя
class UserDeleteView(
    PermissionDeniedMixin,
    LoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    DeleteView
):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users_index')
    success_message = _('User deleted successfully')

    def test_func(self):
        return self.request.user == self.get_object()

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                _("It is impossible to delete the user "
                  "because it is being used")
            )
            return redirect(self.success_url)


# 🔹 Логин
class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_message = _("You are logged in")

    def get_success_url(self):
        return reverse_lazy('index')


# 🔹 Логаут
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)