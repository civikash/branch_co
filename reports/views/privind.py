from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.db.models import Max
from django.http import HttpResponseRedirect
from reports.models import ManagerReportDescriereaAsociati, ReportHeader, ReportItems1, ReportItems2, ReportItems3


class PrivindListView(View):
    template_name = 'reports/reports/privind/privind_list.html'

    def dispatch(self, request, *args, **kwargs):
        rows = ReportHeader.objects.filter(
            company__users__username=request.user).order_by('code')
        item_1 = ReportItems1.objects.filter(
            company__users__username=request.user).order_by('code')
        item_2 = ReportItems2.objects.filter(
            company__users__username=request.user).order_by('code')
        item_3 = ReportItems3.objects.filter(
            company__users__username=request.user).order_by('code')

        # получить максимальный код, если такие объекты уже существуют
        max_code = rows.last().code if rows.exists() else 0
        max_counter = ReportHeader.objects.aggregate(
            Max('counter'))['counter__max'] or 0
        
        max_code_item_1 = item_1.last().code if item_1.exists() else 0
        max_counter_1 = ReportItems1.objects.aggregate(
            Max('counter'))['counter__max'] or 0
        
        max_code_item_2 = item_2.last().code if item_2.exists() else 0
        max_counter_2 = ReportItems2.objects.aggregate(
            Max('counter'))['counter__max'] or 0
        
        max_code_item_3 = item_3.last().code if item_3.exists() else 0
        max_counter_3 = ReportItems3.objects.aggregate(
            Max('counter'))['counter__max'] or 0

        # HEADER создать новые объекты с одинаковым значением counter, начиная с max_counter + 1
        num_new_objs = 17 - len(rows)
        next_counter = max_counter + 1 if num_new_objs > 0 else max_counter + 1  # Определение значения next_counter

        # ITEM_1
        item_new_objs_1 = 32 - len(item_1)
        next_counter_item_1 = max_counter_1 + 1 if item_new_objs_1 > 0 else max_counter_1 + 1  # Определение значения next_counter

        # ITEM_2
        item_new_objs_2 = 21 - len(item_2)
        next_counter_item_2 = max_counter_2 + 1 if item_new_objs_2 > 0 else max_counter_2 + 1  # Определение значения next_counter

        # ITEM_3
        item_new_objs_3 = 29 - len(item_3)
        next_counter_item_3 = max_counter_3 + 1 if item_new_objs_3 > 0 else max_counter_3 + 1  # Определение значения next_counter

        # Проверка метода запроса
        if request.method == 'POST':
            # Создание первого объекта InfEconOp с заполненными полями company и counter
            inf_econ_op = ReportHeader.objects.create(
                company=request.user.company, counter=next_counter)
            
            item_post_1 = ReportItems1.objects.create(
                company=request.user.company, counter=next_counter_item_1)
            
            item_post_2 = ReportItems2.objects.create(
                company=request.user.company, counter=next_counter_item_2)
            
            item_post_3 = ReportItems3.objects.create(
                company=request.user.company, counter=next_counter_item_3)

            # Создание остальных объектов InfEconOp с увеличенным значением counter
            for i in range(16):
                ReportHeader.objects.create(
                    company=request.user.company, counter=next_counter)
            
            for i in range(31):
                ReportItems1.objects.create(
                    company=request.user.company, counter=next_counter_item_1)
                

            for i in range(20):
                ReportItems2.objects.create(
                    company=request.user.company, counter=next_counter_item_2)
                
            for i in range(28):
                ReportItems3.objects.create(
                    company=request.user.company, counter=next_counter_item_3)

            # Создание объекта ManagerInfEconOp и связывание с InfEconOp
            manager_inf_econ_op = ManagerReportDescriereaAsociati.objects.create(
                reports=inf_econ_op, report_item_1=item_post_1, report_item_2=item_post_2, report_item_3=item_post_3)

            # Перенаправление на страницу, где будет отображен созданный объект
            return redirect('reports:privind-detail', uid=manager_inf_econ_op.uid)

        # Если метод запроса не POST, вызываем метод dispatch родительского класса
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        reports_user = ManagerReportDescriereaAsociati.objects.filter(reports__company=request.user.company)
        context = {'reports': reports_user}
        return render(request, self.template_name, context)


