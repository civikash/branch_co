from django.contrib import admin
from reports.models import InfEconOp, ReportItems1, MiscCadrelor, ManagerMiscCadrelor, ReportItems2, ReportItems3, ReportHeader, ManagerReportDescriereaAsociati, SecondInfEconOp, ManagerInfEconOp

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
