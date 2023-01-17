from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from main import views as general_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', general_views.app, name='app'),
    path('app/', general_views.app, name='app'),
    path('app/introductory/', general_views.opening, name='beginning'),

    path('app/auth/', include('accounts.urls',
                              namespace='authentication_accounts')),

    path('app/auth/vendor/', include('vendors.urls', namespace="vendors")),

    path('app/auth/vendor/menu-builder/', include('menus.urls', namespace='menus')),

    path('app/market-places/', include('marketplaces.urls', namespace='marketplaces')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
