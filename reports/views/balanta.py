from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from datetime import datetime
from django.db.models import Max
from django.http import HttpResponseRedirect
from reports.models import Balanta1, Balanta2, Balanta3, Balanta4, ManagerRaportBalanta


class BalantaListView(View):
    template_name = 'reports/reports/balanta/balanta_list.html'

    def dispatch(self, request, *args, **kwargs):
        rows = Balanta1.objects.filter(
            company__users__username=request.user).order_by('code')
        item_1 = Balanta2.objects.filter(
            company__users__username=request.user).order_by('code')
        item_2 = Balanta3.objects.filter(
            company__users__username=request.user).order_by('code')
        item_3 = Balanta4.objects.filter(
            company__users__username=request.user).order_by('code')

        # получить максимальный код, если такие объекты уже существуют
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

        # HEADER создать новые объекты с одинаковым значением counter, начиная с max_counter + 1
        num_new_objs = 130 - len(rows)
        next_counter = max_counter + 1 if num_new_objs > 0 else max_counter + 1  # Определение значения next_counter

        # ITEM_1
        item_new_objs_1 = 44 - len(item_1)
        next_counter_item_1 = max_counter_1 + 1 if item_new_objs_1 > 0 else max_counter_1 + 1  # Определение значения next_counter

        # ITEM_2
        item_new_objs_2 = 22 - len(item_2)
        next_counter_item_2 = max_counter_2 + 1 if item_new_objs_2 > 0 else max_counter_2 + 1  # Определение значения next_counter

        # ITEM_3
        item_new_objs_3 = 29 - len(item_3)
        next_counter_item_3 = max_counter_3 + 1 if item_new_objs_3 > 0 else max_counter_3 + 1  # Определение значения next_counter

        # Проверка метода запроса
        if request.method == 'POST':
            indocatori = [
                'ACTIVE IMOBILIZATE I. Imobilizări necorporale',
                '1. Imobilizări necorporale în curs de execuție',
                '2. Imobilizări necorporale în exploatare, total',
                'din care: 2.1. concesiuni, licențe și mărci',
                '2.2. drepturi de autor și titluri de protecție',
                '2.3. programe informatice',
                '2.4. alte imobilizări necorporale',
                '3. Fond comercial',
                '4. Avansuri acordate pentru imobilizări necorporale',
                'Total imobilizări necorporale (rd.010 + rd.020 + rd.030 + rd.040)',
                'II. Imobilizări corporale',
                '1. Imobilizări corporale în curs de execuție',
                '2. Terenuri',
                '3. Mijloace fixe, total',
                'din care: 3.1. clădiri',
                '3.2. construcții speciale',
                '3.3. mașini, utilaje și instalații tehnice',
                '3.4. mijloace de transport',
                '3.5. inventar și mobilier',
                '3.6. alte mijloace fixe',
                '4. Resurse minerale',
                '5. Active biologice imobilizate',
                '6. Investiții imobiliare',
                '7. Avansuri acordate pentru imobilizări corporale',
                'Total imobilizări corporale (rd.060 + rd.070 + rd.080 + rd.090 + rd.100 + rd.110 + rd.120)',
                'III. Investiții financiare pe termen lung',
                '1. Investiții financiare pe termen lung în părți neafiliate',
                '2. Investiții financiare pe termen lung în părți afiliate, total',
                'din care: 2.1. acțiuni și cote de participație deținute în părțile afiliate',
                '2.2 împrumuturi acordate părților afiliate',
                '2.3 împrumuturi acordate aferente intereselor de participare',
                '2.4 alte investiții financiare',
                'Total investiții financiare pe termen lung (rd.140 + rd.150)',
                'IV. Creanțe pe termen lung și alte active imobilizate',
                '1. Creanțe comerciale pe termen lung',
                '2. Creanțe ale părților afiliate pe termen lung',
                'inclusiv: creanțe aferente intereselor de participare',
                '3. Alte creanțe pe termen lung',
                '4. Cheltuieli anticipate pe termen lung',
                '5. Alte active imobilizate',
                'Total creanțe pe termen lung și alte active imobilizate (rd.170 + rd.180 + rd.190 + rd.200 + rd.210)',
                'TOTAL ACTIVE IMOBILIZATE (rd.050 + rd.130 + rd.160 + rd.220)',
                'ACTIVE CIRCULANTE I. Stocuri',
                '1. Materiale și obiecte de mică valoare și scurtă durată',
                '2. Active biologice circulante',
                '3. Producția în curs de execuție',
                '4. Produse și mărfuri',
                '5. Avansuri acordate pentru stocuri',
                'Total stocuri (rd.240 + rd.250 + rd.260 + rd.270 + rd.280)',
                'II. Creanțe curente și alte active circulante',
                '1. Creanțe comerciale curente',
                '2. Creanțe ale părților afiliate curente',
                'inclusiv: creanțe aferente intereselor de participare',
                '3. Creanțe ale bugetului',
                '4. Creanțele ale personalului',
                '5. Alte creanțe curente',
                '6. Cheltuieli anticipate curente',
                '7. Alte active circulante',
                'Total creanțe curente și alte active circulante (rd.300 + rd.310 + rd.320 + rd.330 + rd.340 + rd.350 + rd.360)',
                'III. Investiții financiare curente',
                '1. Investiții financiare curente în părți neafiliate',
                '2. Investiții financiare curente în părți afiliate, total',
                'din care: 2.1. acțiuni și cote de participație deținute în părțile afiliate',
                '2.2. împrumuturi acordate părților afiliate',
                '2.3. împrumuturi acordate aferente intereselor de participare',
                '2.4. alte investiții financiare în părți afiliate',
                'Total investiții financiare curente (rd.380 + rd.390)',
                'IV. Numerar și documente bănești',
                'TOTAL ACTIVE CIRCULANTE (rd.290 + rd.370 + rd.400 + rd.410)',
                'TOTAL ACTIVE (rd.230 + rd.420)',
                'P A S I V',
                'CAPITAL PROPRIU I. Capital social și neînregistrat'
                '1. Capital social',
                '2. Capital nevărsat',
                '3. Capital neînregistrat',
                '4. Capital retras',
                '5. Patrimoniul primit de la stat cu drept de proprietate',
                'Total capital social și neînregistrat (rd.440 + rd.450 + rd.460 + rd.470 + rd.480)',
                'II. Prime de capital',
                'III. Rezerve',
                '1. Capital de rezervă',
                '2. Rezerve statutare',
                '3. Alte rezerve',
                'Total rezerve (rd.510 + rd.520 + rd.530)',
                'IV. Profit (pierdere)',
                '1. Corecții ale rezultatelor anilor precedenți',
                '2. Profit nerepartizat (pierdere neacoperită) al anilor precedenți',
                '3. Profit net (pierdere netă) al perioadei de gestiune',
                '4. Profit utilizat al perioadei de gestiune',
                'Total profit (pierdere) (rd.550 + rd.560 + rd.570 + rd.580)',
                'V. Rezerve din reevaluare',
                'VI. Alte elemente de capital propriu',
                'TOTAL CAPITAL PROPRIU (rd.490 + rd.500 + rd.540 + rd.590 + rd.600 + rd.610)',
                'DATORII PE TERMEN LUNG',
                '1. Credite bancare pe termen lung',
                '2. Împrumuturi pe termen lung',
                'din care: 2.1. împrumuturi din emisiunea de obligațiuni',
                'inclusiv: împrumuturi din emisiunea de obligațiuni convertibile',
                '2.2. alte împrumuturi pe termen lung',
                '3. Datorii comerciale pe termen lung',
                '4. Datorii față de părțile afiliate pe termen lung',
                'inclusiv: datorii aferente intereselor de participare',
                '5. Avansuri primite pe termen lung',
                '6. Venituri anticipate pe termen lung',
                '7. Alte datorii pe termen lung',
                'TOTAL DATORII PE TERMEN LUNG (rd.630 + rd.640 + rd.650 + rd.660 + rd.670 + rd.680 + rd.690)',
                'DATORII CURENTE',
                '1. Credite bancare pe termen scurt',
                '2. Împrumuturi pe termen scurt, total',
                'din care: 2.1. împrumuturi din emisiunea de obligațiuni',
                'inclusiv: împrumuturi din emisiunea de obligațiuni convertibile',
                '2.2. alte împrumuturi pe termen scurt',
                '3. Datorii comerciale curente',
                '4. Datorii față de părțile afiliate curente',
                'inclusiv: datorii aferente intereselor de participare',
                '5. Avansuri primite curente',
                '6. Datorii față de personal',
                '7. Datorii privind asigurările sociale și medicale',
                '8. Datorii față de buget',
                '9. Datorii față de proprietari',
                '10. Venituri anticipate curente',
                '11. Alte datorii curente',
                'TOTAL DATORII CURENTE (rd.710 + rd.720 + rd.730 + rd.740 + rd.750 + rd.760 + rd.770 + rd.780 + rd.790 + rd.800 + rd.810)',
                'PROVIZIOANE',
                '1. Provizioane pentru beneficiile angajaților',
                '2. Provizioane pentru garanții acordate cumpărătorilor/clienților',
                '3. Provizioane pentru impozite',
                '4. Alte provizioane',
                'TOTAL PROVIZIOANE (rd.830 + rd.840 + rd.850 + rd.860)',
                'TOTAL PASIVE (rd.620 + rd.700 + rd.820 + rd.870)'
            ]
            code_rd = ['', '010', '020', '021', '022', '023', '024', '030', '040', '050', '', 
                       '060', '070', '080', '081', '082', '083', '084', '085', '086', '090',
                       '100', '110', '120', '130', '', '140', '150', '151', '152', '153', '154',
                       '160', '', '170', '180', '181', '190', '200', '210', '220', '230', '',
                       '240', '250', '260', '270', '280', '290', '', '300', '310', '311', '320',
                       '330', '340', '350', '360', '370', '', '380', '390', '391', '392', '393',
                       '394', '400', '410', '420', '430', '', '', '440', '450', '460', '470', '480',
                       '490', '500', '', '510', '520', '530', '540', '', '550', '560', '570',
                       '580', '590', '600', '610', '620', '', '630', '640', '641', '642', '643',
                       '650', '660', '661', '670',' 680', '690', '700', '', '710', '720', '721',
                       '722', '723', '730', '740', '741', '750', '760', '770', '780', '790', '800',
                       '810', '820', '', '830', '840', '850', '860', '870', '880']
            
            indicatori_2_turple = ['Venituri din vînzări, total', 
                                   'din care: venituri din vînzarea produselor și mărfurilor',
                                   'venituri din prestarea serviciilor și executarea lucrărilor',
                                   'venituri din contracte de construcție',
                                   'venituri din contracte de leasing',
                                   'venituri din contracte de microfinanţare',
                                   'alte venituri din vînzări',
                                   'Costul vînzărilor, total',
                                   'din care: valoarea contabilă a produselor și mărfurilor vîndute',
                                   'costul serviciilor prestate și lucrărilor executate terților',
                                   'costuri aferente contractelor de construcție',
                                   'costuri aferente contractelor de leasing',
                                   'costuri aferente contractelor de microfinanţare',
                                   'alte costuri aferente vînzărilor',
                                   'Profit brut (pierdere brută) (rd.010 - rd.020)',
                                   'Alte venituri din activitatea operațională',
                                   'Cheltuieli de distribuire',
                                   'Cheltuieli administrative',
                                   'Alte cheltuieli din activitatea operațională',
                                   'Rezultatul din activitatea operațională: profit (pierdere) (rd.030 + rd.040 - rd.050 - rd.060 - rd.070)',
                                   'Venituri financiare, total',
                                   'din care: venituri din interese de participare',
                                   'inclusiv: veniturile obținute de la părțile afiliate',
                                   'venituri din dobînzi',
                                   'inclusiv: veniturile obținute de la părțile afiliate',
                                   'venituri din alte investiții financiare pe termen lung',
                                   'inclusiv: veniturile obținute de la părțile afiliate',
                                   'venituri aferente ajustărilor de valoare privind investițiile financiare pe termen lung și curente',
                                   'venituri din ieșirea investițiilor financiare',
                                   'venituri aferente diferențelor de curs valutar și de sumă',
                                   'Cheltuieli financiare, total',
                                   'din care: cheltuieli privind dobînzile',
                                   'inclusiv: cheltuielile aferente părților afiliate',
                                   'cheltuieli aferente ajustărilor de valoare privind investițiile financiare pe termen lung și curente',
                                   'cheltuieli aferente ieșirii investițiilor financiare',
                                   'cheltuieli aferente diferențelor de curs valutar și de sumă',
                                   'Rezultatul: profit (pierdere) financiar(ă) (rd.090 - rd.100)',
                                   'Venituri cu active imobilizate și excepționale',
                                   'Cheltuieli cu active imobilizate și excepționale',
                                   'Rezultatul din operațiuni cu active imobilizate și excepționale: profit (pierdere) (rd.120 - rd.130)',
                                   'Rezultatul din alte activități: profit (pierdere) (rd.110 + rd.140)',
                                   'Profit (pierdere) pînă la impozitare (rd.080 + rd.150)',
                                   'Cheltuieli privind impozitul pe venit',
                                   'Profit net (pierdere netă) al perioadei de gestiune (rd.160 - rd.170)']
            
            code_rd_2 = ['010', '011', '012', '013', '014', '015', '016', '020', '021', '022', '023',
                         '024', '025', '026', '030', '040', '050', '060', '070', '080', '090' ,'091',
                         '092', '093', '094', '095', '096', '097', '098', '099', '100', '101', '102',
                         '103', '104', '105', '110', '120', '130', '140', '150', '160', '170', '180']

            indicatori_3_turple = ['Capital social și neînregistrat',
                                   '1. Capital social',
                                   '2. Capital nevărsat',
                                   '3. Capital neînregistrat',
                                   '4. Capital retras',
                                   '5. Patrimoniul primit de la stat cu drept de proprietate',
                                   'Total capital social și neînregistrat (rd.010 + rd.020 + rd.030 + rd.040 + rd.050)',
                                   'Prime de capital',
                                   'Rezerve',
                                   '1. Capital de rezervă',
                                   '2. Rezerve statutare',
                                   '3. Alte rezerve',
                                   'Total rezerve (rd.080 + rd.090 + rd.100)',
                                   'Profit (pierdere)',
                                   '1. Corecții ale rezultatelor anilor precedenți',
                                   '2. Profit nerepartizat (pierdere neacoperită) al anilor precedenți',
                                   '3. Profit net (pierdere netă) al perioadei de gestiune',
                                   '4. Profit utilizat al perioadei de gestiune',
                                   'Total profit (pierdere) (rd.120 + rd.130 + rd.140 + rd.150)',
                                   'Rezerve din reevaluare',
                                   'Alte elemente de capital propriu',
                                   'Total capital propriu (rd.060 + rd.070 + rd.110 + rd.160 + rd.170 + rd.180)']

            code_rd_3 = ['', '010', '020', '030', '040', '050', '060', '070', '', '080', '090', '100',
                         '110', '', '120', '130', '140', '150', '160', '170', '180', '190']

            indicatori_4_turple = ['Fluxuri de numerar din activitatea operațională',
                                   'Încasări din vînzări',
                                   'Plăți pentru stocuri și servicii procurate',
                                   'Plăți către angajați și organe de asigurare socială și medicală',
                                   'Dobînzi plătite',
                                   'Plata impozitului pe venit',
                                   'Alte încasări',
                                   'Alte plăți',
                                   'Fluxul net de numerar din activitatea operațională (rd.010 - rd.020 - rd.030 - rd.040 - rd.050 + rd.060 - rd.070)',
                                   'Fluxuri de numerar din activitatea de investiții',
                                   'Încasări din vînzarea activelor imobilizate',
                                   'Plăți aferente intrărilor de active imobilizate',
                                   'Dobînzi încasate',
                                   'Dividende încasate',
                                   'inclusiv: dividende încasate din străinătate',
                                   'Alte încasări (plăți)',
                                   'Fluxul net de numerar din activitatea de investiții (rd.090 - rd.100 + rd.110 + rd.120 ± rd.130)',
                                   'Fluxuri de numerar din activitatea financiară',
                                   'Încasări sub formă de credite și împrumuturi',
                                   'Plăți aferente rambursării creditelor și împrumuturilor',
                                   'Dividende plătite',
                                   'inclusiv: dividende plătite nerezidenților',
                                   'Încasări din operațiuni de capital',
                                   'Alte încasări (plăți)',
                                   'Fluxul net de numerar din activitatea financiară (rd.150 - rd.160 - rd.170 + rd.180 ± rd.190)',
                                   'Fluxul net de numerar total (± rd.080 ± rd.140 ± rd.200)',
                                   'Diferențe de curs valutar favorabile (nefavorabile)',
                                   'Sold de numerar la începutul perioadei de gestiune',
                                   'Sold de numerar la sfîrşitul perioadei de gestiune (± rd.210 ± rd.220 + rd.230)']
            
            code_rd_4 = ['', '010', '020', '030', '040', '050', '060', '070', '080', '', '090',
                         '100', '110', '120', '121', '130', '140', '', '150', '160', '170',
                         '171', '180', '190', '200', '210', '220', '230', '240']

            # Создание первого объекта InfEconOp с заполненными полями company и counter
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

            # Создание остальных объектов InfEconOp с увеличенным значением counter
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
            manager_inf_econ_op = ManagerRaportBalanta.objects.create(
                reports=inf_econ_op, reports_2=item_post_1, reports_3=item_post_2, reports_4=item_post_3)

            # Перенаправление на страницу, где будет отображен созданный объект
            return redirect('reports:balanta-detail', uid=manager_inf_econ_op.uid)

        # Если метод запроса не POST, вызываем метод dispatch родительского класса
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        reports_user = ManagerRaportBalanta.objects.filter(reports__company=request.user.company)
        context = {'reports': reports_user}
        return render(request, self.template_name, context)


