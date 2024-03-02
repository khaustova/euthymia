from django import forms
from django.forms import ModelForm
from mptt.forms import TreeNodeChoiceField
from apps.manager.models import Feedback, EmailSubscription
from .models import Comment


class CommentForm(ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget.attrs.update({'class': 'comments__parent'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super().save(*args, **kwargs)

    class Meta:
        model = Comment
        fields = ('author', 'guest', 'email', 'body', 'parent')
        widgets = {
            'guest': forms.TextInput(attrs={
                'class': 'comment-form__name-field custom-input',
                'placeholder': 'Имя',
                'autocomplete': 'on',
                }
            ),
            'email': forms.EmailInput(attrs={
                'class': 'comment-form__email-field custom-input',
                'placeholder': 'E-mail',
                'autocomplete': 'on',
                }
            ),
            'body': forms.Textarea(attrs={
                'class': 'comment-form__comment-field',
                'placeholder': 'Оставьте комментарий...',
                }
            )
        }


class FeedbackForm(ModelForm):

    class Meta:
        model = Feedback
        fields = ('name', 'email', 'message')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'feedback-form__field',
                'placeholder': 'Имя',
                'autocomplete': 'on',
                }
            ),
            'email': forms.EmailInput(attrs={
                'class': 'feedback-form__field',
                'placeholder': 'E-mail',
                'autocomplete': 'on',
                }
            ),
            'message': forms.Textarea(attrs={
                'class': 'feedback-form__field',
                'placeholder': 'Написать сообщение...',
                }
            )
        }


class SubscribeForm(ModelForm):

    class Meta:
        model = EmailSubscription
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'custom-input',
                'placeholder': 'E-mail',
                'autocomplete': 'on',
                }
            ),
        }
