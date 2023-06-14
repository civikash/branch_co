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
    counter = models.IntegerField(_("Counter"), default=0)
    code = models.AutoField(_("Code"), primary_key=True)
    associat = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    fondul = models.DecimalField(max_digits=10, decimal_places=1, null=True)

class ReportItems1(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    counter = models.IntegerField(_("Counter"), default=0)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.CASCADE, related_name='company_report_items_1')
    code = models.AutoField(_("Code"), primary_key=True)
    prejud = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    sup_10 = models.DecimalField(max_digits=10, decimal_places=1, null=True)

class ReportItems2(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    counter = models.IntegerField(_("Counter"), default=0)
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
    counter = models.IntegerField(_("Counter"), default=0)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.CASCADE, related_name='company_report_items_3')
    code = models.AutoField(_("Code"), primary_key=True)
    n_year = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    n_1_year = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    perc = models.IntegerField(_("Perc"), null=True)

class ManagerReportDescriereaAsociati(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    reports = models.ForeignKey(ReportHeader, verbose_name=_("Головная часть"), on_delete=models.CASCADE, to_field='code')
    report_item_1 = models.ForeignKey(ReportItems1, verbose_name=_("Вторая часть"), on_delete=models.CASCADE, null=True, to_field='code')
    report_item_2 = models.ForeignKey(ReportItems2, verbose_name=_("Вторая часть"), on_delete=models.CASCADE, null=True, to_field='code')
    report_item_3 = models.ForeignKey(ReportItems3, verbose_name=_("Вторая часть"), on_delete=models.CASCADE, null=True, to_field='code')
    date = models.DateField(_("Дата"), auto_now=True)

class MiscCadrelor(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    counter = models.IntegerField(_("Counter"), default=0)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.CASCADE, related_name='misc_cadrelor')
    code = models.AutoField(_("Code"), primary_key=True)
    codul_rind = models.IntegerField(_("Codul rînd"), null=True, blank=True)
    category = models.IntegerField(_("Categorii"), null=True, blank=True)
    num_func = models.IntegerField(_("Num func"), null=True, blank=True)
    num_script = models.IntegerField(_("Num scriptic"), null=True, blank=True)
    num_locuri = models.IntegerField(_("Num locuri"), null=True, blank=True)
    sal_pana = models.IntegerField(_("Sal pana la 30 ani"), null=True, blank=True)
    studii_super = models.IntegerField(_("Studii Superioare"), null=True, blank=True)
    studii_medii_speciale = models.IntegerField(_("Studii medii speciale"), null=True, blank=True)
    studii_medii = models.IntegerField(_("Studii medii"), null=True, blank=True)
    absolventi = models.IntegerField(_("Absolventi"), null=True, blank=True)
    mai_ani = models.IntegerField(_("mai mare 5 ani"), null=True, blank=True)
    mai_ani_consum = models.IntegerField(_("mai mare 5 ani consum"), null=True, blank=True)
    perfectionare = models.IntegerField(_("Perfectionare a cadrelor"), null=True, blank=True)


class ManagerMiscCadrelor(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    reports = models.ForeignKey(MiscCadrelor, verbose_name=_("MiscCadrelor"), on_delete=models.CASCADE, to_field='code')
    date = models.DateField(_("Дата"), auto_now=True)


class InvestitiiActive1(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.PROTECT, to_field='uid', related_name='account_company_investitii')
    code = models.AutoField(_("Code"), primary_key=True)
    counter = models.IntegerField(_("Counter"), default=0)
    codul_rind = models.IntegerField(_("Codul_rînd"), null=True, blank=True)
    indicatori = models.CharField(_("Indicatorii"), max_length=120, null=True, blank=True)
    intrari = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    investitii = models.DecimalField(max_digits=10, decimal_places=1, null=True)


class InvestitiiActive2(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    company = models.ForeignKey(CompanyData, verbose_name=_("Company"), on_delete=models.PROTECT, to_field='uid', related_name='account_company_investitii_2')
    code = models.AutoField(_("Code"), primary_key=True)
    counter = models.IntegerField(_("Counter"), default=0)
    codul_rind = models.IntegerField(_("Codul_rînd"), null=True, blank=True)
    code_cuatm = models.IntegerField(_("CodCUATM"), null=True, blank=True)
    numa_oras = models.CharField(_("Numa_oras"), max_length=120, null=True, blank=True)
    cladiri = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    apart = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    sup_total = models.DecimalField(max_digits=10, decimal_places=1, null=True)


class ManagerRaportStatisticTrimestrial(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
    reports = models.ForeignKey(InvestitiiActive1, verbose_name=_("Investiţii în active imobilizate"), on_delete=models.CASCADE, to_field='code')
    reports_2 = models.ForeignKey(InvestitiiActive2, verbose_name=_("Clădiri rezidenţiale (de locuit)"), on_delete=models.CASCADE, null=True, to_field='code')
    date = models.DateField(_("Дата"), auto_now=True)



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