class BalantaDetail(View):
    template_name = 'reports/reports/balanta/balanta_detail.html'
    user = None


    def get(self, request, uid, *args, **kwargs):
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

        #HEADER
        la = [header.la for header in raport_detail]
        indicatorii_1 = [header.indicatorii for header in raport_detail]
        code_rind_1 = [header.code_rind for header in raport_detail]
        inceputul_1 = [header.inceputul for header in raport_detail]
        sfirsitul_1 = [header.sfirsitul for header in raport_detail]

        #ITEMS-1
        indicatorii_2 = [item1.indicatorii for item1 in raport_item_1]
        de_la_2 = [item1.de_la for item1 in raport_item_1]
        pina_la_2 = [item1.pina_la for item1 in raport_item_1]
        code_rind_2 = [item1.code_rind for item1 in raport_item_1]
        precedenta_2 = [item1.precedenta for item1 in raport_item_1]
        curenta_2 = [item1.curenta for item1 in raport_item_1]


        #ITEMS-2 
        indicatorii_3 = [item2.indicatorii for item2 in raport_item_2]
        de_la_3 = [item2.de_la for item2 in raport_item_2]
        pina_la_3 = [item2.pina_la for item2 in raport_item_2]
        code_rind_3 = [item2.code_rind for item2 in raport_item_2]
        inceputul_3 = [item2.inceputul for item2 in raport_item_2]
        majorari_3 = [item2.majorari for item2 in raport_item_2]
        diminuari_3 = [item2.diminuari for item2 in raport_item_2]
        sfirsitul_3 = [item2.sfirsitul for item2 in raport_item_2]


        #ITEMS-3
        indicatorii_4 = [item3.indicatorii for item3 in raport_item_3]
        de_la_4 = [item3.de_la for item3 in raport_item_3]
        pina_la_4 = [item3.pina_la for item3 in raport_item_3]
        code_rind_4 = [item3.code_rind for item3 in raport_item_3]
        precedenta_4 = [item3.precedenta for item3 in raport_item_3]
        curenta_4 = [item3.curenta for item3 in raport_item_3]

        header = [
            {
                'crt': 'A',
                'rowspan': 42,
                'indicatorii': indicatorii_1 if indicatorii_1 else '',
                'code_rind': code_rind_1 if code_rind_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '',
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else ''
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '',
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '',
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else ''
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '',
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else ''
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '',
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else ''
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '',
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else ''
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '',
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else ''
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '',
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #10
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #11
                'code_rind': code_rind_1 if code_rind_1 else '',
                # 'inceputul': inceputul_1 if inceputul_1 else '',
                # 'sfirsitul': sfirsitul_1 if sfirsitul_1 else ''
            },
            {         
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #12
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #13
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #14
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #15
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #16
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #17
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #18
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #19
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #20
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #21
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #22
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #23
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #24
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #25
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #26
                'code_rind': code_rind_1 if code_rind_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #27
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #28
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #29
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #30
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #31
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #32
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                                {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #33
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                                            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #34
                'code_rind': code_rind_1 if code_rind_1 else '',
            },
                                                {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #35
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                                {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #36
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #37
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #38
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #39
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #40
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #41
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #42
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {   'crt': 'B',
                'rowspan': 28,
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #43
                'code_rind': code_rind_1 if code_rind_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #44
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #45
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #46
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #47
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #48
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #49
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #50
                'code_rind': code_rind_1 if code_rind_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #51
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #52
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #53
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #54
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #55
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #56
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #57
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #58
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #59
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #60
                'code_rind': code_rind_1 if code_rind_1 else '',
            },
                        {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #61
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #62
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #63
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #64
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                        {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #65
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                        {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #66
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #67
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #68
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #69
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #70
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'colspan': 5,
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #71
            },
            {
                'crt': 'C',
                'rowspan': 21,
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #72
                'code_rind': code_rind_1 if code_rind_1 else '', 
            },
                                                {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #73
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                                {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #74
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                                {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #75
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                                {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #76
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                                {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #77
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                                            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #78
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                                            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #79
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #80
            },
                                                            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #81
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                                            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #82
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                                            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #83
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                                                        {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #84
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                                                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #85
                'code_rind': code_rind_1 if code_rind_1 else '',
            },
             {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #86
                'code_rind': code_rind_1 if code_rind_1 else '',
                'X': 'X'
            },
                                                                        {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #87
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                         {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #88
                'code_rind': code_rind_1 if code_rind_1 else '',
                'X': 'X'
            },
                         {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #89
                'code_rind': code_rind_1 if code_rind_1 else '',
                'X': 'X'
            },
                         {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #90
                'code_rind': code_rind_1 if code_rind_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                                                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #91
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                                                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #92
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                     {
                                                         'crt': 'D',
                'rowspan': 13,
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #93
                'code_rind': code_rind_1 if code_rind_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                                                                                {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #94
                'code_rind': code_rind_1 if code_rind_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #95
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #96
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #97
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #98
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #99
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                        {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #100
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #101
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #102
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #103
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #104
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #105
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                        {
                                                                                     'crt': 'E',
                'rowspan': 17,
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #106
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #107
                'code_rind': code_rind_1 if code_rind_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #108
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #109
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                        {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #110
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #111
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #112
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #113
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #114
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #115
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #116
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #117
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #118
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #119
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #120
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #121
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #122
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                        {
                                           'crt': 'F.',
                'rowspan': 7,
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #123
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },                        
            {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #124
                'code_rind': code_rind_1 if code_rind_1 else '',
            },
                        {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #125
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                        {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #126
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                        {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #127
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            },
                        {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #128
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                    {
                'indicatorii': indicatorii_1 if indicatorii_1 else '', #129
                'code_rind': code_rind_1 if code_rind_1 else '',
                'inceputul': inceputul_1 if inceputul_1 else '',
                'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },      
            #                         {
            #     'indicatorii': indicatorii_1 if indicatorii_1 else '', #130
            #     'code_rind': code_rind_1 if code_rind_1 else '',
            #     'inceputul': inceputul_1 if inceputul_1 else '',
            #     'sfirsitul': sfirsitul_1 if sfirsitul_1 else '',
            #     'blocked_inceputul': True,
            #     'blocked_sfirsitul': True,
            # },      
            
        ]

        items_row_1 = [
            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #1
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #2
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                        {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #3
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                        {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #4
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                        {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #5
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                        {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #6
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                        {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #7
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                        {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #8
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                    {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #9
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                    {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #10
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                    {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #11
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                    {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #12
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                    {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #13
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                    {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #14
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                    {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #15
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                                {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #16
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #17
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #18
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #19
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #20
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #21
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #22
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #23
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #24
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #25
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #26
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #27
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #28
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #29
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #30
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #31
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #32
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #33
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #34
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #35
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #36
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                            {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #37
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                                                        {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #38
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                                        {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #39
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                                        {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #40
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                                                        {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #41
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                                                        {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #42
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
                                                                                    {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #43
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
            },
                                                                                    {
                'indicatorii': indicatorii_2 if indicatorii_2 else '', #44
                'code_rind': code_rind_2 if code_rind_2 else '',
                'precedenta': precedenta_2 if precedenta_2 else '',
                'curenta': curenta_2 if curenta_2 else '',
                'blocked_inceputul': True,
                'blocked_sfirsitul': True,
            },
        ]

        items_row_2 = [
            {
                'crt': 'I.',
                'rowspan': 7,
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #1
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #2
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #3
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #4
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #5
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #6
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_inceputul': True,
                'blocked_majorari': True,
                'blocked_diminuari': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #7
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
                        {
                'crt': 'II.',
                'rowspan': 1,
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #8
                'blocked_sfirsitul': True,
            },
            {
                                'crt': 'III.',
                'rowspan': 5,
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #9
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
             {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #10
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
                         {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #11
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #12
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_inceputul': True,
                'blocked_majorari': True,
                'blocked_diminuari': True,
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #13
                'blocked_sfirsitul': True,
            },
            {
                'crt': 'IV.',
                'rowspan': 6,
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #14
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  'X',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
                         {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #15
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #16
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  'X',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #17
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  'X',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
            {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #18
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_inceputul': True,
                'blocked_majorari': True,
                'blocked_diminuari': True,
                'blocked_sfirsitul': True,
            },
                         {
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #19
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
                         {
                                             'crt': 'V.',
                'rowspan': 1,
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #20
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_sfirsitul': True,
            },
                        {
                'crt': 'VI.',
                'rowspan': 1,
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #21
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_inceputul': True,
                'blocked_majorari': True,
                'blocked_diminuari': True,
                'blocked_sfirsitul': True,
            },
                                    {
                'crt': '.',
                'rowspan': 1,
                'indicatorii': indicatorii_3 if indicatorii_3 else '', #22
                'code_rind': code_rind_3 if code_rind_3 else '',
                'inceputul':  inceputul_3 if inceputul_3 else '',
                'majorari': majorari_3 if majorari_3 else '',
                'diminuari': diminuari_3 if diminuari_3 else '',
                'sfirsitul':  sfirsitul_3 if sfirsitul_3 else '',
                'blocked_inceputul': True,
                'blocked_majorari': True,
                'blocked_diminuari': True,
                'blocked_sfirsitul': True,
            }
            
        ]   
        items_row_3 = [
            {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #1
            },
            {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #2
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
            {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #3
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
            {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #4
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
            {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #5
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                        {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #6
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                        {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #7
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                        {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #8
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                    {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #9
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
                'blocked_precedenta': True,
                'blocked_curenta': True,
            },
            {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #10
            },
                                    {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #11
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                    {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #12
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                    {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #13
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                    {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #14
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                    {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #15
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                    {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #16
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                                {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #17
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
                'blocked_precedenta': True,
                'blocked_curenta': True,
            },
                        {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #18
            },
                                                {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #19
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                                {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #20
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                                {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #21
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                                {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #22
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                                {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #23
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                                {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #24
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                                            {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #25
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
                'blocked_precedenta': True,
                'blocked_curenta': True,
            },
                                                            {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #26
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
                'blocked_precedenta': True,
                'blocked_curenta': True,
            },
                                                            {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #27
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                                            {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #28
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
            },
                                                                        {
                'indicatorii': indicatorii_4 if indicatorii_4 else '', #29
                'code_rind': code_rind_4 if code_rind_4 else '',
                'precedenta': precedenta_4 if precedenta_4 else '',
                'curenta': curenta_4 if curenta_4 else '',
                'blocked_precedenta': True,
                'blocked_curenta': True,
            }
        ]   
       
        sales_list = ManagerRaportBalanta.objects.filter(reports__uid=manager_inf_econ_op.reports.uid).order_by('reports__counter')

        # marfa_list = SecondInfEconOp.objects.filter(company__users__username=request.user).order_by('code')
        current_header = 0
        current_item_1 = 0
        current_item_2 = 0
        current_item_3 = 0


        for items_11 in raport_detail: 
            header[current_header]['indicatorii'] = items_11.indicatorii
            header[current_header]['code_rind'] = items_11.code_rind
            header[current_header]['inceputul'] = items_11.inceputul
            header[current_header]['sfirsitul'] = items_11.sfirsitul
            header[current_header]['code'] = items_11.code
            current_header += 1

        for sales in raport_item_1: 
            items_row_1[current_item_1]['indicatorii'] = sales.indicatorii
            items_row_1[current_item_1]['code_rind'] = sales.code_rind
            items_row_1[current_item_1]['precedenta'] = sales.precedenta
            items_row_1[current_item_1]['curenta'] = sales.curenta
            items_row_1[current_item_1]['code'] = sales.code
            current_item_1 += 1

        for sales in raport_item_2: 
            items_row_2[current_item_2]['indicatorii'] = sales.indicatorii
            items_row_2[current_item_2]['code_rind'] = sales.code_rind
            items_row_2[current_item_2]['inceputul'] = sales.inceputul
            items_row_2[current_item_2]['majorari'] = sales.majorari
            items_row_2[current_item_2]['diminuari'] = sales.diminuari
            items_row_2[current_item_2]['sfirsitul'] = sales.sfirsitul
            items_row_2[current_item_2]['code'] = sales.code
            current_item_2 += 1

        for sales in raport_item_3: 
            items_row_3[current_item_3]['indicatorii'] = sales.indicatorii
            items_row_3[current_item_3]['code_rind'] = sales.code_rind
            items_row_3[current_item_3]['precedenta'] = sales.precedenta
            items_row_3[current_item_3]['curenta'] = sales.curenta
            items_row_3[current_item_3]['code'] = sales.code
            current_item_3 += 1

        context = {'sales': sales, 'data_1': data_1, 'data_2': data_2, 'data_3': data_3,
                   'data_4': data_4, 'manager_inf_econ_op': manager_inf_econ_op, 'header': header, 'item_1': items_row_1, 'item_2': items_row_2, 'item_3': items_row_3}
        
        if request.user.is_superuser or check_user:
            return render(request, self.template_name, context)
        elif not check_user:
            return redirect('reports:reports')
        
        return render(request, self.template_name, context)
    
    def post(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerRaportBalanta.objects.get(uid=uid)

        counter_uid = manager_inf_econ_op.reports.counter



        rows = Balanta1.objects.filter(counter=counter_uid).order_by('code')
        
        items_1 = Balanta2.objects.filter(counter=counter_uid).order_by('code')
        items_2 = Balanta3.objects.filter(counter=counter_uid).order_by('code')
        items_3 = Balanta4.objects.filter(counter=counter_uid).order_by('code')


        #ITEMS - 1 -- POST
        data_1 = request.POST.get('data_1')

        if data_1:
            date_obj = datetime.strptime(data_1, "%d.%m.%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")

        indicatori_1 = [request.POST.get(f'indicatori_1_{row.code}', None) for row in rows]
        code_rind_1 = [request.POST.get(f'code_rind_1_{row.code}', None) for row in rows]
        inceputul_1 = [request.POST.get(f'inceputul_1_{row.code}', None) for row in rows]
        sfirsitul_1 = [request.POST.get(f'sfirsitul_1_{row.code}', None) for row in rows]
        
        #ITEMS - 2 -- POST
        data_2 = request.POST.get('data_2')
        data_2_1 = request.POST.get('data_3')

        if data_2:
            date_obj_2 = datetime.strptime(data_2, "%d.%m.%Y")
            formatted_date_2 = date_obj_2.strftime("%Y-%m-%d")
           

        if data_2_1:
            date_obj_2_1 = datetime.strptime(data_2_1, "%d.%m.%Y")
            formatted_date_2_1 = date_obj_2_1.strftime("%Y-%m-%d")

        indicatori_2 = [request.POST.get(f'indicatori_2_{row.code}', None) for row in items_1]
        code_rind_2 = [request.POST.get(f'code_rind_2_{row.code}', None) for row in items_1]
        precedenta_1 = [request.POST.get(f'precedenta_1_{row.code}', None) for row in items_1]
        curenta_1 = [request.POST.get(f'curenta_1_{row.code}', None) for row in items_1]

        #ITEMS - 3 -- POST
        data_3 = request.POST.get('data_4')
        data_3_1 = request.POST.get('data_5')
    
        if data_3:
            date_obj_3 = datetime.strptime(data_3, "%d.%m.%Y")
            formatted_date_3 = date_obj_3.strftime("%Y-%m-%d")

        if data_3_1:
            date_obj_3_1 = datetime.strptime(data_3_1, "%d.%m.%Y")
            formatted_date_3_1 = date_obj_3_1.strftime("%Y-%m-%d")

        indicatori_3 = [request.POST.get(f'indicatori_3_{row.code}', None) for row in items_2]
        code_rind_3 = [request.POST.get(f'code_rind_3_{row.code}', None) for row in items_2]
        inceputul_3 = [request.POST.get(f'inceputul_3_{row.code}', None) for row in items_2]
        majorari_3 = [request.POST.get(f'majorari_3_{row.code}', None) for row in items_2]
        diminuari_3 = [request.POST.get(f'diminuari_3_{row.code}', None) for row in items_2]
        sfirsitul_3 = [request.POST.get(f'sfirsitul_3_{row.code}', None) for row in items_2]

        #ITEMS - 4 -- POST
        data_4 = request.POST.get('data_6')
        data_4_1 = request.POST.get('data_7')

        if data_4:
            date_obj_4 = datetime.strptime(data_4, "%d.%m.%Y")
            formatted_date_4 = date_obj_4.strftime("%Y-%m-%d")

        if data_4_1:
            date_obj_4_1 = datetime.strptime(data_4_1, "%d.%m.%Y")
            formatted_date_4_1 = date_obj_4_1.strftime("%Y-%m-%d")

        indicatori_4 = [request.POST.get(f'indicatori_4_{row.code}', None) for row in items_3]
        code_rind_4 = [request.POST.get(f'code_rind_4_{row.code}', None) for row in items_3]
        precedenta_4 = [request.POST.get(f'precedenta_4_{row.code}', None) for row in items_3]
        curenta_4 = [request.POST.get(f'curenta_4_{row.code}', None) for row in items_3]

        counter = 0
        associat = []
        fondul = []

        #ITEMS - 1 -- POST
        for i, row, in enumerate(rows):
            try:
                report_item_1 = Balanta1.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.la = str(formatted_date) if formatted_date else None
                    report_item_1.indicatori = str(indicatori_1[i]) if indicatori_1[i] else None
                    report_item_1.code_rind = float(code_rind_1[i]) if code_rind_1[i] else None
                    report_item_1.inceputul = float(inceputul_1[i]) if inceputul_1[i] else None
                    report_item_1.sfirsitul = float(sfirsitul_1[i]) if sfirsitul_1[i] else None
                    report_item_1.save()
                    print(report_item_1)
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except Balanta1.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_1 = Balanta1.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.la = str(formatted_date) if formatted_date else None
                    report_item_1.indicatori = str(indicatori_1[i]) if indicatori_1[i] else None
                    report_item_1.code_rind = float(code_rind_1[i]) if code_rind_1[i] else None
                    report_item_1.inceputul = float(inceputul_1[i]) if inceputul_1[i] else None
                    report_item_1.sfirsitul = float(sfirsitul_1[i]) if sfirsitul_1[i] else None
                    report_item_1.save()
                    counter += 1
                    report_item_1.counter = counter
                    report_item_1.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")

        #ITEMS - 2 -- POST
        for i, row, in enumerate(items_1):
            try:
                report_item_2 = Balanta2.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_2 is not None:
                    report_item_2.de_la = str(formatted_date_2) if formatted_date_2 else None
                    report_item_2.pina_la = str(formatted_date_2_1) if formatted_date_2_1 else None
                    report_item_2.indicatori = str(indicatori_2[i]) if indicatori_2[i] else None
                    report_item_2.code_rind = float(code_rind_2[i]) if code_rind_2[i] else None
                    report_item_2.precedenta = float(precedenta_1[i]) if precedenta_1[i] else None
                    report_item_2.curenta = float(curenta_1[i]) if curenta_1[i] else None
                    report_item_2.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except Balanta2.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_2 = Balanta2.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_2 is not None:
                    report_item_2.de_la = str(formatted_date_2) if formatted_date_2 else None
                    report_item_2.pina_la = str(formatted_date_2_1) if formatted_date_2_1 else None
                    report_item_2.indicatori = str(indicatori_2[i]) if indicatori_2[i] else None
                    report_item_2.code_rind = float(code_rind_2[i]) if code_rind_2[i] else None
                    report_item_2.precedenta = float(precedenta_1[i]) if precedenta_1[i] else None
                    report_item_2.curenta = float(curenta_1[i]) if curenta_1[i] else None
                    report_item_2.save()
                    counter += 1
                    report_item_2.counter = counter
                    report_item_2.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")

        #ITEMS - 3 -- POST
        for i, row, in enumerate(items_2):
            try:
                report_item_3 = Balanta3.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_3 is not None:
                    report_item_3.de_la = str(formatted_date_3) if formatted_date_3 else None
                    report_item_3.pina_la = str(formatted_date_3_1) if formatted_date_3_1 else None
                    report_item_3.indicatori = str(indicatori_3[i]) if indicatori_3[i] else None
                    report_item_3.code_rind = float(code_rind_3[i]) if code_rind_3[i] else None
                    report_item_3.inceputul = float(inceputul_3[i]) if inceputul_3[i] else None
                    report_item_3.majorari = float(majorari_3[i]) if majorari_3[i] else None
                    report_item_3.diminuari = float(diminuari_3[i]) if diminuari_3[i] else None
                    report_item_3.sfirsitul = float(sfirsitul_3[i]) if sfirsitul_3[i] else None
                    report_item_3.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except Balanta3.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_3 = Balanta3.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_3 is not None:
                    report_item_3.de_la = str(formatted_date_3) if formatted_date_3 else None
                    report_item_3.pina_la = str(formatted_date_3_1) if formatted_date_3_1 else None
                    report_item_3.indicatori = str(indicatori_3[i]) if indicatori_3[i] else None
                    report_item_3.code_rind = float(code_rind_3[i]) if code_rind_3[i] else None
                    report_item_3.inceputul = float(inceputul_3[i]) if inceputul_3[i] else None
                    report_item_3.majorari = float(majorari_3[i]) if majorari_3[i] else None
                    report_item_3.diminuari = float(diminuari_3[i]) if diminuari_3[i] else None
                    report_item_3.sfirsitul = float(sfirsitul_3[i]) if sfirsitul_3[i] else None
                    report_item_3.save()
                    counter += 1
                    report_item_3.counter = counter
                    report_item_3.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")
        # print('POST Запрос',request.POST)
        # print(f"Number of InfEconOp objects saved: {counter}")  # выводим число сохраненных объектов
        
        #ITEMS - 4 -- POST
        for i, row, in enumerate(items_3):
            try:
                report_item_4 = Balanta4.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_4 is not None:
                    report_item_4.de_la = str(formatted_date_4) if formatted_date_4 else None
                    report_item_4.pina_la = str(formatted_date_4_1) if formatted_date_4_1 else None
                    report_item_4.indicatori = str(indicatori_4[i]) if indicatori_4[i] else None
                    report_item_4.code_rind = float(code_rind_4[i]) if code_rind_4[i] else None
                    report_item_4.precedenta = float(precedenta_4[i]) if precedenta_4[i] else None
                    report_item_4.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except Balanta4.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_4 = Balanta3.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_4 is not None:
                    report_item_4.de_la = str(formatted_date_4) if formatted_date_4 else None
                    report_item_4.pina_la = str(formatted_date_4_1) if formatted_date_4_1 else None
                    report_item_4.indicatori = str(indicatori_4[i]) if indicatori_3[i] else None
                    report_item_4.code_rind = float(code_rind_4[i]) if code_rind_4[i] else None
                    report_item_4.precedenta = float(precedenta_4[i]) if precedenta_4[i] else None
                    report_item_4.save()
                    counter += 1
                    report_item_4.counter = counter
                    report_item_4.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")
        # print('POST Запрос',request.POST)
        # print(f"Number of InfEconOp objects saved: {counter}")  # выводим число сохраненных объектов
        return HttpResponseRedirect(request.path_info)
    
