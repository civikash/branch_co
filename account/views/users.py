from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from account.models import User
import re


class UsersView(View):
    template_name = 'account/users.html'

    def get(self, request):
        users = User.objects.all()
        context = {
            'users': users
        }
        return render(request, self.template_name, context)
    

class AddUserView(View):
    template_name = 'account/users_add.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')


        if not password:
            return HttpResponse('Введите пароль')
        if len(password) < 8:
            return HttpResponse('Пароль должен содержать не менее 8 символов')
        if not re.search(r'[A-Z]', password):
            return HttpResponse('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r'[a-z]', password):
            return HttpResponse('Пароль должен содержать хотя бы одну строчную букву')


        # Проверка наличия обязательных полей
        if not username or not password:
            return HttpResponse('Заполните обязательные поля')

        # Проверка уникальности имени пользователя
        if User.objects.filter(username=username).exists():
            return HttpResponse('Имя пользователя уже занято')

        # Создание нового пользователя
        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        return HttpResponse('Форма успешно отправлена')