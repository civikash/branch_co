from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.views.generic import View
from django.contrib.auth.views import LoginView


class LoginView(LoginView):
    template_name = 'account/login.html'
    success_url = '/reports/'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.GET.get('next'):
            self.success_url = self.request.GET.get('next')
        return response