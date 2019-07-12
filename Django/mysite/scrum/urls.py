from django.conf.urls import url
from scrum import views

urlpatterns = [

####web

	url(r'^$',views.main),
	url(r'^recording/',views.playRecording),
	url(r'^login/', views.get_login_page),
	url(r'^logincheck/', views.get_login_page),
	url(r'^register/', views.get_register_page),

	# android
	url(r'^recording/', views.getRecording),
	url(r'^verify/', views.login_check),
	url(r'^createuser/', views.createSuperUser),

]