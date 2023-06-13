from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.db.models import Max
from django.http import HttpResponseRedirect
from reports.models import ManagerRaportStatisticTrimestrial, InvestitiiActive1, InvestitiiActive2


class InvestitiListView(View):
    template_name = 'reports/reports/investiti/investiti_list.html'

    def dispatch(self, request, *args, **kwargs):
        rows = InvestitiiActive1.objects.filter(
            company__users__username=request.user).order_by('code')

        # получить максимальный код, если такие объекты уже существуют
        max_code = rows.last().code if rows.exists() else 0
        max_counter = InvestitiiActive1.objects.aggregate(
            Max('counter'))['counter__max'] or 0

        # создать новые объекты с одинаковым значением counter, начиная с max_counter + 1
        num_new_objs = 30 - len(rows)
        next_counter = max_counter + 1 if num_new_objs > 0 else max_counter + \
            1  # Определение значения next_counter

        # Проверка метода запроса
        if request.method == 'POST':
            # Создание первого объекта InfEconOp с заполненными полями company и counter
            inf_econ_op = InvestitiiActive1.objects.create(
                company=request.user.company, counter=next_counter)

            # Создание остальных объектов InfEconOp с увеличенным значением counter
            for i in range(29):
                InvestitiiActive1.objects.create(
                    company=request.user.company, counter=next_counter)

            # Создание объекта ManagerInfEconOp и связывание с InfEconOp
            manager_inf_econ_op = ManagerRaportStatisticTrimestrial.objects.create(
                reports=inf_econ_op)

            # Перенаправление на страницу, где будет отображен созданный объект
            return redirect('reports:reports-vision', uid=manager_inf_econ_op.uid)

        # Если метод запроса не POST, вызываем метод dispatch родительского класса
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        reports_user = ManagerRaportStatisticTrimestrial.objects.filter(
            reports__company=request.user.company)
        context = {'reports': reports_user}
        return render(request, self.template_name, context)


