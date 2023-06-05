from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.db.models import Max
from django.http import HttpResponseRedirect
from reports.models import InfEconOp, ManagerInfEconOp


class InfEconOpCreateView(View):
    template_name = 'reports/reports/economica.html'

    def dispatch(self, request, *args, **kwargs):
        rows = InfEconOp.objects.filter(
            company__users__username=request.user).order_by('code')

        # получить максимальный код, если такие объекты уже существуют
        max_code = rows.last().code if rows.exists() else 0
        max_counter = InfEconOp.objects.aggregate(
            Max('counter'))['counter__max'] or 0

        # создать новые объекты с одинаковым значением counter, начиная с max_counter + 1
        num_new_objs = 19 - len(rows)
        next_counter = max_counter + 1 if num_new_objs > 0 else max_counter + 1  # Определение значения next_counter

        # Проверка метода запроса
        if request.method == 'POST':
            # Создание первого объекта InfEconOp с заполненными полями company и counter
            inf_econ_op = InfEconOp.objects.create(
                company=request.user.company, counter=next_counter)

            # Создание остальных объектов InfEconOp с увеличенным значением counter
            for i in range(18):
                InfEconOp.objects.create(
                    company=request.user.company, counter=next_counter)

            # Создание объекта ManagerInfEconOp и связывание с InfEconOp
            manager_inf_econ_op = ManagerInfEconOp.objects.create(
                reports=inf_econ_op)

            # Перенаправление на страницу, где будет отображен созданный объект
            return redirect('reports:reports-vision', uid=manager_inf_econ_op.uid)

        # Если метод запроса не POST, вызываем метод dispatch родительского класса
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        reports_user = ManagerInfEconOp.objects.filter(reports__company=request.user.company)
        context = {'reports': reports_user}
        return render(request, self.template_name, context)
