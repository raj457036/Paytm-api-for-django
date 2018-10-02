from django.contrib import admin
from .models import PaytmDataBase #,PaytmRefundDataBase
# Register your models here.

class PaytmDataBaseAdmin(admin.ModelAdmin):
    list_display = ('order_id','amount', 'txn_id')

admin.site.register(PaytmDataBase, PaytmDataBaseAdmin)
# admin.site.register(PaytmRefundDataBase)
