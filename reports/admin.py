from django.contrib import admin
from reports.models import InfEconOp, CompanyData, ManagerRaportStocuri, Stocuri2, Stocuri1, ManagerRaportStatisticTrimestrial, InvestitiiActive1, InvestitiiActive2, ReportItems1, MiscCadrelor, ManagerMiscCadrelor, ReportItems2, ReportItems3, ReportHeader, ManagerReportDescriereaAsociati, SecondInfEconOp, ManagerInfEconOp


@admin.register(CompanyData)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(ManagerRaportStocuri)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(Stocuri1)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(Stocuri2)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(ManagerRaportStatisticTrimestrial)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(InvestitiiActive1)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(InvestitiiActive2)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(ManagerMiscCadrelor)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(MiscCadrelor)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(ReportItems3)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(ReportItems2)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(ReportItems1)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(ReportHeader)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(ManagerReportDescriereaAsociati)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(ManagerInfEconOp)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(InfEconOp)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(SecondInfEconOp)
class AccountAdmin(admin.ModelAdmin):
    pass
