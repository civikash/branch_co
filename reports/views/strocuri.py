from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.db.models import Max
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect, HttpResponse
from reports.models import Stocuri1, Stocuri2, ManagerRaportStocuri


class StrocuriListView(View):
    template_name = 'reports/reports/strocuri/strocuri_list.html'

    def dispatch(self, request, *args, **kwargs):
        strocuri_1 = Stocuri1.objects.filter(
            company__users__username=request.user).order_by('code')
        strocuri_2 = Stocuri2.objects.filter(
            company__users__username=request.user).order_by('code')

        # получить максимальный код, если такие объекты уже существуют
        max_code = strocuri_1.last().code if strocuri_1.exists() else 0
        max_counter = Stocuri1.objects.aggregate(
            Max('counter'))['counter__max'] or 0
        
        max_code_item_1 = strocuri_2.last().code if strocuri_2.exists() else 0
        max_counter_1 = Stocuri2.objects.aggregate(
            Max('counter'))['counter__max'] or 0

        # Stocuri1 создать новые объекты с одинаковым значением counter, начиная с max_counter + 1
        num_new_objs = 4 - len(strocuri_1)
        next_counter = max_counter + 1 if num_new_objs > 0 else max_counter + 1  # Определение значения next_counter

        # Stocuri2
        item_new_objs_1 = 31 - len(strocuri_2)
        next_counter_item_1 = max_counter_1 + 1 if item_new_objs_1 > 0 else max_counter_1 + 1  # Определение значения next_counter


        # Проверка метода запроса
        if request.method == 'POST':
            nrd = ['2000', '2300', '2400', '2500']
            indicatori = ['Stocuri - total', 'din care: Producția în curs de execuție (215)', 'Produse (216)', 'Mărfuri (217)']
            
            nrd_2 = ['0100', '0101', '0102', '0103', '0110', '0120', '0121', '0122', '0130', '0131', '0132',
                     '0140', '0141', '0150', '0160', '0170', '0180', '0190', '0200', '0300', '0310', '0320', '0500',
                     '0510', '0520', '0540', '0700', '0800', '0900', '1000', '1010']
            indicatori_2 = ['Cifra de afaceri (venituri din vânzări), fără TVA și accize (contul 611; 613) (rd.0101+rd.0102+rd.0103); (rd.0110+rd.0120+rd.0130+rd.0140+rd.0150+0160)', 
                            'din care: pentru prima lună a trimestrului', 'pentru a doua lună a trimestrului', 'pentru a treia lună a trimestrului',
                            'din rd.0100 inclusiv din: vânzarea produselor - total (6111)', 'vânzarea mărfurilor - total (6112)', 'inclusiv: cu amănuntul', 'cu ridicata',
                            'prestarea serviciilor, executarea lucrărilor, alte venituri din vânzări, (6113, 6114, 6117, 6118)',
                            'din care: prestate întreprinderilor', 'prestate populației', 'contracte de construcție (6115)', 'din care: populației',
                            'contracte de leasing operațional și financiar (arendă, locațiune), (6116)', 'venituri din dobânzile aferente împrumuturilor acordate (613)', 
                            'din rd. 0100 - venituri din vânzarea apartamentelor noi și caselor particulare noi populației', 
                            'Alte venituri din activitatea operațională (contul 612)', 'Valoarea contabilă a mărfurilor vîndute',
                            'Costuri și cheltuieli operaționale - total (rd.0300+rd.0500+rd. 0700+rd. 0800+rd.0900+rd.1000)',
                            'Costuri și cheltuieli materiale - total, din care:', 'materii prime, materiale, semifabricate cumpărate, piese de schimb',
                            'combustibil', 'Costuri și cheltuieli aferente serviciilor (lucrărilor) prestate (executate) de terți în cadrul activității operaționale – total, din care:',
                            'de transport', 'de comunicații', 'de prelucrare a materiei prime proprii', 'Amortizarea și deprecierea activelor imobilizate', 
                            'Remunerarea muncii', 'Contribuții de asigurări sociale de stat obligatorii', '	Alte costuri și cheltuieli operaționale - total, din care:', 
                            'privind leasing operațional (arendă, locațiune )']
            print(len(indicatori_2))

            # Создание первого объекта InfEconOp с заполненными полями company и counter
            if request.user.company:
                inf_econ_op = Stocuri1.objects.create(
                    company=request.user.company, counter=next_counter, code_rind=nrd[0], indicatori=indicatori[0])
                
                item_post_1 = Stocuri2.objects.create(
                    company=request.user.company, counter=next_counter_item_1, code_rind=nrd_2[0], indicatorii=indicatori_2[0])
            else:
                return redirect('account:company-data')

            # Создание остальных объектов InfEconOp с увеличенным значением counter
            for i, (n, ind) in zip(range(3), zip(nrd[1:], indicatori[1:])):
                Stocuri1.objects.create(
                    company=request.user.company, counter=next_counter, code_rind=n, indicatori=ind)
            
            for i, (rnd, indic) in zip(range(30), zip(nrd_2[1:], indicatori_2[1:])):
                Stocuri2.objects.create(
                    company=request.user.company, counter=next_counter_item_1, code_rind=rnd, indicatorii=indic)
                

            # Создание объекта ManagerInfEconOp и связывание с InfEconOp
            manager_inf_econ_op = ManagerRaportStocuri.objects.create(
                reports=inf_econ_op, ci_2=item_post_1)

            # Перенаправление на страницу, где будет отображен созданный объект
            return redirect('reports:strocuri-detail', uid=manager_inf_econ_op.uid)

        # Если метод запроса не POST, вызываем метод dispatch родительского класса
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        reports_user = ManagerRaportStocuri.objects.filter(reports__company=request.user.company)
        context = {'reports': reports_user}
        return render(request, self.template_name, context)


