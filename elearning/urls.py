from django.conf.urls import url
from elearning import views

urlpatterns = [
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^register$',views.register),
    url(r'^tree$',views.tree),
    url(r'^node/(?P<node_id>\w+)/homework$',views.HomeworkView.as_view()),
    url(r'^node/(?P<node_id>\w+)/homeworkanswer$',views.HomeworkAnswerView.as_view()),
    url(r'^node/(?P<node_id>\w+)/materials$',views.get_materials),
    url(r'^node/(?P<node_id>\w+)/material$',views.MaterialFileUploadView.as_view()),
    url(r'^node/(?P<node_id>\w+)/material/(?P<material_id>\w+)$',views.MaterialFileDownloadView.as_view()),


]