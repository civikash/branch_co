from django.contrib import admin
from account.models import User

@admin.register(User)
class AccountAdmin(admin.ModelAdmin):
    pass