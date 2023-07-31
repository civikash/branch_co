# Руководство

# app - account
Данный модуль реализовывает функционал личных кабинетов, авторизации, информации о пользователе и его организации
templates\account 
- Шаблоны, элементы страниц, приложения account

  account\views
  # company.py

    Класс CompanyDataView(LoginRequiredMixin, View) реализовывает возможность сохранения информации о организации, которую ввел пользователь. Выполняются две функции: get и post
  
          class CompanyDataView(LoginRequiredMixin, View):
            template_name = 'account/company_account.html'
            success_url = '/reports/'
        
            def get(self, request, *args, **kwargs):
                company_data = CompanyData.objects.filter(user=request.user).first()
                context = {'company_data': company_data}
                return render(request, self.template_name, context)
        
            def post(self, request, *args, **kwargs):
                company_data = CompanyData.objects.filter(user=request.user).first()
                if company_data:
                    company_data.name = request.POST.get('name')
                    company_data.address = request.POST.get('address')
                    company_data.district = request.POST.get('district')
                    company_data.village = request.POST.get('village')
                    company_data.street = request.POST.get('street')
                    company_data.code_cuiio = request.POST.get('code_cuiio')
                    company_data.code_idno = request.POST.get('code_idno')
                    company_data.ruler = request.POST.get('ruler')
                    company_data.accountant = request.POST.get('accountant')
                    company_data.executor = request.POST.get('executor')
                    company_data.tel = request.POST.get('tel')
                    company_data.anul = request.POST.get('anul')
                else:
                    company_data = CompanyData(
                        name=request.POST.get('name'),
                        user=request.user,
                        address=request.POST.get('address'),
                        district=request.POST.get('district'),
                        village=request.POST.get('village'),
                        street=request.POST.get('street'),
                        code_cuiio=request.POST.get('code_cuiio'),
                        code_idno=request.POST.get('code_idno'),
                        ruler=request.POST.get('ruler'),
                        accountant=request.POST.get('accountant'),
                        executor=request.POST.get('executor'),
                        tel=request.POST.get('tel'),
                        anul=request.POST.get('anul'),
                    )
                
                try:
                    company_data.full_clean()
                    company_data.save()
        
                    user = request.user
                    user.company = company_data
                    user.save()
        
                    return redirect(self.success_url)
                except ValidationError as e:
                    return render(request, self.template_name, {'form': company_data, 'errors': e.message_dict})

  

  # login.py
  
  Класс LoginView(LoginView) реализовывает авторизацию на сайте. Методы form_valid и form_invalid отвечают за валидацию введенных пользователем данных

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

  # logout.py
  
  Класс LogoutView(View) реализовывает выход из профиля

      class LogoutView(View):
          def get(self, request):
              logout(request)
              return redirect('account:login')

  # signout.py

  Данный модуль не используется в проекте и деактивирован. Отвечает за регистрацию на сайте


  # users.py

  Реализация подробного просмотра профиля пользователя - class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, View) -, общий просмотр списка пользователей -  class UsersView(View) - и создание нового пользователя в системе - class AddUserView(View) -.

        class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
          template_name = 'account/user_detail.html'
      
          def test_func(self):
              return self.request.user.is_superuser
          
          def dispatch(self, request, *args, **kwargs):
              response = super().dispatch(request, *args, **kwargs)
              if not request.user.is_superuser:
                  raise PermissionDenied
              return response
      
          def get(self, request, id, *args, **kwargs):
              user = get_object_or_404(User, id=id)
              context = {'user': user}
              return render(request, self.template_name, context)
      
          def post(self, request, id, *args, **kwargs):
              user = get_object_or_404(User, id=id)
              old_password = request.POST.get('old_password')
              new_password = request.POST.get('password')
              if not user.check_password(old_password):
                  messages.error(request, 'Старый пароль неверный!')
                  return redirect('account:users-detail', id=id)
              user.set_password(new_password)
              user.save()
              messages.success(request, 'Пароль успешно изменен!')
              return redirect('account:users-detail', id=id)
          
      class UsersView(View):
          template_name = 'account/users.html'
      
          def dispatch(self, request, *args, **kwargs):
              response = super().dispatch(request, *args, **kwargs)
              if not request.user.is_superuser:
                  raise PermissionDenied
              return response
      
          def get(self, request):
              users = User.objects.all()
              context = {
                  'users': users
              }
              return render(request, self.template_name, context)
          
      
      class AddUserView(View):
          template_name = 'account/users_add.html'
      
          def dispatch(self, request, *args, **kwargs):
              response = super().dispatch(request, *args, **kwargs)
              if not request.user.is_superuser:
                  raise PermissionDenied
              return response
      
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
      
              return redirect('account:users')
  account\models
  # models.py
     Модель пользователя, где происходит привязка организации к профилю
          class User(AbstractUser):
              company = models.ForeignKey(CompanyData, on_delete=models.PROTECT, null=True, related_name='users')
              user_permissions = models.ManyToManyField(
                  'auth.Permission',
                  blank=True,
                  related_name='user_set_custom'
              )
              groups = models.ManyToManyField(
                  'auth.Group',
                  blank=True,
                  related_name='user_set_custom'
              )

  




    # APP - REPORTS (!!!Модуль отчетов !!!)
    Здесь описан основной функционал модуля отчетов. Реализация построена на одной парадигме. В папке views этого приложения находится реализация всех отчетов в системе, каждомо отчету сопутствует свой файл
    
        class BalantaListView(View):
        template_name = 'reports/reports/balanta/balanta_list.html'
        ""
        В данном методе реализована разбивка на несколько частей одного отчета,
        осуществляется фильтрация по коду (который у каждого отчета совсем уникальный)
        и по пользователю.
        ""
        def dispatch(self, request, *args, **kwargs):
            rows = Balanta1.objects.filter(
                company__users__username=request.user).order_by('code')
            item_1 = Balanta2.objects.filter(
                company__users__username=request.user).order_by('code')
            item_2 = Balanta3.objects.filter(
                company__users__username=request.user).order_by('code')
            item_3 = Balanta4.objects.filter(
                company__users__username=request.user).order_by('code')
    
            ""
            получить максимальный код, если такие объекты уже существуют.
            Каждый новый созданный отчет будет получать прибавление к 'counter' в зависимости от
            Последнего созданного значения и его счетчика
            ""
            max_code = rows.last().code if rows.exists() else 0
            max_counter = Balanta1.objects.aggregate(
                Max('counter'))['counter__max'] or 0
            
            max_code_item_1 = item_1.last().code if item_1.exists() else 0
            max_counter_1 = Balanta2.objects.aggregate(
                Max('counter'))['counter__max'] or 0
            
            max_code_item_2 = item_2.last().code if item_2.exists() else 0
            max_counter_2 = Balanta3.objects.aggregate(
                Max('counter'))['counter__max'] or 0
            
            max_code_item_3 = item_3.last().code if item_3.exists() else 0
            max_counter_3 = Balanta4.objects.aggregate(
                Max('counter'))['counter__max'] or 0
    
            num_new_objs = 130 - len(rows)
            next_counter = max_counter + 1 if num_new_objs > 0 else max_counter + 1  # Определение значения next_counter
    
            item_new_objs_1 = 44 - len(item_1)
            next_counter_item_1 = max_counter_1 + 1 if item_new_objs_1 > 0 else max_counter_1 + 1  # Определение значения next_counter
    
            item_new_objs_2 = 22 - len(item_2)
            next_counter_item_2 = max_counter_2 + 1 if item_new_objs_2 > 0 else max_counter_2 + 1  # Определение значения next_counter
    
            item_new_objs_3 = 29 - len(item_3)
            next_counter_item_3 = max_counter_3 + 1 if item_new_objs_3 > 0 else max_counter_3 + 1  # Определение значения next_counter
    
            # Проверка метода запроса. При создании каждого нового отчета, данные, которые представлены в списке будут автоматически созданы в соответствующих полях модели.
            if request.method == 'POST':
                indocatori = ['']
                code_rd = ['']
                
                indicatori_2_turple = ['']
                
                code_rd_2 = ['']
    
                indicatori_3_turple = ['']
    
                code_rd_3 = ['']
    
                indicatori_4_turple = ['']
                
                code_rd_4 = ['']
    
                # Создание первого объекта с заполненными полями company и counter
                if request.user.company:
                    inf_econ_op = Balanta1.objects.create(
                        company=request.user.company, counter=next_counter)
                
                    item_post_1 = Balanta2.objects.create(
                            company=request.user.company, counter=next_counter_item_1)
                    
                    item_post_2 = Balanta3.objects.create(
                        company=request.user.company, counter=next_counter_item_2)
                    
                    item_post_3 = Balanta4.objects.create(
                        company=request.user.company, counter=next_counter_item_3)
                else:
                    return redirect('account:company-data')
    
                # Создание остальных объектов с увеличенным значением counter
                for i, (n, ind) in zip(range(129), zip(indocatori[1:], code_rd[1:])):
                    if ind == '':
                        ind = None
                    Balanta1.objects.create(
                        company=request.user.company, counter=next_counter, indicatorii=n, code_rind=ind)
                
                for i, (n2, ind2) in zip(range(43), zip(indicatori_2_turple[1:], code_rd_2[1:])):
                    if ind2 == '':
                        ind2 = None
                    Balanta2.objects.create(
                        company=request.user.company, counter=next_counter, indicatorii=n2, code_rind=ind2)
                    
    
                for i, (n3, ind3) in zip(range(21), zip(indicatori_3_turple[1:], code_rd_3[1:])):
                    if ind3 == '':
                        ind3 = None
                    Balanta3.objects.create(
                        company=request.user.company, counter=next_counter, indicatorii=n3, code_rind=ind3)
                    
                for i, (n4, ind4) in zip(range(28), zip(indicatori_4_turple[1:], code_rd_4[1:])):
                    if ind4 == '':
                        ind4 = None
                    Balanta4.objects.create(
                        company=request.user.company, counter=next_counter, indicatorii=n4, code_rind=ind4)
    
                # Создание объекта ManagerInfEconOp и связывание с InfEconOp
                ""
                Все модели которые начинаются на Manager хранят информацию по отчетам
                которые были созданы пользователем
                ""
                manager_inf_econ_op = ManagerRaportBalanta.objects.create(
                    reports=inf_econ_op, reports_2=item_post_1, reports_3=item_post_2, reports_4=item_post_3)
    
                # Перенаправление на страницу, где будет отображен созданный объект
                return redirect('reports:balanta-detail', uid=manager_inf_econ_op.uid)
    
            # Если метод запроса не POST, вызываем метод dispatch родительского класса
            return super().dispatch(request, *args, **kwargs)


              def get(self, request, *args, **kwargs):
                ""
                reports_user - выводит все отчеты, этого типа, которые были созданы пользователем
                ""
                reports_user = ManagerRaportBalanta.objects.filter(reports__company=request.user.company)
                context = {'reports': reports_user}
                return render(request, self.template_name, context)


  # class BalantaDetail - классы с аналогичными наименованиями отвечают за функционал самого отчета, где пользователь вводит данные



          class BalantaDetail(View):
            template_name = 'reports/reports/balanta/balanta_detail.html'
            user = None
        
        
            def get(self, request, uid, *args, **kwargs):
                ""
                manager_inf_econ_op - берется информация по отчету, который был открыт пользователем
                check_user - проверка, что это автор отчета
                counter - важная переменная, которая считает количество reports за manager
                sales - производит фильтрацию по коду.
                Остальные переменные реализовывают фильтрацию по коду и counter чтобы взять все части одного отчета
                Проще говоря, отчет имеет свой counter, его части отчета имеют такой же counter и они получаются связанные засчет этого
                числа
                ""
                manager_inf_econ_op = ManagerRaportBalanta.objects.filter(uid=uid).first()
                check_user = ManagerRaportBalanta.objects.filter(reports__company=request.user.company)
                
                counter = manager_inf_econ_op.reports.counter
        
                sales = ManagerRaportBalanta.objects.filter(reports__uid=manager_inf_econ_op.uid).order_by('reports__code')
        
                items_1 = Balanta2.objects.filter(company__users__username=request.user).order_by('code')
                items_2 = Balanta3.objects.filter(company__users__username=request.user).order_by('code')
                items_3 = Balanta4.objects.filter(company__users__username=request.user).order_by('code')
        
                raport_detail = Balanta1.objects.filter(counter=counter).order_by('code')
        
                raport_item_1 = Balanta2.objects.filter(counter=counter).order_by('code')
                raport_item_2 = Balanta3.objects.filter(counter=counter).order_by('code')
                raport_item_3 = Balanta4.objects.filter(counter=counter).order_by('code')
                
                data_1 = Balanta1.objects.filter(counter=counter).first()
                data_2 = Balanta2.objects.filter(counter=counter).first()
                data_3 = Balanta3.objects.filter(counter=counter).first()
                data_4 = Balanta4.objects.filter(counter=counter).first()

    
  

  
