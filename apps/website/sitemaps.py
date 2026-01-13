from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.website.models import Article


class ArticleSitemap(Sitemap):
    """Карта сайта для статей."""
    
    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj: Article):
        return obj.updated_date

    
class StaticSitemap(Sitemap):
    """Карта сайта для статичных страниц."""
    
    def items(self):
        return ['index', 'hot_index']

    def location(self, item):
        return reverse(f'website:{item}')
