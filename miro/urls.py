from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.screen_saver_view, name='screen_saver_view'),
    url(r'^ir_input/$', views.ir_input_view, name='ir_input_view'),
    url(r'^login/$',views.login_view,name = 'login_view'),
    url(r'^join/$',views.regist_view, name='regist_view'),
    url(r'^clock/$',views.clock,name='clock'),
    url(r'^logout/$',views.logout_view,name='logout_view'),
    url(r'^face_reg/$',views.face_reg_view,name='face_reg_view'),
    url(r'^face_login/$',views.face_login_view,name='face_login_view'),
    url(r'^choice_face/$',views.choice_face,name='choice_face'),
    url(r'^admin/', admin.site.urls),
    url(r'^message/$',views.message_view,name='message_view'),
    url(r'^schedule/$',views.schedule_view,name='schedule_view'),
    url(r'^store/$',views.store_view,name='store_view'),
    url(r'^subway/$',views.subway_view,name='subway_view'),
]
