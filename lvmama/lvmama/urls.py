import django
from django.conf.urls import url, include
from django.contrib import admin
from lvmamaios.views import *
from django.conf.urls import handler403, handler404, handler500

handler403 = permission_denied
handler404 = page_not_found
handler500 = page_error

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^lvmamaios/', include('lvmamaios.urls')),
    url(r'^signin/', signin),
]

# from wiki.urls import get_pattern as get_wiki_pattern
# from django_nyt.urls import get_pattern as get_nyt_pattern
# urlpatterns += [
#     url(r'^notifications/', get_nyt_pattern()),
#     url(r'', get_wiki_pattern())
# ]