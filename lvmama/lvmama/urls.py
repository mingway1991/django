import django
from django.conf.urls import url, include
from django.contrib import admin
from lvmamaios.views import signin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^lvmamaios/', include('lvmamaios.urls')),
    url(r'^signin/', signin),
]
