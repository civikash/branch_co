from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib import messages

class LoginView(LoginView):
    template_name = 'account/login.html'
    success_url = '/reports/'
    admin_url = '/admin-control/reports/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect(self.admin_url)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)
            if self.request.GET.get('next'):
                self.success_url = self.request.GET.get('next')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Старый пароль неверный!')
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Неправильное имя пользователя или пароль!')
        return super().form_invalid(form)

