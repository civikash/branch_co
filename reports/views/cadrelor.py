from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View
from django.db.models import Max
from django.http import HttpResponseRedirect
from reports.models import ManagerReportDescriereaAsociati, ReportHeader, ReportItems1, ReportItems2, ReportItems3, MiscCadrelor, ManagerMiscCadrelor


class CadrelorListView(View):
    template_name = 'reports/reports/cadrelor/cadrelor_list.html'

    def dispatch(self, request, *args, **kwargs):
        rows = MiscCadrelor.objects.filter(
            company__users__username=request.user).order_by('code')

        # получить максимальный код, если такие объекты уже существуют
        max_code = rows.last().code if rows.exists() else 0
        max_counter = MiscCadrelor.objects.aggregate(
            Max('counter'))['counter__max'] or 0

        # HEADER создать новые объекты с одинаковым значением counter, начиная с max_counter + 1
        num_new_objs = 37 - len(rows)
        next_counter = max_counter + 1 if num_new_objs > 0 else max_counter + 1  # Определение значения next_counter

        # Проверка метода запроса
        if request.method == 'POST':
            # Создание первого объекта InfEconOp с заполненными полями company и counter
            inf_econ_op = MiscCadrelor.objects.create(
                company=request.user.company, counter=next_counter)

            # Создание остальных объектов InfEconOp с увеличенным значением counter
            for i in range(36):
                MiscCadrelor.objects.create(
                    company=request.user.company, counter=next_counter)

            # Создание объекта ManagerInfEconOp и связывание с InfEconOp
            manager_inf_econ_op = ManagerMiscCadrelor.objects.create(
                reports=inf_econ_op)

            # Перенаправление на страницу, где будет отображен созданный объект
            return redirect('reports:cadrelor-detail', uid=manager_inf_econ_op.uid)

        # Если метод запроса не POST, вызываем метод dispatch родительского класса
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        reports_user = ManagerMiscCadrelor.objects.filter(reports__company=request.user.company)
        context = {'reports': reports_user}
        return render(request, self.template_name, context)


