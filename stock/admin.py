from django.contrib import admin

from stock.models import CustomUser
from stock.models import Stock

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_superuser', 'id', 'id_employee', 'email')
    search_fields = ('username', 'email')
    list_filter = ('date_joined',)
    ordering = ('username',) 

admin.site.register(CustomUser, CustomerAdmin)
admin.site.register(Stock)
