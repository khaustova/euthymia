from email.headerregistry import ContentTypeHeader
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.contrib.contenttypes.models import ContentType
from .models import EmailSubscription, Feedback
from django.template.response import TemplateResponse

@admin.register(EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscription_date')
    
    
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message'[:50], 'created_date', 'reply_status')
    #readonly_fields = ('name', 'email', 'message'[:50], 'created_date')
    list_filter = ('reply_status',)
    fields = ('name', 'email', 'message'[:50], 'reply')

    change_form_template = 'manager/feedback_reply_form.html'
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['reply'] = Feedback.objects.get(id=object_id)
        return super(FeedbackAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
        
    def save_model(self, request, obj, form, change):
        if obj.reply:
            obj.reply_status = True
        super().save_model(request, obj, form, change)


    
    