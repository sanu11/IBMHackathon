from django.conf.urls import url
from scrum import views

urlpatterns = [

####Android

	url(r'^$',views.main),
	url(r'^recording/',views.getRecording),
	url(r'^play/',views.playRecording),
	url(r'^login/', views.get_login_page),

]