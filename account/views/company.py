from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from reports.models import CompanyData
from account.models import User


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
