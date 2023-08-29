from django.contrib import admin
from django.db import transaction
from django.contrib.auth.hashers import make_password
import re
from .models import EmailSubscription, Feedback, AboutSite
from .tasks import reply_feedback


@admin.register(AboutSite)
class AboutSiteAdmin(admin.ModelAdmin):
    list_display = ('about_site'[:256],)
    

@admin.register(EmailSubscription)
class EmailSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscription_date')
    
    def save_model(self, request, obj, form, change):
        obj.email_hash = make_password(obj.email, salt=None, hasher='default')
        obj.email_hash = re.sub(r'\W', '5', obj.email_hash)
        
        while EmailSubscription.objects.filter(email_hash=obj.email_hash).exists():
            obj.email_hash = make_password(obj.email, salt=None, hasher='default')
            obj.email_hash = re.sub(r'\W', '5', obj.email_hash)
            
        super().save_model(request, obj, form, change)
    
    
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message'[:128], 'created_date', 'reply_status')
    #readonly_fields = ('name', 'email', 'message'[:50], 'created_date')
    list_filter = ('reply_status',)
    fields = ('name', 'email', 'message'[:128], 'reply')

    change_form_template = 'admingo/feedback_reply_form.html'
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['reply'] = Feedback.objects.get(id=object_id)
        
        return super(FeedbackAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
        
    def save_model(self, request, obj, form, change):
        if obj.reply:
            obj.reply_status = True
            transaction.on_commit(lambda: reply_feedback.delay(obj.name, obj.email, obj.reply))
        super().save_model(request, obj, form, change)
