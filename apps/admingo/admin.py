from django.db import transaction
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import path
from mptt.admin import DraggableMPTTAdmin
from manager.tasks import send_notification
from .models import Notification


@admin.action(description="Отметить как прочитанное")
def make_read(modeladmin, request, queryset):
    queryset.update(read=True)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notifications_message', 'read')
    list_per_page = 50
    actions = [make_read]
    
    change_list_template = 'admingo/notifications.html'
    
    def get_urls(self):
        urls = super().get_urls()
        read_url = [path("set_read/", self.admin_site.admin_view(self.set_read))]
        delete_url = [path("delete_all/", self.admin_site.admin_view(self.delete_all))]
        return read_url + delete_url + urls

    def set_read(self, request):
        Notification.objects.all().update(read=True)
        self.message_user(request, "Все уведомления отмечены как прочитанные.")
        return HttpResponseRedirect("../")

    
    def delete_all(self, request):
        Notification.objects.all().delete()
        self.message_user(request, "Все уведомления удалены.")
        return HttpResponseRedirect("../")
    
    
