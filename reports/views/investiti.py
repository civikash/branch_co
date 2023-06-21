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
            nrd = ['100', '200', '210', '220', '230', '240', '300', '400', '410',
                   '420', '430', '440', '441', '450', '460', '500', '600', '700',
                   '710', '720', '0', '810', '820', '830', '840', '850', '860', '870', 
                   '880', '890']
            indicatori = ['TOTAL imobilizări necorporale şi corporale (200 + 300)', 
                          'Imobilizări necorporale, total (210 + 220 + 230 + 240)', 
                          'drepturi de proprietate intelectuală', 'cheltuieli de cercetare-dezvoltare', 
                          'programe informatice', 'alte imobilizări necorporale', 
                          'Imobilizări corporale, total (400 + 500 + 600 + 700)', 
                          'Mijloace fixe, total (410 + 420 + 430 + 440 + 450 + 460)',
                          'clădiri rezidenţiale (de locuit)', 'clădiri nerezidențiale', 
                          'construcții speciale (inginereşti)', 'maşini, utilaje din care:', 
                          'tehnica de calcul', 'mijloace de transport', 'alte mijloace fixe', 
                          'Terenuri', 'Resurse minerale', 'Active biologice imobilizate (710 + 720)', 
                          'active biologice fitotehnie', 'active biologice zootehnie', 
                          'din rîndul 100 pe surse de finanţare:', 'surse proprii', 
                          'bugetul de stat', 'bugetele unităţilor administrativ-teritoriale',
                          'credite şi împrumuturi interne', 'credite şi împrumuturi externe',
                          'surse din străinătate', 'fondul rutier', 'fondul ecologic', 
                          'altele']

            # Создание первого объекта InfEconOp с заполненными полями company и counter
            if request.user.company:
                inf_econ_op = InvestitiiActive1.objects.create(
                    company=request.user.company, counter=next_counter, codul_rind=nrd[0], indicatori=indicatori[0])
            else:
                return redirect('account:company-data')


            # Создание остальных объектов InfEconOp с увеличенным значением counter
            for i, (n, ind) in zip(range(29), zip(nrd[1:], indicatori[1:])):
                InvestitiiActive1.objects.create(
                    company=request.user.company, counter=next_counter, codul_rind=n, indicatori=ind)

            # Создание объекта ManagerInfEconOp и связывание с InfEconOp
            manager_inf_econ_op = ManagerRaportStatisticTrimestrial.objects.create(
                reports=inf_econ_op)

            # Перенаправление на страницу, где будет отображен созданный объект
            return redirect('reports:investi-detail', uid=manager_inf_econ_op.uid)

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
        check_user = ManagerRaportStatisticTrimestrial.objects.filter(reports__company=request.user.company)
        
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
            code_cuatm = invest_s_2.code_cuatm
            numa_oras = invest_s_2.numa_oras
            cladiri = invest_s_2.cladiri
            apart = invest_s_2.apart
            sup_total =invest_s_2.sup_total

            invest_s_2_rows.append({
                'crt': crt,
                'codul_rind': codul_rind,
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
        current_marfa = 0

        for marfas_i in invest_item_2:
            invest_s_2_rows[current_marfa]['codul_rind'] = marfas_i.codul_rind
            invest_s_2_rows[current_marfa]['code_cuatm'] = marfas_i.code_cuatm
            invest_s_2_rows[current_marfa]['numa_oras'] = marfas_i.numa_oras
            invest_s_2_rows[current_marfa]['cladiri'] = marfas_i.cladiri
            invest_s_2_rows[current_marfa]['apart'] = marfas_i.apart
            invest_s_2_rows[current_marfa]['sup_total'] = marfas_i.sup_total
            invest_s_2_rows[current_marfa]['code'] = marfas_i.code
            current_marfa += 1  # увеличиваем текущий номер ячейки на 1

        for sales in raport_detail: 
            invest_rows_1[current_inves]['codul_rind'] = sales.codul_rind
            invest_rows_1[current_inves]['indicatori'] = sales.indicatori
            invest_rows_1[current_inves]['intrari'] = sales.intrari
            invest_rows_1[current_inves]['investitii'] = sales.investitii
            invest_rows_1[current_inves]['code'] = sales.code
            current_inves += 1

        context = {'sales': sales, 'manager_inf_econ_op': manager_inf_econ_op, 'invest_rows_1': invest_rows_1, 'invest_s_2_rows': invest_s_2_rows}
        
        if request.user.is_superuser or check_user:
            return render(request, self.template_name, context)
        elif not check_user:
            return redirect('reports:reports')
        
        return render(request, self.template_name, context)
    
    def post(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerRaportStatisticTrimestrial.objects.get(uid=uid)

        counter_uid = manager_inf_econ_op.reports.counter



        rows = InvestitiiActive1.objects.filter(counter=counter_uid).order_by('code')
        invest_s_2_rows = InvestitiiActive2.objects.filter(company__users__username=request.user).order_by('code')
        

        #ITEMS - 1 -- POST
        s_codul_rind = [request.POST.get(f's_codul_rind_{row.code}', None) for row in rows]
        indicatori = [request.POST.get(f'indicatori_{row.code}', None) for row in rows]
        intrari = [request.POST.get(f'intrari_{row.code}', None) for row in rows]
        investitii = [request.POST.get(f'investitii_{row.code}', None) for row in rows]

        #ITEMS - 2 -- POST
        codul_rind = [request.POST.get(f'codul_rind_{row.code}', None) for row in invest_s_2_rows]
        code_cuatm = [request.POST.get(f'code_cuatm_{row.code}', None) for row in invest_s_2_rows]
        numa_oras = [request.POST.get(f'numa_oras_{row.code}', None) for row in invest_s_2_rows]
        cladiri = [request.POST.get(f'cladiri_{row.code}', None) for row in invest_s_2_rows]
        apart = [request.POST.get(f'apart_{row.code}', None) for row in invest_s_2_rows]
        sup_total = [request.POST.get(f'sup_total_{row.code}', None) for row in invest_s_2_rows]


        new_codul_rind = request.POST.getlist('new_codul_rind_') 
        new_code_cuatm = request.POST.getlist('new_code_cuatm_')
        new_numa_oras = request.POST.getlist('new_numa_oras_')
        new_cladiri = request.POST.getlist('new_cladiri_')
        new_apart = request.POST.getlist('new_apart_')
        new_sup_total = request.POST.getlist('new_sup_total_')

        print('NECO', new_codul_rind)
        counter = 0

        #HEADER -- POST
        for i, row, in enumerate(rows):
            try:
                report_item_1 = InvestitiiActive1.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.codul_rind = float(s_codul_rind[i]) if s_codul_rind[i] else None
                    report_item_1.indicatori = str(indicatori[i]) if indicatori[i] else None
                    report_item_1.intrari = float(intrari[i]) if intrari[i] else None
                    report_item_1.investitii = float(investitii[i]) if investitii[i] else None
                    report_item_1.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except InvestitiiActive1.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_1 = InvestitiiActive1.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.codul_rind = float(s_codul_rind[i]) if s_codul_rind[i] else None
                    report_item_1.indicatori = str(indicatori[i]) if indicatori[i] else None
                    report_item_1.intrari = float(intrari[i]) if intrari[i] else None
                    report_item_1.investitii = float(investitii[i]) if investitii[i] else None
                    report_item_1.save()
                    counter += 1
                    report_item_1.counter = counter
                    report_item_1.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")

        for i, marfa, in enumerate(invest_s_2_rows):
            try:
                sec_inf_econ_op = InvestitiiActive2.objects.filter(company__users__username=request.user, code=marfa.code).first()
                if sec_inf_econ_op is not None:
                    sec_inf_econ_op.codul_rind = float(codul_rind[i]) if codul_rind[i] else None
                    sec_inf_econ_op.code_cuatm = float(code_cuatm[i]) if code_cuatm[i] else None
                    sec_inf_econ_op.numa_oras = str(numa_oras[i]) if numa_oras[i] else None
                    sec_inf_econ_op.cladiri = float(cladiri[i]) if cladiri[i] else None
                    sec_inf_econ_op.apart = float(apart[i]) if apart[i] else None
                    sec_inf_econ_op.sup_total = float(sup_total[i]) if sup_total[i] else None
                    sec_inf_econ_op.counter = counter_uid
                    sec_inf_econ_op.save()
                     # увеличиваем счетчик на 1 при успешном сохранении объекта
            except InvestitiiActive2.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                sec_inf_econ_op = InvestitiiActive2.objects.filter(company__users__username=request.user, code=marfa.code).first()
                if sec_inf_econ_op is not None:
                    sec_inf_econ_op.codul_rind = float(codul_rind[i]) if codul_rind[i] else None
                    sec_inf_econ_op.code_cuatm = float(code_cuatm[i]) if code_cuatm[i] else None
                    sec_inf_econ_op.numa_oras = str(numa_oras[i]) if numa_oras[i] else None
                    sec_inf_econ_op.cladiri = float(cladiri[i]) if cladiri[i] else None
                    sec_inf_econ_op.apart = float(apart[i]) if apart[i] else None
                    sec_inf_econ_op.sup_total = float(sup_total[i]) if sup_total[i] else None
                    sec_inf_econ_op.counter = counter_uid
                    sec_inf_econ_op.save()
                    sec_inf_econ_op.counter = counter_uid
                    sec_inf_econ_op.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")
        try:
            for i in range(len(new_codul_rind)):
                    new_sec_inf_econ_op = InvestitiiActive2.objects.create(company=request.user.company)
                    new_sec_inf_econ_op.codul_rind = float(new_codul_rind[i]) if new_codul_rind[i] else None
                    new_sec_inf_econ_op.code_cuatm = float(new_code_cuatm[i]) if new_code_cuatm[i] else None
                    new_sec_inf_econ_op.numa_oras = str(new_numa_oras[i]) if new_numa_oras[i] else None
                    new_sec_inf_econ_op.cladiri = float(new_cladiri[i]) if new_cladiri[i] else None
                    new_sec_inf_econ_op.apart = float(new_apart[i]) if new_apart[i] else None
                    new_sec_inf_econ_op.sup_total = float(new_sup_total[i]) if new_sup_total[i] else None
                    print(new_sec_inf_econ_op.codul_rind)
                    new_sec_inf_econ_op.save()
                    new_sec_inf_econ_op.counter = counter_uid
                    new_sec_inf_econ_op.save()
                    print(new_sec_inf_econ_op)
        except Exception as e:
            print(f"Error while creating new InvestitiiActive2 object: {e}")
            raise
        print('POST Запрос',request.POST)
        # print(f"Number of InfEconOp objects saved: {counter}")  # выводим число сохраненных объектов
        return HttpResponseRedirect(request.path_info)