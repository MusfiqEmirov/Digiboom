from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(f'{settings.ADMIN_URL}', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('core.urls')),
]

handler404 = 'core.views.page_not_found'

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
