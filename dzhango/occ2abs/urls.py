from django.conf.urls import url
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
        url(r'^query/(?P<lang>zh)$', views.query, name="queryzh"),
        url(r'^query/(?P<lang>(ar|ja))$', views.query, name="queryother"),
        url(r'^query/people$', views.query_for_people, name="query_for_people"),
        url(r'^query(?P<lang>.*)$', views.query, name="defaulttozh")
]