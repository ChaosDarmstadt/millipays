from django.conf.urls import include, url

from millipays.views import index, balance

urlpatterns = [
    url(r'^$', index.index, name='index'),
    url(r'balances$', balance.balances, name='balances'),
]
