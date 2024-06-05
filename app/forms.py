from django.contrib.auth.forms import UserCreationForm
# from django import forms

from app.models import User


class RegisterUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields
