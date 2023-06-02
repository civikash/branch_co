from django.contrib import admin
from reports.models import InfEconOp, SecondInfEconOp, ManagerInfEconOp

@admin.register(ManagerInfEconOp)
class AccountAdmin(admin.ModelAdmin):
    pass

@admin.register(InfEconOp)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(SecondInfEconOp)
class AccountAdmin(admin.ModelAdmin):
    pass
