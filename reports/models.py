from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import uuid

class CompanyData(models.Model):
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4)
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
    user = models.ForeignKey(User, verbose_name=_("Company"), on_delete=models.CASCADE, related_name='user')
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
    user = models.ForeignKey(User, verbose_name=_("Company"), on_delete=models.CASCADE, related_name='company')
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