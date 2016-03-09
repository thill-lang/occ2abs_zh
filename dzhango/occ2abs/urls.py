from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^query$', views.query, name="query"),
        url(r'^people$', views.query_for_people, name="query_for_people")
]