from millipays.models import Product, Member, CashLog

from django.shortcuts import render


def balances(request):
    context = {'members': Member.objects.all()}
    return render(request, 'millipays/balances.html', context)