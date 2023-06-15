from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.db.models import Q
from itertools import chain
from reports.models import InfEconOp, SecondInfEconOp, ManagerInfEconOp, ManagerMiscCadrelor, ManagerReportDescriereaAsociati



class ReportsList(View):
    template_name = 'reports/all_reports.html'

    # @require_company_data
    def get(self, request, *args, **kwargs):
        # Запросы к каждой модели
        reports_inf_econ_op = ManagerInfEconOp.objects.all()
        reports_misc_cadrelor = ManagerMiscCadrelor.objects.all()
        reports_report_descrierea_asociati = ManagerReportDescriereaAsociati.objects.all()

        # Объединение результатов запросов
        reports = list(chain(reports_inf_econ_op, reports_misc_cadrelor, reports_report_descrierea_asociati))

        context = {'reports': reports}
        return render(request, self.template_name, context)
    


class ReportDetails(View):
    template_name = 'reports/reports/informatie_client.html'

    def get(self, request, *args, **kwargs):
        # Получаем значение counter из параметров запроса
        counter = kwargs.get('counter')
        
        reports = InfEconOp.objects.filter(counter=counter)
        s_marfas = SecondInfEconOp.objects.filter(counter=counter)

        before_total_list = [sale.n_beforeTotal for sale in reports]
        before_lunar_list = [sale.n_beforeLunar for sale in reports]
        n_total_list = [sale.n_total for sale in reports]
        n_lunar_list = [sale.n_lunar for sale in reports]
        codes = [sale.code for sale in reports]

        marfas = []  
        for i, marfa in enumerate(s_marfas):
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
                'before_total': before_total,
                'before_lunar': before_lunar,
                'n_total': n_total,
                'n_lunar': n_lunar,
                'n_beforeMarfa': n_beforeMarfa,
                'n_marfa': n_marfa,
            })
        print(marfas)
        rows = [    
            {
                'rowspan': 3,     
                'crt': 1,
                'description': 'Volumul de vînzări prin intermediul unităților de comerț, total',        
                'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''

                
            },
        {
            'description': 'inclusiv vînzări de produse alimentare',
            'unit_of_measure': '-//-',
            'before_total': before_total_list if before_total_list else '',
            'before_lunar': before_lunar_list if before_lunar_list else '',
            'n_total': n_total_list if n_total_list else '',
            'n_lunar': n_lunar_list if n_lunar_list else ''
        },
        {  
            'description': 'Stocuri de mărfuri',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
        {  
            'rowspan': 4,      
            'crt': 2,
            'description': 'Volumul de vînzări cu ridicata, prin intermediul bazelor angro',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
            'description': 'Stocuri de mărfuri',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
            'description': 'Volumul exportului',
            'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                {  
            'description': 'Volumul importului',
            'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''

        },
            {  
            'rowspan': 6,      
            'crt': 3,
            'description': 'Volumul de prestări servicii, total, dintre care:',
            'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
            'description': 'în alimentația publică, total',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
            'description': 'inclusiv producția proprie',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                {  
            'description': 'servicii de piață',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                    {  
            'description': 'servicii de locațiune și păstrare',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                    {  
            'description': 'alte servicii',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                {  
            'rowspan': 5,      
            'crt': 4,
            'description': 'Volumul de prestări servicii, total, dintre care:',
            'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
            'description': 'în alimentația publică, total',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
            'description': 'inclusiv producția proprie',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                {  
            'description': 'servicii de locațiune și păstrare',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                    {  
            'description': 'alte servicii',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
                    {  
            'rowspan': 2,      
            'crt': 5,
            'description': 'Volumul de prestări servicii, total, dintre care:',
            'unit_of_measure': 'mii lei',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
            {  
            'description': 'în alimentația publică, total',
            'unit_of_measure': '-//-',
                'before_total': before_total_list if before_total_list else '',
                'before_lunar': before_lunar_list if before_lunar_list else '',
                'n_total': n_total_list if n_total_list else '',
                'n_lunar': n_lunar_list if n_lunar_list else ''
        },
    ]     
        
        current_row = 0
        current_marfa = 0

        for s_marfas in s_marfas:
            marfas[current_marfa]['name'] = s_marfas.name
            marfas[current_marfa]['before_total'] = s_marfas.n_beforeTotal
            marfas[current_marfa]['before_lunar'] = s_marfas.n_beforeLunar
            marfas[current_marfa]['n_total'] = s_marfas.n_total
            marfas[current_marfa]['n_lunar'] = s_marfas.n_lunar
            marfas[current_marfa]['n_beforeMarfa'] = s_marfas.n_beforeMarfa
            marfas[current_marfa]['n_marfa'] = s_marfas.n_Marfa
            marfas[current_marfa]['code'] = s_marfas.code
            current_marfa += 1  # увеличиваем текущий номер ячейки на 1

        for sales in reports:
            rows[current_row]['before_total'] = sales.n_beforeTotal
            rows[current_row]['before_lunar'] = sales.n_beforeLunar
            rows[current_row]['n_total'] = sales.n_total
            rows[current_row]['n_lunar'] = sales.n_lunar
            rows[current_row]['code'] = sales.code
            current_row += 1  # увеличиваем текущий номер ячейки на 1

        context = {'reports': reports, 'rows': rows, 'marfas': marfas}
        return render(request, self.template_name, context)