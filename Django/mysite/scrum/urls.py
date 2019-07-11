from django.conf.urls import url
from scrum import views

urlpatterns = [

####Android

	url(r'^$',views.main),
	url(r'^test/',views.tryApi)

]