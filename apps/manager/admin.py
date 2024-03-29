import re
from django.http import HttpRequest
from django.db import transaction
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.shortcuts import reverse, redirect
from .models import EmailSubscription, Feedback, SiteSettings
from .tasks import reply_feedback


@admin.register(SiteSettings)
class SiteDescriptionAdmin(admin.ModelAdmin):

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        first_obj = self.model.objects.first()
        if first_obj is not None:
            return redirect(reverse('admin:manager_sitesettings_change', args=(first_obj.pk,)))
        return redirect(reverse('admin:manager_sitesettings_add'))


@admin.register(EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscription_date')

    def save_model(self, request: HttpRequest, obj: EmailSubscription, form, change):
        obj.email_hash = make_password(obj.email, salt=None, hasher='default')
        obj.email_hash = re.sub(r'\W', '5', obj.email_hash)

        while EmailSubscription.objects.filter(email_hash=obj.email_hash).exists():
            obj.email_hash = make_password(obj.email, salt=None, hasher='default')
            obj.email_hash = re.sub(r'\W', '5', obj.email_hash)

        super().save_model(request, obj, form, change)


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message'[:256], 'feedback_ip', 'created_date', 'reply_status')
    readonly_fields = ('name', 'email', 'message', 'created_date')
    list_filter = ('reply_status',)
    fields = ('name', 'email', 'message'[:256], 'reply')

    change_form_template = 'dashboard/feedback_reply_form.html'

    def change_view(self, request: HttpRequest, object_id: int, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['reply'] = Feedback.objects.get(id=object_id)

        return super(FeedbackAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def save_model(self, request: HttpRequest, obj: Feedback, form, change):
        if obj.reply:
            obj.reply_status = True
            transaction.on_commit(lambda: reply_feedback.delay(obj.name, obj.email, obj.reply))
        super().save_model(request, obj, form, change)