class InvestitiDetail(View):
    template_name = 'reports/reports/investiti/investitii_detail.html'
    user = None


    def get(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerRaportStatisticTrimestrial.objects.filter(uid=uid).first()
        print(manager_inf_econ_op)
        if not manager_inf_econ_op:
            return request("Отчет не найден")
        
        counter = manager_inf_econ_op.reports.counter
        sales = ManagerRaportStatisticTrimestrial.objects.filter(reports__uid=manager_inf_econ_op.uid).order_by('reports__code')
        s_invest = InvestitiiActive2.objects.filter(company__users__username=request.user).order_by('code')


        raport_detail = InvestitiiActive1.objects.filter(counter=counter).order_by('code')
        invest_item_2 = InvestitiiActive2.objects.filter(counter=counter).order_by('code')
        
        #INVEST
        codul_rind = [invest_o.codul_rind for invest_o in raport_detail]
        indicatori = [invest_o.indicatori for invest_o in raport_detail]
        intrari = [invest_o.intrari for invest_o in raport_detail]
        investitii = [invest_o.investitii for invest_o in raport_detail]
        codes = [sale.code for sale in raport_detail]

        invest_s_2_rows = []
        for i, invest_s_2 in enumerate(invest_item_2):
            crt = i + 1
            codul_rind = invest_s_2.codul_rind
            indicatori = invest_s_2.indicatori
            code_cuatm = invest_s_2.code_cuatm
            numa_oras = invest_s_2.numa_oras
            cladiri = invest_s_2.cladiri
            apart = invest_s_2.apart
            sup_total =invest_s_2.sup_total

            invest_s_2_rows.append({
                'crt': crt,
                'codul_rind': codul_rind,
                'indicatori': indicatori,
                'code_cuatm': code_cuatm,
                'numa_oras': numa_oras,
                'cladiri': cladiri,
                'apart': apart,
                'sup_total': sup_total,
            })

        invest_rows_1 = [
            {
                'crt': 1,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 2,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 3,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 4,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 5,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 6,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 7,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 8,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 9,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 10,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 11,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 12,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 13,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 14,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 15,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 16,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
            {
                'crt': 17,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                        {
                'crt': 18,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                        {
                'crt': 19,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                        {
                'crt': 20,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                                    {
                'crt': 21,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                                    {
                'crt': 22,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                                    {
                'crt': 23,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                                    {
                'crt': 24,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                                    {
                'crt': 25,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                                    {
                'crt': 26,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                                    {
                'crt': 27,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                                    {
                'crt': 28,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                                    {
                'crt': 29,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
                                    {
                'crt': 30,
                'codul_rind': codul_rind if codul_rind else '',
                'indicatori': indicatori if indicatori else '',
                'intrari': intrari if intrari else '',
                'investitii': investitii if investitii else ''
            },
        ]

       
        sales_list = ManagerRaportStatisticTrimestrial.objects.filter(reports__uid=manager_inf_econ_op.reports.uid).order_by('reports__counter')

        
        invest_2_list = InvestitiiActive2.objects.filter(company__users__username=request.user).order_by('code')
        
        current_inves = 0


        for sales in raport_detail: 
            invest_rows_1[current_inves]['codul_rind'] = sales.codul_rind
            invest_rows_1[current_inves]['indicatori'] = sales.indicatori
            invest_rows_1[current_inves]['intrari'] = sales.intrari
            invest_rows_1[current_inves]['investitii'] = sales.investitii
            invest_rows_1[current_inves]['code'] = sales.code
            current_inves += 1

        context = {'sales': sales, 'manager_inf_econ_op': manager_inf_econ_op, 'invest_rows_1': invest_rows_1, 'invest_s_2_rows': invest_s_2_rows}
        return render(request, self.template_name, context)
    
    def post(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerRaportStatisticTrimestrial.objects.get(uid=uid)

        counter_uid = manager_inf_econ_op.reports.counter



        rows = InvestitiiActive1.objects.filter(counter=counter_uid).order_by('code')
        rows_2 = InvestitiiActive2.objects.filter(company__users__username=request.user).order_by('code')
        

        #ITEMS - 1 -- POST
        codul_rind = [request.POST.get(f'codul_rind_{row.code}', None) for row in rows]
        indicatori = [request.POST.get(f'indicatori_{row.code}', None) for row in rows]
        intrari = [request.POST.get(f'intrari_{row.code}', None) for row in rows]
        investitii = [request.POST.get(f'investitii_{row.code}', None) for row in rows]

        #ITEMS - 2 -- POST
        d_t_ini = [request.POST.get(f'd_t_ini_{row.code}', None) for row in items_2]
        c_t_ini = [request.POST.get(f'c_t_ini_{row.code}', None) for row in items_2]
        calculat = [request.POST.get(f'calculat_{row.code}', None) for row in items_2]
        transferat = [request.POST.get(f'transferat_{row.code}', None) for row in items_2]
        d_t_fin = [request.POST.get(f'd_t_fin_{row.code}', None) for row in items_2]
        c_t_fin = [request.POST.get(f'c_t_fin_{row.code}', None) for row in items_2]

        counter = 0

        #HEADER -- POST
        for i, row, in enumerate(rows):
            try:
                report_item_1 = InvestitiiActive1.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.codul_rind = float(codul_rind[i]) if codul_rind[i] else None
                    report_item_1.indicatori = str(indicatori[i]) if indicatori[i] else None
                    report_item_1.intrari = float(intrari[i]) if intrari[i] else None
                    report_item_1.investitii = float(investitii[i]) if investitii[i] else None
                    report_item_1.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except InvestitiiActive1.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_1 = InvestitiiActive1.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.codul_rind = float(codul_rind[i]) if codul_rind[i] else None
                    report_item_1.indicatori = str(indicatori[i]) if indicatori[i] else None
                    report_item_1.intrari = float(intrari[i]) if intrari[i] else None
                    report_item_1.investitii = float(investitii[i]) if investitii[i] else None
                    report_item_1.save()
                    counter += 1
                    report_item_1.counter = counter
                    report_item_1.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")
        # print('POST Запрос',request.POST)
        # print(f"Number of InfEconOp objects saved: {counter}")  # выводим число сохраненных объектов
        return HttpResponseRedirect(request.path_info)