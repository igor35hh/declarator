from django.urls import path, re_path
from declarator.views import OfficeListView

app_name = 'declarator'


urlpatterns = [
    re_path(r'^$', OfficeListView.as_view(), name='offises_list'),
    re_path(r'^office/(?P<office_id>\d+)/(?P<parent_id>\d{1})/$',\
            OfficeListView.as_view(), name='offise_by_id'),
]
