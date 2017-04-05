from django.conf.urls import url

from .views import *

app_name = 'ana'
urlpatterns = [
    url(r'^data', analyse_data),
    url(r'^newspec', analyse_newspec),
    url(r'^list-all', analyse_data_list_all),
]
