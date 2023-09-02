from django.db import transaction
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from mptt.admin import DraggableMPTTAdmin
from manager.tasks import send_notification
from .models import Article, Category, Comment, UserProfile


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'views', 'updated_date')
    list_display_links = ('title',)
    list_filter = ('category',)
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ('next_article', 'prev_article', 'category')
    list_per_page = 50
    date_hierarchy = 'created_date'
    search_fields = ('title',)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            transaction.on_commit(lambda: send_notification.delay(obj.pk))
    
    
@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title',)
    search_fields = ('name',)
    mptt_level_indent = 2
    

@admin.register(Comment)
class CommentAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'article', 'email', 'created_date')
    mptt_level_indent = 2
    list_display_links = ('article',)
    list_filter = ('created_date',)
    
    
class UserInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Дополнительная информация'
 
 
class UserAdmin(UserAdmin):
    inlines = (UserInline, )
 
 
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
    