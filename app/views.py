from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from app.forms import RegisterUserForm
from app.models import User


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


class RegisterUserView(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = "registration/register.html"

    success_url = reverse_lazy("app:login")