class PrivindDetail(View):
    template_name = 'reports/reports/privind/privind_detail.html'
    user = None


    def get(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerReportDescriereaAsociati.objects.filter(uid=uid).first()
        print(manager_inf_econ_op)
        if not manager_inf_econ_op:
            return request("Отчет не найден")
        
        counter = manager_inf_econ_op.reports.counter
        sales = ManagerReportDescriereaAsociati.objects.filter(reports__uid=manager_inf_econ_op.uid).order_by('reports__code')

        items_1 = ReportItems1.objects.filter(company__users__username=request.user).order_by('code')
        items_2 = ReportItems2.objects.filter(company__users__username=request.user).order_by('code')
        items_3 = ReportItems3.objects.filter(company__users__username=request.user).order_by('code')

        raport_detail = ReportHeader.objects.filter(counter=counter).order_by('code')

        raport_item_1 = ReportItems1.objects.filter(counter=counter).order_by('code')
        raport_item_2 = ReportItems2.objects.filter(counter=counter).order_by('code')
        raport_item_3 = ReportItems3.objects.filter(counter=counter).order_by('code')
        
        #HEADER
        associat = [header.associat for header in raport_detail]
        fondul = [header.fondul for header in raport_detail]

        #ITEMS-1
        prejud = [item1.prejud for item1 in raport_item_1]
        sup_10 = [item1.sup_10 for item1 in raport_item_1]

        #ITEMS-2 
        d_t_ini = [item2.d_t_ini for item2 in raport_item_2]
        c_t_ini = [item2.c_t_fin for item2 in raport_item_2]
        calculat = [item2.calculat for item2 in raport_item_2]
        transferat = [item2.transferat for item2 in raport_item_2]
        d_t_fin = [item2.d_t_fin for item2 in raport_item_2]
        c_t_fin = [item2.c_t_fin for item2 in raport_item_2]

        #ITEMS-3
        n_year = [item3.n_year for item3 in raport_item_3]
        n_1_year = [item3.n_1_year for item3 in raport_item_3]
        perc = [item3.perc for item3 in raport_item_3]

        header = [
            {
                'crt': 1,
                'descrierea': 'Membri cooperatori la 01.01.2023 Пайщики на 01.01.2023',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                        {
                'crt': 2,
                'descrierea': 'Membri cooperatori nou-atrași în a. 2023 (persoane) Вновь кооперировано в 2023 (чел)',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                        {
                'crt': 3,
                'descrierea': 'Întrări în perioada anului 2023 - transferări sau fuzionarea organizațiilor cooperatiste (persoane) Поступило за 2023– в порядке перехода или слияния организации (чел) ',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                        {
                'crt': 4,
                'descrierea': 'Ieșiri pe perioada a. 2023 pe diverse motive (persoane) Выбыло за 2023 по разным причинам (чел)',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                        {
                'crt': 5,
                'descrierea': 'Membri cooperatori la 31.12.2023 (persoane) Пайщики на 31.12.2023 (чел)',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                        {
                'crt': 6,
                'descrierea': 'Soldul părților sociale la 01.01.2023 (lei) – total Остаток на 01.01.2023 (лей) – всего',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                        {
                'crt': 7,
                'rowspan': 4,
                'descrierea': 'Încasări pentru sporire total: Поступило на увеличение всего:',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
            {
                'descrierea': 'Inclusiv: ( втч:)',
                'associat': '-',
                'fondul': '-'
            },
                                    {
                'descrierea': '- părți sociale (паевых взносов)',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                                    {
                'descrierea': '- de la alte organizații (от других организаций)',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                                    {
                'crt': 8,
                'rowspan': 5,
                'descrierea': 'Casări la diminuare-total Списано на уменшение – всего inclusiv (втч): -Virate altor întreprinderi (перечислено другим предприятиям) - Rambursarea părților sociale (возвращено паевых взносов) - Trecute în fondul statutar (зачислены в уставный фонд) - Alte casări (другие списания)',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
            {         
                'descrierea': 'Null',                     
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                                                {
                                                    'descrierea': 'Null', 
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                                                {
                                                    'descrierea': 'Null', 
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                                                {
                                                    'descrierea': 'Null', 
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                                    {
                'crt': 9,
                'descrierea': 'Soldul părților sociale la 31.12.2023 (lei) Остаток на 31.12.2023',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
                        {
                'crt': 10,
                'descrierea': 'Urmează a fi achitate părți sociale pentru completarea integrală a sumei stabilită de statut (Подлежит внесению до полной суммы установленной уставом) ',
                'associat': associat if associat else '',
                'fondul': fondul if fondul else ''
            },
        ]

        items_row_1 = [
            {
                'crt': 1,
                'descrierea': 'Soldul la 01.01.2023 Остаток на 01.01.2023',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
            {
                'descrierea': 'Depistate în a. 2023  (Выявлено в 2023)',
                'rowcolumn': 4,
            },
            {
                'crt': 2,
                'descrierea': 'Numărul de cazuri  (Количество случаев) ',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                        {
                'crt': 3,
                'rowspan': 3,
                'descrierea': 'Suma  (Сумма)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                        {
                'descrierea': 'inclusiv: (в.т.ч): - Mărfuri și materiale (товары и материалы)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                        {
                'descrierea': '- Mijloace bănești (денежные средства)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                        {
                'crt': 4,
                'descrierea': 'Transferat de pe alte conturi (переведено с других счетов)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                        {
                'crt': 5,
                'rowspan': 2,
                'descrierea': 'Încasat total (погашено всего)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
            {
                'descrierea': 'Inclusiv:(в.т.ч): *De la companiile de asigurări (oт страховых  компаний)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                    {
                'crt': 6,
                'rowspan': 2,
                'descrierea': 'Casate: (Списанны)-   total (всего)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                    {
                'descrierea': 'Inclusiv:(в.т.ч):  - la pierderile operaționale (операционые расходы) - din alte surse (из других источников)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                    {
                'crt': 7,
                'rowspan': 2,
                'descrierea': 'Soldul la 31.12.2023 – total (Остаток на 31.12.2023- всего)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
            {         
                'descrierea': 'Inclusiv:( втч:)  - aflate spre examinare în instanța de  judecată (переданы в суд ) ',                     
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                        {
                'descrierea': 'Circulația datoriilor formate de la furturi (Оборот долгов по кражам) ',
                'rowcolumn': 4,
            },
            {
                'crt': 1,
                'descrierea': 'Soldul la 01.01.2023 (Остаток на 01.01.2023)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
            {
                'descrierea': 'Depistate în a. 2023  (Выявлено в 2023)', 
                'rowcolumn': 4
            },
            {
                'crt': 2,
                'descrierea': 'Numărul de cazuri  (Количество случаев) ',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                        {
                'crt': 3,
                'descrierea': 'Suma  (Сумма)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                    {
                'crt': 4,
                'rowspan': 2,
                'descrierea': 'Încasat total (погашено всего)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
            {
                'descrierea': 'Inclusiv:(в.т.ч): din cele depistate în a. 2023 (из выявленных в 2023 г)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                                {
                'crt': 5,
                'rowspan': 2,
                'descrierea': 'Casate: (Списанны)-total (всего)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                        {
                'descrierea': 'Inclusiv:(в.т.ч): - la pierderile operaționale (операционные расходы) - din alte surse (из других источников)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                                            {
                'crt': 6,
                'descrierea': 'Soldul la 31.12.2023– total (Остаток на 31.12.2023 - всего)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                    {
                'descrierea': 'Pierderi în urma incendiilor (Потери от пожаров)',
                'rowcolumn': 4,
            },
            {
                'crt': 1,
                'descrierea': 'Soldul la 01.01.2023 (Остаток на 01.01.2023)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                                {
                'descrierea': 'Depistate în a. 2023  (Выявлено в 2023)',
                'rowcolumn': 4,
            },
                        {
                'crt': 2,
                'descrierea': 'Numărul de cazuri  (Количество случаев)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                    {
                'crt': 3,
                'descrierea': 'Suma  (Сумма)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                    {
                'crt': 4,
                'rowspan': 2,
                'descrierea': 'Încasat total (погашено всего)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
            {
                'descrierea': 'Inclusiv:(в.т.ч):*De la companiile de asigurări (oт страховых  компаний)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                                {
                'crt': 5,
                'descrierea': 'Casate: (Списанны)-   total (всего)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
                                                {
                'crt': 6,
                'descrierea': 'Soldul la 31.12.2023 – total (Остаток на 31.12.2023– всего)',
                'prejud': prejud if prejud else '',
                'sup_10': sup_10 if sup_10 else ''
            },
        ]

        items_row_2 = [
            {
                'taxele': 'Impozitul din salariu',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Impozitul din alte surse de plată',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Impozitul din activitate',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Impozitul din activitate',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Impozitul pe bunurile imobiliare',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'TVA',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Accize',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Taxa amenajarea teritoriului',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Taxa pentru unitățile comerciale',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Taxa de piață',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Taxa pentru folosirea drumurilor',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Alte taxe și impozite',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Total impozite și taxe',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'descrierea': 'Contribuțiile de asigurări sociale',
                'rowcolumn': 7,
            },
            {
                'rowspan': 2,
                'taxele': 'Contribuții sociale 24,0 %',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Total',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'descrierea': 'Contribuțiile asigurărilor medicale',
                'rowcolumn': 7,
            },
            {
                'taxele': 'Contribuții medicale (9%)',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Total bugetul public',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            },
            {
                'taxele': 'Amenzi',
                'd_t_ini': d_t_ini if d_t_ini else '',
                'c_t_ini': c_t_ini if c_t_ini else '',
                'calculat': calculat if calculat else '',
                'transferat': transferat if transferat else '',
                'd_t_fin': d_t_fin if d_t_fin else '',
                'c_t_fin': c_t_fin if c_t_fin else ''
            }
        ]   
        items_row_3 = [
            {
                'crt': 1,
                'denumirea': 'Impozitul din salariu',
                'um': 'mii. lei',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 2,
                'denumirea': 'Volumul serviciilor - totale',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 3,
                'denumirea': 'Volumul producției industriale',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 4,
                'denumirea': 'Volumul achizițiilor producției agricole',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 5,
                'denumirea': 'Total imobilizări corporale (130)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 6,
                'denumirea': 'Total active circulante (420), inclusiv:',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 7,
                'rowspan': 7,
                'denumirea': 'Mijloace circulante proprii (620-230)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': 'Stocuri (290)',
                'um': '',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': 'Creante curente și alte active circulante- total (370)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': 'inclusiv-creanțe comerciale (300)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': '- creanțe ale bugetului-(320)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': '-creanțe ale personalului (330)',
                'um': '',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': '-alte creante curente (340)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 8,
                'rowspan': 7,
                'denumirea': 'Datorii de achitat-totale (700+820)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': 'Incl. Credite bancare (630+710)',
                'um': '--',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': 'Imprumuturi banesti (640+720)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': 'Datorii comerciale (730)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': 'Datorii față de personal (760)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': 'Datorii privind asigurarile (770)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': 'Datorii față de buget (780)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 9,
                'rowspan': 2,
                'denumirea': 'Reziultatul  financiar (r. 180 din F. 2)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'denumirea': 'Incl. activitate operationala (r. 080-F. 2)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 10,
                'denumirea': 'Din alte activități (150 - F. 2)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 11,
                'denumirea': 'Venituri din vinzari (010 – F. 2)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 12,
                'denumirea': 'Consumuri(020 – F.2)',
                'um': '',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 13,
                'denumirea': 'Alte venituri operationale (040 - F.2)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 14,
                'denumirea': 'Celtuieli(050+060+070 F. 2)',
                'um': '-/-',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 15,
                'denumirea': 'Numarul mediu scriptic',
                'um': 'persoane',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
            {
                'crt': 16,
                'denumirea': 'Salariul mediu',
                'um': 'lei',
                'n_year': n_year if n_year else '',
                'n_1_year': n_1_year if n_1_year else '',
                'perc': perc if perc else '',
            },
        ]   
       
        sales_list = ManagerReportDescriereaAsociati.objects.filter(reports__uid=manager_inf_econ_op.reports.uid).order_by('reports__counter')

        # marfa_list = SecondInfEconOp.objects.filter(company__users__username=request.user).order_by('code')
        current_header = 0
        current_item_1 = 0
        current_item_2 = 0
        current_item_3 = 0


        for sales in raport_detail: 
             header[current_header]['associat'] = sales.associat
             header[current_header]['fondul'] = sales.fondul
             header[current_header]['code'] = sales.code
             current_header += 1

        for sales in raport_item_1: 
             items_row_1[current_item_1]['prejud'] = sales.prejud
             items_row_1[current_item_1]['sup_10'] = sales.sup_10
             items_row_1[current_item_1]['code'] = sales.code
             current_item_1 += 1

        for sales in raport_item_2: 
             items_row_2[current_item_2]['d_t_ini'] = sales.d_t_ini
             items_row_2[current_item_2]['c_t_ini'] = sales.c_t_ini
             items_row_2[current_item_2]['calculat'] = sales.calculat
             items_row_2[current_item_2]['transferat'] = sales.transferat
             items_row_2[current_item_2]['d_t_fin'] = sales.d_t_fin
             items_row_2[current_item_2]['c_t_fin'] = sales.c_t_fin
             items_row_2[current_item_2]['code'] = sales.code
             current_item_2 += 1

        for sales in raport_item_3: 
             items_row_3[current_item_3]['n_year'] = sales.n_year
             items_row_3[current_item_3]['n_1_year'] = sales.n_1_year
             items_row_3[current_item_3]['perc'] = sales.perc
             items_row_3[current_item_3]['code'] = sales.code
             current_item_3 += 1
        context = {'sales': sales, 'manager_inf_econ_op': manager_inf_econ_op, 'header': header, 'item_1': items_row_1, 'item_2': items_row_2, 'item_3': items_row_3}
        return render(request, self.template_name, context)
    
    def post(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerReportDescriereaAsociati.objects.get(uid=uid)

        counter_uid = manager_inf_econ_op.reports.counter



        rows = ReportHeader.objects.filter(counter=counter_uid).order_by('code')
        
        items_1 = ReportItems1.objects.filter(counter=counter_uid).order_by('code')
        items_2 = ReportItems2.objects.filter(counter=counter_uid).order_by('code')
        items_3 = ReportItems3.objects.filter(counter=counter_uid).order_by('code')


        #ITEMS - 1 -- POST
        prejud = [request.POST.get(f'prejud_{row.code}', None) for row in items_1]
        sup_10 = [request.POST.get(f'sup_10_{row.code}', None) for row in items_1]

        #ITEMS - 2 -- POST
        d_t_ini = [request.POST.get(f'd_t_ini_{row.code}', None) for row in items_2]
        c_t_ini = [request.POST.get(f'c_t_ini_{row.code}', None) for row in items_2]
        calculat = [request.POST.get(f'calculat_{row.code}', None) for row in items_2]
        transferat = [request.POST.get(f'transferat_{row.code}', None) for row in items_2]
        d_t_fin = [request.POST.get(f'd_t_fin_{row.code}', None) for row in items_2]
        c_t_fin = [request.POST.get(f'c_t_fin_{row.code}', None) for row in items_2]

        #ITEMS - 3 -- POST
        n_year = [request.POST.get(f'n_year_{row.code}', None) for row in items_3]
        n_1_year = [request.POST.get(f'n_1_year_{row.code}', None) for row in items_3]
        perc = [request.POST.get(f'perc_{row.code}', None) for row in items_3]

        counter = 0
        associat = []
        fondul = []



        associat = [request.POST.get(f'associat_{row.code}', None) for row in rows]
        fondul = [request.POST.get(f'fondul_{row.code}', None) for row in rows]

        
        #HEADER -- POST
        for i, row, in enumerate(rows):
            try:
                report_item_1 = ReportHeader.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.associat = float(associat[i]) if associat[i] else None
                    report_item_1.fondul = float(fondul[i]) if fondul[i] else None
                    report_item_1.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except ReportHeader.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_1 = ReportHeader.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.associat = float(associat[i]) if associat[i] else None
                    report_item_1.fondul = float(fondul[i]) if fondul[i] else None
                    report_item_1.save()
                    counter += 1
                    report_item_1.counter = counter
                    report_item_1.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")




        #ITEMS - 1 -- POST
        for i, row, in enumerate(items_1):
            try:
                report_item_1 = ReportItems1.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.prejud = float(prejud[i]) if prejud[i] else None
                    report_item_1.sup_10 = float(sup_10[i]) if sup_10[i] else None
                    report_item_1.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except ReportItems1.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_1 = ReportItems1.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.prejud = float(prejud[i]) if prejud[i] else None
                    report_item_1.sup_10 = float(sup_10[i]) if sup_10[i] else None
                    report_item_1.save()
                    counter += 1
                    report_item_1.counter = counter
                    report_item_1.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")

        #ITEMS - 2 -- POST
        for i, row, in enumerate(items_2):
            try:
                report_item_2 = ReportItems2.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_2 is not None:
                    report_item_2.d_t_ini = float(d_t_ini[i]) if d_t_ini[i] else None
                    report_item_2.c_t_ini = float(c_t_ini[i]) if c_t_ini[i] else None
                    report_item_2.calculat = float(calculat[i]) if calculat[i] else None
                    report_item_2.transferat = float(transferat[i]) if transferat[i] else None
                    report_item_2.d_t_fin = float(d_t_fin[i]) if d_t_fin[i] else None
                    report_item_2.c_t_fin = float(c_t_fin[i]) if c_t_fin[i] else None
                    report_item_2.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except ReportItems2.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_2 = ReportItems2.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_2 is not None:
                    report_item_2.d_t_ini = float(d_t_ini[i]) if d_t_ini[i] else None
                    report_item_2.c_t_ini = float(c_t_ini[i]) if c_t_ini[i] else None
                    report_item_2.calculat = float(calculat[i]) if calculat[i] else None
                    report_item_2.transferat = float(transferat[i]) if transferat[i] else None
                    report_item_2.d_t_fin = float(d_t_fin[i]) if d_t_fin[i] else None
                    report_item_2.c_t_fin = float(c_t_fin[i]) if c_t_fin[i] else None
                    report_item_2.save()
                    counter += 1
                    report_item_2.counter = counter
                    report_item_2.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")

            #ITEMS - 3 -- POST
        for i, row, in enumerate(items_3):
            try:
                report_item_3 = ReportItems3.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_3 is not None:
                    report_item_3.n_year = float(n_year[i]) if n_year[i] else None
                    report_item_3.n_1_year = float(n_1_year[i]) if n_1_year[i] else None
                    report_item_3.perc = float(perc[i]) if perc[i] else None
                    report_item_3.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except ReportItems3.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_3 = ReportItems3.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_3 is not None:
                    report_item_3.n_year = float(n_year[i]) if n_year[i] else None
                    report_item_3.n_1_year = float(n_1_year[i]) if n_1_year[i] else None
                    report_item_3.perc = float(perc[i]) if perc[i] else None
                    report_item_3.save()
                    counter += 1
                    report_item_3.counter = counter
                    report_item_3.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")
        # print('POST Запрос',request.POST)
        # print(f"Number of InfEconOp objects saved: {counter}")  # выводим число сохраненных объектов
        return HttpResponseRedirect(request.path_info)