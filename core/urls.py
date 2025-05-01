from django.contrib import admin
from django.views.generic.base import TemplateView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.blog.sitemaps import StaticSitemap, ArticleSitemap


def page_not_found_handler(request: HttpRequest, exception=None) -> HttpResponse:
    return render(request, 'blog/404.html', status=404)


def server_error_handler(request: HttpRequest, exception=None) -> HttpResponse:
    return render(request, 'blog/500.html', status=500)


handler404 = page_not_found_handler
handler500 = server_error_handler

sitemaps = {
    'static': StaticSitemap,
    'articles': ArticleSitemap,
}

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('apps.blog.urls')),
    path(
        'sitemap.xml', 
        sitemap, {'sitemaps': sitemaps}, 
        name='django.contrib.sitemaps.views.sitemap'
    ),
    path(
        'robots.txt',
        TemplateView.as_view(template_name='blog/robots.txt', content_type='text/plain'),
    ),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
