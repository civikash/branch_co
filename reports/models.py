from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import uuid

class CompanyData(models.Model):
    uid = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(_("Denumirea"), max_length=150, null=False)
    address = models.CharField(_("Adresa"), max_length=150, null=False)
    district = models.CharField(_("Raionul"), max_length=74, null=False)
    village = models.CharField(_("Satul"), max_length=55, null=False)
    street = models.CharField(_("Strada"), max_length=155, null=False)
    code_cuiio = models.IntegerField(null=False)
    code_idno = models.IntegerField(null=False)
    ruler = models.CharField(_("Conducătorul"), max_length=150, null=False)
    accountant = models.CharField(_("Contabil"), max_length=150, null=False)
    executor = models.CharField(_("Executantul"), max_length=150, null=False)
    tel = models.CharField(_("Tel"), max_length=15, null=False)
    anul = models.CharField(_("Anul"), max_length=5, null=False)



class InfEconOp(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.PROTECT, to_field='uid', related_name='account_company')
    code = models.AutoField(_("Code"), primary_key=True)
    counter = models.IntegerField(_("Counter"), default=0)
    n_year = models.IntegerField(_("Year"), null=True, blank=True)
    n_month = models.IntegerField(_("Month"), null=True, blank=True)
    before_year = models.IntegerField(_("Before Year"), null=True, blank=True)
    before_month = models.IntegerField(_("Before Month"), null=True, blank=True)
    n_beforeTotal = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    n_beforeLunar = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    n_total = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    n_lunar = models.DecimalField(max_digits=10, decimal_places=1, null=True)

    class Meta:
        unique_together = ('code', 'counter')


class SecondInfEconOp(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.PROTECT, related_name='company')
    code = models.AutoField(_("Code"), primary_key=True)
    counter = models.IntegerField(_("Counter"), default=0)
    name = models.CharField(_("Denumirea"), max_length=150, null=True)
    n_year = models.IntegerField(_("Year"), null=True, blank=True)
    n_month = models.IntegerField(_("Month"), null=True, blank=True)
    before_year = models.IntegerField(_("Before Year"), null=True, blank=True)
    before_month = models.IntegerField(_("Before Month"), null=True, blank=True)
    n_beforeTotal = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    n_beforeLunar = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    n_total = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    n_lunar = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    n_beforeMarfa = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    n_Marfa = models.DecimalField(max_digits=10, decimal_places=1, null=True)

    class Meta:
        unique_together = ('code', 'counter')

class ManagerInfEconOp(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    reports = models.ForeignKey(InfEconOp, verbose_name=_("Первый отчет"), on_delete=models.CASCADE, to_field='code')
    reports_second = models.ForeignKey(SecondInfEconOp, verbose_name=_("Вторая часть"), on_delete=models.CASCADE, null=True, to_field='code')
    date = models.DateField(_("Дата"), auto_now=True)

class VolVanzAmauntul(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.CASCADE, related_name='company_volvanz')
    code = models.AutoField(_("Code"), primary_key=True)
    counter = models.IntegerField(_("Counter"), default=0)
    name = models.CharField(_("Denumirea"), max_length=150, null=True)
    n_year = models.IntegerField(_("Year"), null=True, blank=True)
    n_month = models.IntegerField(_("Month"), null=True, blank=True)
    prec = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    cur = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    percentage = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    pond_prec = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    pond_cur = models.DecimalField(max_digits=10, decimal_places=1, null=True)

    class Meta:
        unique_together = ('code', 'counter')

class ReportHeader(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.CASCADE, related_name='company_report_header')
    code = models.AutoField(_("Code"), primary_key=True)
    associat = models.BooleanField(_("Associat"))
    fondul = models.BooleanField(_("Associat"))

class ReportItems1(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.CASCADE, related_name='company_report_items_1')
    code = models.AutoField(_("Code"), primary_key=True)
    prejud = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    sup_10 = models.DecimalField(max_digits=10, decimal_places=1, null=True)

class ReportItems2(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.CASCADE, related_name='company_report_items_2')
    code = models.AutoField(_("Code"), primary_key=True)
    d_t_ini = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    c_t_ini = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    calculat = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    transferat = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    d_t_fin = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    c_t_fin = models.DecimalField(max_digits=10, decimal_places=1, null=True)

class ReportItems3(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.CASCADE, related_name='company_report_items_3')
    code = models.AutoField(_("Code"), primary_key=True)
    n_year = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    n_1_year = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    perc = models.IntegerField(_("Perc"))


@receiver(pre_save, sender=InfEconOp)
def update_n_total(sender, instance, **kwargs):
    if instance.n_year is not None:
        instance.before_year = instance.n_year - 1
    if instance.n_month is not None:
        instance.before_month = instance.n_month - 1


@receiver(pre_save, sender=SecondInfEconOp)
def update_before_year(sender, instance, **kwargs):
    if instance.n_year is not None:
        instance.before_year = instance.n_year - 1
    if instance.n_month is not None:
        instance.before_month = instance.n_month - 1