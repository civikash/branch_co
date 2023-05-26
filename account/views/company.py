from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from reports.models import CompanyData


class CompanyDataView(LoginRequiredMixin, View):
    template_name = 'account/company_account.html'
    success_url = '/reports/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        company_data = CompanyData.objects.create(
            name=request.POST.get('name'),
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
        print(company_data)
        try:
            company_data.full_clean()
            company_data.save()
            return redirect(self.success_url)
        except ValidationError as e:
            return render(request, self.template_name, {'form': company_data, 'errors': e.message_dict})
