from django.conf.urls import url
from django.urls import path, re_path
from query_handler import views


urlpatterns = [
    # re_path(r'^sparql\?', views.query_handler_sparql),
    re_path(r'^sparql/$', views.query_handler_sparql),
    re_path(r'^fuzzy-query/$', views.query_handler_fuzzy_sparql),
]