class CadrelorDetailView(View):
    template_name = 'reports/reports/cadrelor/cadrelor_detail.html'
    user = None


    def get(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerMiscCadrelor.objects.filter(uid=uid).first()
        check_user = ManagerMiscCadrelor.objects.filter(reports__company=request.user.company)
        
        counter = manager_inf_econ_op.reports.counter
        sales = ManagerMiscCadrelor.objects.filter(reports__uid=manager_inf_econ_op.uid).order_by('reports__code')


        raport_detail = MiscCadrelor.objects.filter(counter=counter).order_by('code')
        
        #cadrelor
        codul_rind = [cadrelor.codul_rind for cadrelor in raport_detail]
        category  = [cadrelor.category  for cadrelor in raport_detail]
        num_func = [cadrelor.num_func for cadrelor in raport_detail]
        num_script  = [cadrelor.num_script  for cadrelor in raport_detail]
        num_locuri = [cadrelor.num_locuri for cadrelor in raport_detail]
        sal_pana  = [cadrelor.sal_pana  for cadrelor in raport_detail]
        studii_super = [cadrelor.studii_super for cadrelor in raport_detail]
        studii_medii_speciale  = [cadrelor.studii_medii_speciale  for cadrelor in raport_detail]
        studii_medii = [cadrelor.studii_medii for cadrelor in raport_detail]
        absolventi  = [cadrelor.absolventi  for cadrelor in raport_detail]
        mai_ani  = [cadrelor.mai_ani  for cadrelor in raport_detail]
        mai_ani_consum = [cadrelor.mai_ani_consum for cadrelor in raport_detail]
        perfectionare  = [cadrelor.perfectionare  for cadrelor in raport_detail]

        header = [
            {
                'crt': 1,
                'descrierea': 'Numărul scriptic total al personalului (rubricile 02-15 şi 16-24)',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'descrierea': 'inclusiv:',
                'rowcolumn': 13,
            },
            {
                'crt': 2,
                'descrierea': 'Preşedinţi birouri executive uniuni/cooperative',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 3,
                'descrierea': 'Vicepreşedinţi birouri executive  uniuni/cooperative ',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 4,
                'descrierea': 'Contabili-şefi uniuni/cooperative/ întreprinderi/instituții',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 5,
                'descrierea': 'Directori Întreprinderi comerţ angro',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 6,
                'descrierea': 'Directori Întreprinderi producţie',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 7,
                'descrierea': 'Directori Întreprinderi panificaţie',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 8,
                'descrierea': 'Directori Întreprinderi achiziţii',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 9,
                'descrierea': 'Directori Întreprinderi comerţ amănuntul',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 10,
                'descrierea': 'Directori Întreprinderi alimentaţie publică',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 11,
                'descrierea': 'Conducători entități alte profiluri',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 12,
                'descrierea': 'Șefi pieţe comerciale',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 13,
                'descrierea': 'Şefi direcţii, secţii',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 14,
                'descrierea': 'Specialişti:',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'descrierea': 'inclusiv:',
                'rowcolumn': 13,
            },
            {
                'descrierea': 'Economişti',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
                        {
                'descrierea': 'Merceologi',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'descrierea': 'Contabili-şefi adjuncţi',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'descrierea': 'Contabili',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'descrierea': 'Jurişti ',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'descrierea': 'Instructori  cadre/munca statutară',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'descrierea': 'Ingineri',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'descrierea': 'Alți  specialiști',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 15,
                'descrierea': 'Cenzori',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 16,
                'descrierea': 'Șefi magazine:',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
                        {
                'crt': 17,
                'descrierea': 'Șefi unități alimentație publică',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
                                    {
                'crt': 18,
                'descrierea': 'Vînzători',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
                                                {
                'crt': 19,
                'descrierea': 'Bucatari',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
                                                            {
                'crt': 20,
                'descrierea': 'Chelneri',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
                                                                        {
                'crt': 21,
                'descrierea': 'Barmani',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
            {
                'crt': 22,
                'descrierea': 'Cofetari',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
                        {
                'crt': 23,
                'descrierea': 'Brutari',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
                                    {
                'crt': 24,
                'descrierea': 'Paznici',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
                                                {
                'crt': 25,
                'descrierea': 'Şefi depozite',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
                                                            {
                'crt': 26,
                'descrierea': 'Alţi gestionari',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
                                                                        {
                'crt': 27,
                'descrierea': 'Alţi salariaţi',
                'codul_rind': codul_rind if codul_rind else '',
                'category': category if category else '',
                'num_func': num_func if num_func else '',
                'num_script': num_script if num_script else '',
                'num_locuri': num_locuri if num_locuri else '',
                'sal_pana': sal_pana if sal_pana else '',
                'studii_medii_speciale': studii_medii_speciale if studii_medii_speciale else '',
                'absolventi': absolventi if absolventi else '',
                'mai_ani': mai_ani if mai_ani else '',
                'mai_ani_consum': mai_ani_consum if mai_ani_consum else '',
                'perfectionare': perfectionare if perfectionare else '',
            },
        ]
       
        sales_list = ManagerMiscCadrelor.objects.filter(reports__uid=manager_inf_econ_op.reports.uid).order_by('reports__counter')

        # marfa_list = SecondInfEconOp.objects.filter(company__users__username=request.user).order_by('code')
        current_header = 0


        for sales in raport_detail: 
            header[current_header]['codul_rind'] = sales.codul_rind
            header[current_header]['category'] = sales.category
            header[current_header]['num_func'] = sales.num_func
            header[current_header]['num_script'] = sales.num_script
            header[current_header]['num_locuri'] = sales.num_locuri
            header[current_header]['sal_pana'] = sales.sal_pana
            header[current_header]['studii_medii_speciale'] = sales.studii_medii_speciale
            header[current_header]['absolventi'] = sales.absolventi
            header[current_header]['mai_ani'] = sales.mai_ani
            header[current_header]['mai_ani_consum'] = sales.mai_ani_consum
            header[current_header]['perfectionare'] = sales.perfectionare
            header[current_header]['code'] = sales.code
            current_header += 1

        context = {'sales': sales, 'manager_inf_econ_op': manager_inf_econ_op, 'header': header}

        if request.user.is_superuser or check_user:
            return render(request, self.template_name, context)
        elif not check_user:
            return redirect('reports:reports')
        
        return render(request, self.template_name, context)
    
    def post(self, request, uid, *args, **kwargs):
        manager_inf_econ_op = ManagerMiscCadrelor.objects.get(uid=uid)

        counter_uid = manager_inf_econ_op.reports.counter



        rows = MiscCadrelor.objects.filter(counter=counter_uid).order_by('code')
    

        #MiscCadrelor -- POST
        codul_rind = [request.POST.get(f'codul_rind_{row.code}', None) for row in rows]
        category = [request.POST.get(f'category_{row.code}', None) for row in rows]
        num_func = [request.POST.get(f'num_func_{row.code}', None) for row in rows]
        num_script = [request.POST.get(f'num_script_{row.code}', None) for row in rows]
        num_locuri = [request.POST.get(f'num_locuri_{row.code}', None) for row in rows]
        sal_pana = [request.POST.get(f'sal_pana_{row.code}', None) for row in rows]
        studii_medii_speciale = [request.POST.get(f'studii_medii_speciale_{row.code}', None) for row in rows]
        absolventi = [request.POST.get(f'absolventi_{row.code}', None) for row in rows]
        mai_ani = [request.POST.get(f'mai_ani_{row.code}', None) for row in rows]
        mai_ani_consum = [request.POST.get(f'mai_ani_consum_{row.code}', None) for row in rows]
        perfectionare = [request.POST.get(f'perfectionare_{row.code}', None) for row in rows]
        counter = 0

        #MiscCadrelor -- POST
        for i, row, in enumerate(rows):
            try:
                report_item_1 = MiscCadrelor.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.codul_rind = float(codul_rind[i]) if codul_rind[i] else None
                    report_item_1.category = float(category[i]) if category[i] else None
                    report_item_1.num_func = float(num_func[i]) if num_func[i] else None
                    report_item_1.num_script = float(num_script[i]) if num_script[i] else None
                    report_item_1.num_locuri = float(num_locuri[i]) if num_locuri[i] else None
                    report_item_1.sal_pana = float(sal_pana[i]) if sal_pana[i] else None
                    report_item_1.studii_medii_speciale = float(studii_medii_speciale[i]) if studii_medii_speciale[i] else None
                    report_item_1.absolventi = float(absolventi[i]) if absolventi[i] else None
                    report_item_1.mai_ani = float(mai_ani[i]) if mai_ani[i] else None
                    report_item_1.mai_ani_consum = float(mai_ani_consum[i]) if mai_ani_consum[i] else None
                    report_item_1.perfectionare = float(perfectionare[i]) if perfectionare[i] else None
                    report_item_1.save()
                    # увеличиваем счетчик на 1 при успешном сохранении объекта
            except MiscCadrelor.MultipleObjectsReturned as e:
                # если объектов несколько, нужно выбрать один для изменения
                report_item_1 = MiscCadrelor.objects.filter(counter=counter_uid, code=row.code).first()
                if report_item_1 is not None:
                    report_item_1.codul_rind = float(codul_rind[i]) if codul_rind[i] else None
                    report_item_1.category = float(category[i]) if category[i] else None
                    report_item_1.num_func = float(num_func[i]) if num_func[i] else None
                    report_item_1.num_script = float(num_script[i]) if num_script[i] else None
                    report_item_1.num_locuri = float(num_locuri[i]) if num_locuri[i] else None
                    report_item_1.sal_pana = float(sal_pana[i]) if sal_pana[i] else None
                    report_item_1.studii_medii_speciale = float(studii_medii_speciale[i]) if studii_medii_speciale[i] else None
                    report_item_1.absolventi = float(absolventi[i]) if absolventi[i] else None
                    report_item_1.mai_ani = float(mai_ani[i]) if mai_ani[i] else None
                    report_item_1.mai_ani_consum = float(mai_ani_consum[i]) if mai_ani_consum[i] else None
                    report_item_1.perfectionare = float(perfectionare[i]) if perfectionare[i] else None
                    report_item_1.save()
                    counter += 1
                    report_item_1.counter = counter
                    report_item_1.save() 
            except Exception as e:
                print(f"Error while saving InfEconOp object with id {i+1}: {e}")

        # print('POST Запрос',request.POST)
        # print(f"Number of InfEconOp objects saved: {counter}")  # выводим число сохраненных объектов
        return HttpResponseRedirect(request.path_info)