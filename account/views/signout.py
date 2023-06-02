from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.views.generic import View
from account.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class RegisterView(View):
    template_name = 'account/signout.html'

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User(username=username)
            user.set_password(password)
            user.save()
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('reports:reports')
        return render(request, self.template_name, {'form': form})