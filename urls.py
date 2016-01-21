from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name = "index"),
	url(r'^login_simulator/$', views.login_simulator, name = "login_simulator"),
        url(r'^login_sharing_simulator/$', views.login_sharing_simulator, name = "login_sharing_simulator"),
	url(r'^logout_simulator/$', views.logout_simulator, name = "logout_simulator"),
	url(r'^interface/$', views.interface, name = "interface"),
        url(r'^sell/$', views.sell, name = "sell"),
        url(r'^sharing_sell/$', views.sharing_sell, name = "sharing_sell"),
        url(r'^buy/$', views.buy, name = 'buy'),
        url(r'^comment/$', views.comment, name = "comment"),
        url(r'^sharing_comment/$', views.sharing_comment, name = "sharing_comment"),
        url(r'^combine/$', views.combine, name = "combine"),
        url(r'^sharing_combine/$', views.sharing_combine, name = "sharing_combine"),
        url(r'^sharing_interface', views.sharing_interface, name = "sharing_interface"),
        url(r'^googlecharts/$', views.googlecharts, name = "googlecharts"),
]

