from django.contrib import admin
from django.utils import timezone

from millipays.models import Member, Product, CashLog

# Register your models here.

admin.site.register(Product)
admin.site.register(CashLog)


class PrepaidAdmin(admin.ModelAdmin):
    list_display = ['nick', 'addPrepaid', 'balance', 'number', 'consume']
    list_editable = ['addPrepaid']
    ordering = ['nick']

    def save_model(self, request, obj, form, change):
        if not obj.addPrepaid == 0:
            cs = CashLog(member=obj, product=Product.objects.get(name='Prepaid'),
                         count=1, price=-obj.addPrepaid, purchase_date=timezone.now())
            cs.save()
            obj.balance += obj.addPrepaid
            obj.addPrepaid = 0
        obj.save()

admin.site.register(Member, PrepaidAdmin)
