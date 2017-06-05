import django
from django.conf.urls import url, include
from django.contrib import admin
from lvmamaios.views import signin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^lvmamaios/', include('lvmamaios.urls')),
    url(r'^signin/', signin),
]

from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern
urlpatterns += [
    url(r'^notifications/', get_nyt_pattern()),
    url(r'', get_wiki_pattern())
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)