class StrocuriDetail(View):
    template_name = 'reports/reports/strocuri/strocuri_detail.html'
    user = None


    def get(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerRaportStocuri.objects.filter(uid=uid).first()
        check_user = ManagerRaportStocuri.objects.filter(reports__company=request.user.company)
            
        
        counter = manager_inf_econ_op.reports.counter
        sales = ManagerRaportStocuri.objects.filter(reports__uid=manager_inf_econ_op.uid).order_by('reports__code')

        items_1 = Stocuri2.objects.filter(company__users__username=request.user).order_by('code')

        raport_detail = Stocuri1.objects.filter(counter=counter).order_by('code')
        raport_item_1 = Stocuri2.objects.filter(counter=counter).order_by('code')

        
        #HEADER
        code_rind = [header.code_rind for header in raport_detail]
        indicatori = [header.indicatori for header in raport_detail]
        inceputul = [header.code_rind for header in raport_detail]
        finele = [header.finele for header in raport_detail]

        #ITEMS-1
        code_rind_2  = [item1.code_rind  for item1 in raport_item_1]
        indicatorii_2 = [item1.indicatorii for item1 in raport_item_1]
        trimestrul_2 = [item1.trimestrul for item1 in raport_item_1]

        header = [
            {
                'crt': 1,
                'code_rind': code_rind if code_rind else '',
                'indicatori': indicatori if indicatori else '',
                'inceputul': inceputul if inceputul else '',
                'finele': finele if finele else ''
            },
                        {
                'crt': 2,
                'code_rind': code_rind if code_rind else '',
                'indicatori': indicatori if indicatori else '',
                'inceputul': inceputul if inceputul else '',
                'finele': finele if finele else ''
            },
                        {
                'crt': 3,
                'code_rind': code_rind if code_rind else '',
                'indicatori': indicatori if indicatori else '',
                'inceputul': inceputul if inceputul else '',
                'finele': finele if finele else ''
            },
                        {
                'crt': 4,
                'code_rind': code_rind if code_rind else '',
                'indicatori': indicatori if indicatori else '',
                'inceputul': inceputul if inceputul else '',
                'finele': finele if finele else ''
            }
        ]

        items_row_1 = [
            {
                'crt': 1,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatorii': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
            {
                'crt': 2,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                        {
                'crt': 3,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                        {
                'crt': 4,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                        {
                'crt': 5,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                        {
                'crt': 6,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                        {
                'crt': 7,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
            {
                 'crt': 8,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                    {
                'crt': 9,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                    {
                'crt': 10,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                    {
                'crt': 11,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
            {         
                'crt': 12,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                        {
                'crt': 13,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
            {
                'crt': 14,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
            {
                'crt': 15,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
            {
                'crt': 16,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                        {
                'crt': 17,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                    {
                'crt': 18,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
            {
                'crt': 19,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                                {
                'crt': 20,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                        {
                 'crt': 21,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                                            {
                'crt': 22,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                    {
                'crt': 23,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
            {
                 'crt': 24,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                                {
                 'crt': 25,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                        {
                'crt': 26,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                    {
                'crt': 27,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                    {
                'crt': 28,
                'code_rind':code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
            {
                'crt': 29,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                                {
                'crt': 30,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
                                                {
                'crt': 31,
                'code_rind': code_rind_2 if code_rind_2 else '',
                'indicatori': indicatorii_2 if indicatorii_2 else '',
                'trimestrul': trimestrul_2 if trimestrul_2 else '',
            },
        ]

       
        sales_list = ManagerRaportStocuri.objects.filter(reports__uid=manager_inf_econ_op.reports.uid).order_by('reports__counter')

        # marfa_list = SecondInfEconOp.objects.filter(company__users__username=request.user).order_by('code')
        current_header = 0
        current_item_1 = 0


        for sales in raport_detail: 
            header[current_header]['code_rind'] = sales.code_rind
            header[current_header]['indicatori'] = sales.indicatori
            header[current_header]['inceputul'] = sales.inceputul
            header[current_header]['finele'] = sales.finele
            header[current_header]['code'] = sales.code
            current_header += 1

        for raport_item_1 in raport_item_1: 
            items_row_1[current_item_1]['code_rind'] = raport_item_1.code_rind
            items_row_1[current_item_1]['indicatori'] = raport_item_1.indicatorii
            items_row_1[current_item_1]['trimestrul'] = raport_item_1.trimestrul
            items_row_1[current_item_1]['code'] = raport_item_1.code
            current_item_1 += 1

        context = {'sales': sales, 'manager_inf_econ_op': manager_inf_econ_op, 'header': header, 'item_1': items_row_1}
        
        if request.user.is_superuser or check_user:
            return render(request, self.template_name, context)
        elif not check_user:
            return redirect('reports:reports')
        
        return render(request, self.template_name, context)
    
    def post(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerRaportStocuri.objects.get(uid=uid)

        counter_uid = manager_inf_econ_op.reports.counter



        rows = Stocuri1.objects.filter(counter=counter_uid).order_by('code')
        
        items_1 = Stocuri2.objects.filter(counter=counter_uid).order_by('code')

        #ITEMS - 1 -- POST
        code_rind = [request.POST.get(f'code_rind_{row.code}', None) for row in rows]
        indicatori_1 = [request.POST.get(f'indicatori_1_{row.code}', None) for row in rows]
        inceputul = [request.POST.get(f'inceputul_{row.code}', None) for row in rows]
        finele = [request.POST.get(f'finele_{row.code}', None) for row in rows]

        #ITEMS - 2 -- POST
        code_rind_1 = [request.POST.get(f'code_rind_1_{row.code}', None) for row in items_1]
        indicatorii_2 = [request.POST.get(f'indicatorii_2_{row.code}', None) for row in items_1]
        trimestrul = [request.POST.get(f'trimestrul_{row.code}', None) for row in items_1]

        print(indicatorii_2)


        counter = 0

        for i, row, in enumerate(rows):
            try:
                report_item_1 = Stocuri1.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.code_rind = float(code_rind[i]) if code_rind[i] else None
                    report_item_1.indicatori = str(indicatori_1[i]) if indicatori_1[i] else None
                    report_item_1.inceputul = float(inceputul[i]) if inceputul[i] else None
                    report_item_1.finele = float(finele[i]) if finele[i] else None
                    report_item_1.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except Stocuri1.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_1 = Stocuri1.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.code_rind = float(code_rind[i]) if code_rind[i] else None
                    report_item_1.indicatori = str(indicatori_1[i]) if indicatori_1[i] else None
                    report_item_1.inceputul = float(inceputul[i]) if inceputul[i] else None
                    report_item_1.finele = float(finele[i]) if finele[i] else None
                    report_item_1.save()
                    counter += 1
                    report_item_1.counter = counter
                    report_item_1.save() 
            except Exception as e:
                print(f"123Error while saving InfEconOp object with id {i+1}: {e}")




        #ITEMS - 1 -- POST
        for i, row, in enumerate(items_1):
            try:
                report_item_1 = Stocuri2.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.code_rind = float(code_rind_1[i]) if code_rind_1[i] else None
                    report_item_1.indicatorii = float(indicatorii_2[i]) if indicatorii_2[i] else None
                    print(report_item_1.indicatorii)
                    report_item_1.trimestrul = float(trimestrul[i]) if trimestrul[i] else None
                    report_item_1.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except Stocuri2.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_1 = Stocuri2.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.code_rind = float(code_rind_1[i]) if code_rind_1[i] else None
                    report_item_1.indicatorii = float(indicatorii_2[i]) if indicatorii_2[i] else None
                    print(report_item_1.indicatorii)
                    report_item_1.trimestrul = float(trimestrul[i]) if trimestrul[i] else None
                    report_item_1.save()
                    counter += 1
                    report_item_1.counter = counter
                    report_item_1.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")

        # print('POST Запрос',request.POST)
        # print(f"Number of InfEconOp objects saved: {counter}")  # выводим число сохраненных объектов
        return HttpResponseRedirect(request.path_info)