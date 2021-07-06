from django.conf.urls import url
from todo import views

urlpatterns = [
    url(r'^api/todo$', views.todo_list),
    url(r'^api/todo/(?P<pk>[0-9]+)$', views.todo_detail),
]
