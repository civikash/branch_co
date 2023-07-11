from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View
from django.db.models import Max
from reports.models import InfEconOp, SecondInfEconOp, ManagerInfEconOp
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class ReportsAdds(View):
    template_name = 'reports/reports/informatie_client.html'
    user = None


    def get(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerInfEconOp.objects.filter(uid=uid).first()
        check_user = ManagerInfEconOp.objects.filter(reports__company=request.user.company)
        
        counter = manager_inf_econ_op.reports.counter
        sales = ManagerInfEconOp.objects.filter(reports__uid=manager_inf_econ_op.uid).order_by('reports__code')

        s_marfas = SecondInfEconOp.objects.filter(company__users__username=request.user).order_by('code')

        raport_detail = InfEconOp.objects.filter(counter=counter).order_by('code')
        raport_second_part = SecondInfEconOp.objects.filter(counter=counter).order_by('code')
        
        years = InfEconOp.objects.filter(counter=counter).first()
        print('YEARS: ', years)
        econ_years = SecondInfEconOp.objects.filter(company__users__username=request.user).first()

        n_year = [sale.n_year for sale in raport_detail]
        before_total_list = [sale.n_beforeTotal for sale in raport_detail]
        before_lunar_list = [sale.n_beforeLunar for sale in raport_detail]
        n_total_list = [sale.n_total for sale in raport_detail]
        n_lunar_list = [sale.n_lunar for sale in raport_detail]
        codes = [sale.code for sale in raport_detail]
        marfas = []     

        for i, marfa in enumerate(raport_second_part):
            crt = i + 1
            name = marfa.name
            before_total = marfa.n_beforeTotal
            before_lunar = marfa.n_beforeLunar
            n_total = marfa.n_total
            n_lunar = marfa.n_lunar
            n_beforeMarfa = marfa.n_beforeMarfa
            n_marfa = marfa.n_Marfa

            marfas.append({
                'crt': crt,
                'name': name,
                'year': n_year,
                'before_total': before_total,
                'before_lunar': before_lunar,
                'n_total': n_total,
                'n_lunar': n_lunar,
                'n_beforeMarfa': n_beforeMarfa,
                'n_marfa': n_marfa,
            })
        rows = [    
            {
                'rowspan': 6,     
                'crt': 1,
                'year': n_year,
                'description': 'Volumul de vínzări prin intermediul unităților de comerț, total, inclusiv:',        
                'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''

                
            },
        {
            'description': 'cu amănuntul populației',
            'unit_of_measure': '-//-',
            'year': n_year,
            'before_total': before_total_list if before_total_list else '',
            'before_lunar': before_lunar_list if before_lunar_list else '',
            'n_total': n_total_list if n_total_list else '',
            'n_lunar': n_lunar_list if n_lunar_list else ''
        },
        {   'year': n_year,
            'description': 'prin virament către instuțiile bugetare',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
        {  
            'year': n_year,
            'description': 'Altele',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
            'year': n_year,
            'description': 'inclusiv vinzări de produse alimentare',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            { 
            'year': n_year, 
            'description': 'Stocuri de mărfuri',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                {  
                'year': n_year,
            'rowspan': 2,     
            'crt': 2,
            'description': 'Volumul de vînzări cu ridicata, prin intermediul bazelor angro',
            'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''

        },
            {  
                'year': n_year,
            'description': 'Stocuri de marfuri',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
                'year': years,
            'rowspan': 1,      
            'crt': 3,
            'description': 'Volumul de prestări servicii, total, dintre care:',
            'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
                'year': n_year,
            'rowspan': 4,      
            'crt': 4,
            'description': 'în alimentația publică, total',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                {  
                    'year': n_year,
            'description': 'inclusiv producția proprie',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                    {  
                        'year': n_year,
            'description': 'servicii de locațiune şi păstrare',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                    {  
                        'year': n_year,
            'description': 'alte servicii',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                {  
                    'year': n_year,
            'rowspan': 4,      
            'crt': 4,
            'description': 'Volumul producției industriale, inclusiv:',
            'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
                'year': n_year,
            'description': 'píine şi produse de panificație',
            'unit_of_measure': 'tone',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
                'year': n_year,
            'description': 'produse de cofetărie',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                {  
                    'year': n_year,
            'description': 'Altele',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                    {  
                        'year': n_year,
            'rowspan': 2,      
            'crt': 5,
            'description': 'Volumul de preluare a produselor agricole, materiilor prime zootehnice şi de altă natură, total',
            'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                    {  
                        'year': n_year,
            'description': 'inclusiv de la populație',
            'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
    ]     
          
       
        sales_list = ManagerInfEconOp.objects.filter(reports__uid=manager_inf_econ_op.reports.uid).order_by('reports__counter')

        marfa_list = SecondInfEconOp.objects.filter(company__users__username=request.user).order_by('code')
        current_row = 0
        current_marfa = 0

        for marfas_i in raport_second_part:
            marfas[current_row]['n_month'] = marfas_i.n_month
            marfas[current_row]['n_year'] = marfas_i.n_year
            marfas[current_marfa]['name'] = marfas_i.name
            marfas[current_marfa]['before_total'] = marfas_i.n_beforeTotal
            marfas[current_marfa]['before_lunar'] = marfas_i.n_beforeLunar
            marfas[current_marfa]['n_total'] = marfas_i.n_total
            marfas[current_marfa]['n_lunar'] = marfas_i.n_lunar
            marfas[current_marfa]['n_beforeMarfa'] = marfas_i.n_beforeMarfa
            marfas[current_marfa]['n_marfa'] = marfas_i.n_Marfa
            marfas[current_marfa]['code'] = marfas_i.code
            current_marfa += 1  # увеличиваем текущий номер ячейки на 1


        for sales in raport_detail: 
            rows[current_row]['n_year'] = sales.n_year
            rows[current_row]['n_month'] = sales.n_month
            rows[current_row]['before_total'] = sales.n_beforeTotal
            rows[current_row]['before_lunar'] = sales.n_beforeLunar
            rows[current_row]['n_total'] = sales.n_total
            rows[current_row]['n_lunar'] = sales.n_lunar
            rows[current_row]['code'] = sales.code
            current_row += 1  # увеличиваем текущий номер
        context = {'sales': sales, 'econ_years':econ_years, 'manager_inf_econ_op': manager_inf_econ_op, 'years':years, 's_marfas':s_marfas, 'rows': rows, 'marfas': marfas}
        
        if request.user.is_superuser or check_user:
            return render(request, self.template_name, context)
        elif not check_user:
            return redirect('reports:reports')
        
        return render(request, self.template_name, context)
    
    def post(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerInfEconOp.objects.get(uid=uid)

        counter_uid = manager_inf_econ_op.reports.counter

        sales = ManagerInfEconOp.objects.filter(reports__uid=manager_inf_econ_op.uid)
        raport_detail = InfEconOp.objects.filter(counter=counter_uid)

        rows = InfEconOp.objects.filter(counter=counter_uid).order_by('code')
        marfas = SecondInfEconOp.objects.filter(company__users__username=request.user).order_by('code')

        n_month = request.POST.get('n_month')
        n_year = request.POST.get('n_year')
        before_totals = [request.POST.get(f'before_total_{row.code}', None) for row in rows]
        before_lunar = [request.POST.get(f'before_lunar_{row.code}', None) for row in rows]
        n_total = [request.POST.get(f'n_total_{row.code}', None) for row in rows]
        n_lunar = [request.POST.get(f'n_lunar_{row.code}', None) for row in rows]

        # print('POST METHOD ---- -- --- - N_M, N_Y, B_T. B_L, N_T, N_L', n_month, before_lunar, before_totals, n_total, n_lunar)


        n_month_econ = request.POST.get('n_month_econ')
        n_year_econ = request.POST.get('n_year_econ')
        sec_name = [request.POST.get(f'name_{marfa.code}', None) for marfa in marfas]
        sec_before_totals = [request.POST.get(f'sec_before_total_{marfa.code}', None) for marfa in marfas]
        sec_before_lunar = [request.POST.get(f'sec_before_lunar_{marfa.code}', None) for marfa in marfas]
        sec_n_total = [request.POST.get(f'sec_n_total_{marfa.code}', None) for marfa in marfas]
        sec_n_lunar = [request.POST.get(f'sec_n_lunar_{marfa.code}', None) for marfa in marfas]
        sec_n_beforeMarfa = [request.POST.get(f'sec_n_beforeMarfa_{marfa.code}', None) for marfa in marfas]
        sec_n_Marfa = [request.POST.get(f'sec_n_Marfa_{marfa.code}', None) for marfa in marfas]


        new_sec_names = request.POST.getlist('new_name_')
        print('NEW_ROW', new_sec_names)
        new_sec_before_totals = request.POST.getlist('new_sec_before_total_')
        new_sec_before_lunars = request.POST.getlist('new_sec_before_lunar_')
        new_sec_n_totals = request.POST.getlist('new_sec_n_total_')
        new_sec_n_lunars = request.POST.getlist('new_sec_n_lunar_')
        new_sec_n_beforeMarfas = request.POST.getlist('new_sec_n_beforeMarfa_')
        new_sec_n_Marfas = request.POST.getlist('new_sec_n_Marfa_')
        counter = 0  # добавляем и инициализируем счетчик
        for i, row, in enumerate(rows):
            try:
                inf_econ_op = InfEconOp.objects.filter(counter=counter_uid, code=row.code).first()
                if inf_econ_op is not None:
                    inf_econ_op.n_month = int(n_month) if n_month else None
                    inf_econ_op.n_year = int(n_year) if n_year else None
                    print('N MONTH, N_YEAR', inf_econ_op.n_month, inf_econ_op.n_year)
                    inf_econ_op.n_beforeTotal = float(before_totals[i]) if before_totals[i] else None
                    inf_econ_op.n_beforeLunar = float(before_lunar[i]) if before_lunar[i] else None
                    inf_econ_op.n_total = float(n_total[i]) if n_total[i] else None
                    inf_econ_op.n_lunar = float(n_lunar[i]) if n_lunar[i] else None
                    inf_econ_op.save()
                     # увеличиваем счетчик на 1 при успешном сохранении объекта
            except InfEconOp.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                inf_econ_op = InfEconOp.objects.filter(counter=counter_uid, code=row.code).first()
                if inf_econ_op is not None:
                    inf_econ_op.n_month = int(n_month) if n_month else None
                    inf_econ_op.n_year = int(n_year) if n_year else None
                    inf_econ_op.n_beforeTotal = float(before_totals[i]) if before_totals[i] else None
                    inf_econ_op.n_beforeLunar = float(before_lunar[i]) if before_lunar[i] else None
                    inf_econ_op.n_total = float(n_total[i]) if n_total[i] else None
                    inf_econ_op.n_lunar = float(n_lunar[i]) if n_lunar[i] else None
                    inf_econ_op.save()
                    counter += 1
                    inf_econ_op.counter = counter
                    inf_econ_op.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")

        for i, marfa, in enumerate(marfas):
            try:
                sec_inf_econ_op = SecondInfEconOp.objects.filter(company__users__username=request.user, code=marfa.code).first()
                if sec_inf_econ_op is not None:
                    if n_month_econ or n_year_econ or sec_name[i] or sec_before_totals[i] or sec_before_lunar[i] or sec_n_total[i] or sec_n_lunar[i] or sec_n_beforeMarfa[i] or sec_n_Marfa[i]:
                        sec_inf_econ_op.n_month = float(n_month_econ) if n_month_econ else None
                        sec_inf_econ_op.n_year = float(n_year_econ) if n_year_econ else None
                        sec_inf_econ_op.name = str(sec_name[i]) if sec_name[i] else None
                        sec_inf_econ_op.n_beforeTotal = float(sec_before_totals[i]) if sec_before_totals[i] else None
                        sec_inf_econ_op.n_beforeLunar = float(sec_before_lunar[i]) if sec_before_lunar[i] else None
                        sec_inf_econ_op.n_total = float(sec_n_total[i]) if sec_n_total[i] else None
                        sec_inf_econ_op.n_lunar = float(sec_n_lunar[i]) if sec_n_lunar[i] else None
                        sec_inf_econ_op.n_beforeMarfa = float(sec_n_beforeMarfa[i]) if sec_n_beforeMarfa[i] else None
                        sec_inf_econ_op.n_Marfa = float(sec_n_Marfa[i]) if sec_n_Marfa[i] else None
                        sec_inf_econ_op.counter = counter_uid
                        sec_inf_econ_op.save()
                     # увеличиваем счетчик на 1 при успешном сохранении объекта
            except SecondInfEconOp.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                sec_inf_econ_op = SecondInfEconOp.objects.filter(company__users__username=request.user, code=marfa.code).first()
                if sec_inf_econ_op is not None:
                    if n_month_econ or n_year_econ or sec_name[i] or sec_before_totals[i] or sec_before_lunar[i] or sec_n_total[i] or sec_n_lunar[i] or sec_n_beforeMarfa[i] or sec_n_Marfa[i]:
                        sec_inf_econ_op.n_month = float(n_month_econ) if n_month_econ else None
                        sec_inf_econ_op.n_year = float(n_year_econ) if n_year_econ else None
                        sec_inf_econ_op.name = str(sec_name[i]) if sec_name[i] else None
                        sec_inf_econ_op.n_beforeTotal = float(sec_before_totals[i]) if sec_before_totals[i] else None
                        sec_inf_econ_op.n_beforeLunar = float(sec_before_lunar[i]) if sec_before_lunar[i] else None
                        sec_inf_econ_op.n_total = float(sec_n_total[i]) if sec_n_total[i] else None
                        sec_inf_econ_op.n_lunar = float(sec_n_lunar[i]) if sec_n_lunar[i] else None
                        sec_inf_econ_op.n_beforeMarfa = float(sec_n_beforeMarfa[i]) if sec_n_beforeMarfa[i] else None
                        sec_inf_econ_op.n_Marfa = float(sec_n_Marfa[i]) if sec_n_Marfa[i] else None
                        sec_inf_econ_op.counter = counter_uid
                        sec_inf_econ_op.save()
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")
        try:
            for i in range(len(new_sec_names)):
                    new_sec_inf_econ_op = SecondInfEconOp.objects.create(company=request.user.company)
                    if new_sec_inf_econ_op is not None:
                        if n_year_econ or new_sec_names[i] or new_sec_before_totals[i] or new_sec_before_lunars[i] or new_sec_n_totals[i] or new_sec_n_lunars[i] or new_sec_n_beforeMarfas[i] or new_sec_n_Marfas[i]:
                            new_sec_inf_econ_op.n_year = float(n_year_econ) if n_year_econ else None
                            new_sec_inf_econ_op.name = str(new_sec_names[i]) if new_sec_names[i] else None
                            new_sec_inf_econ_op.n_beforeTotal = float(new_sec_before_totals[i]) if new_sec_before_totals[i] else None
                            new_sec_inf_econ_op.n_beforeLunar = float(new_sec_before_lunars[i]) if new_sec_before_lunars[i] else None
                            new_sec_inf_econ_op.n_total = float(new_sec_n_totals[i]) if new_sec_n_totals[i] else None
                            new_sec_inf_econ_op.n_lunar = float(new_sec_n_lunars[i]) if new_sec_n_lunars[i] else None
                            new_sec_inf_econ_op.n_beforeMarfa = float(new_sec_n_beforeMarfas[i]) if new_sec_n_beforeMarfas[i] else None
                            new_sec_inf_econ_op.n_Marfa = float(new_sec_n_Marfas[i]) if new_sec_n_Marfas[i] else None
                            new_sec_inf_econ_op.counter = counter_uid
                            new_sec_inf_econ_op.save()
                            print(new_sec_inf_econ_op)
        except Exception as e:
            print(f"Error while creating new SecondInfEconOp object: {e}")
            raise
        # print('POST Запрос',request.POST)
        # print(f"Number of InfEconOp objects saved: {counter}")  # выводим число сохраненных объектов
        return HttpResponseRedirect(request.path_info)



