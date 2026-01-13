from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from mptt.admin import DraggableMPTTAdmin
from .models import Article, Category, Comment, UserProfile, Subcategory, SiteSettings


class CategoryFilter(AutocompleteFilter):
    """Фильтр категорий с автодополнением."""
    
    title = 'Категория'
    field_name = 'category'


class SubcategoryFilter(AutocompleteFilter):
    """Фильтр подкатегорий с автодополнением."""

    title = 'Подкатегория'
    field_name = 'subcategory'


class ArticleFilter(AutocompleteFilter):
    """Фильтр статей с автодополнением."""
    
    title = 'Статья'
    field_name = 'article'
    
    
@admin.register(SiteSettings)
class SiteDescriptionAdmin(admin.ModelAdmin):
    """Настройки администрирования модели настроек сайта SiteSettings.

    Реализует паттерн синглтон:
    - если объект не существует, то открывается форма создания;
    - если объект существует, то открывается его форма редактирования.
    """

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        first_obj = self.model.objects.first()
        if first_obj is not None:
            return redirect(reverse('admin:website_sitesettings_change', args=(first_obj.pk,)))
        return redirect(reverse('admin:website_sitesettings_add'))


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Настройки администрирования модели статьи Article.

    Особенности:
    - поля формы редактирования статьи;
    - отображаемые колонки в списке;
    - фильтр по категории и подкатегории;
    - автогенерация слага;
    - поиск по заголовку.
    """
    
    fields = (
        'title', 
        'slug',
        'summary', 
        'body', 
        'category', 
        'subcategory',
        'created_date',
        'description',
        'status',
    )
    list_display = (
        'title', 
        'category', 
        'subcategory', 
        'views', 
        'updated_date',
        'status',
    )
    list_display_links = ('title',)
    list_filter = ['status', CategoryFilter, SubcategoryFilter]
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 100
    date_hierarchy = 'created_date'
    search_fields = ('title',)

    change_form_template = 'dashboard/change_form_article.html'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройки администрирования модели категории Category.

    Особенности:
    - поиск категории по названию;
    - автогенерация слага.
    """
    
    list_display = ('name', 'type')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['type',]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """Настройки администрирования модели подкатегории Subcategory.

    Особенности:
    - поиск подкатегории по названию;
    - фильтр по категории;
    - автогенерация слага.
    """
    
    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = [CategoryFilter,]


@admin.register(Comment)
class CommentAdmin(DraggableMPTTAdmin):
    """Настройки администрирования модели комментариев Comment.

    Особенности:
    - вложенные комментарии;
    - перетаскивание для изменения иерархии;
    - фильтр по дате создания и статье.
    """
    
    list_display = (
        'tree_actions', 
        'indented_title', 
        'article', 
        'email', 
        'comment_ip',
        'created_date'
    )
    mptt_level_indent = 2
    list_display_links = ('article',)
    list_filter = ['created_date', ArticleFilter]


class UserInline(admin.StackedInline):
    """Модель для отображения и редактирования профиля пользователя
    непосредственно в административной форме пользователя.
    """
    
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Дополнительная информация'


class UserAdmin(UserAdmin):
    """Расширенная административная панель пользователя.

    Добавляет связанную модель UserProfile
    в форму редактирования стандартного пользователя.
    """
    
    inlines = (UserInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
