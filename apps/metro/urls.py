from django.urls import path
from django.conf import settings
from apps.metro.views import index, rota
from django.conf.urls.static import static

app_name = 'metro'
urlpatterns = [
    path('', index, name="index"),
    path('rota/<int:estacao_origem>/<int:estacao_destino>/', rota, name='rota'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)