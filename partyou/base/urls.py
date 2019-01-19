from django.urls import path

from partyou.base.views import home, contato

app_name = 'base'
urlpatterns = [
    path('', home, name='home'),
    path('contato/', contato, name='contato'),
]
