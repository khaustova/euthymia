from admin_auto_filters.filters import AutocompleteFilter
from django.db import transaction
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from mptt.admin import DraggableMPTTAdmin
from apps.manager.tasks import send_notification
from .models import Article, Category, Comment, UserProfile, Subcategory


class CategoryFilter(AutocompleteFilter):
    title = 'Категория'
    field_name = 'category'


class SubcategoryFilter(AutocompleteFilter):
    title = 'Подкатегория'
    field_name = 'subcategory'
    
    
class ArticleFilter(AutocompleteFilter):
    title = 'Статья'
    field_name = 'article'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = (
        'title', 
        'slug', 
        'summary', 
        'body', 
        'category', 
        'subcategory',
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
    list_filter = [
        'status',
        CategoryFilter,
        SubcategoryFilter,
    ]
    prepopulated_fields = {
       'slug': ('title',)
    }
    list_per_page = 50
    date_hierarchy = 'created_date'
    search_fields = (
        'title',
    )

    change_form_template = 'dashboard/change_form_article.html'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            transaction.on_commit(lambda: send_notification.delay(obj.pk))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {
        'slug': ('name',)
    }
    
    
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)
    search_fields = ('name',)
    list_filter = [
        CategoryFilter,
    ]


@admin.register(Comment)
class CommentAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions', 
        'indented_title', 
        'article', 
        'email', 
        'comment_ip',
        'created_date'
    )
    mptt_level_indent = 2
    list_display_links = (
        'article',
    )
    list_filter = [
        'created_date',
        ArticleFilter,
    ]


class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Дополнительная информация'


class UserAdmin(UserAdmin):
    inlines = (UserInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
