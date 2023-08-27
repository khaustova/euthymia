from django.shortcuts import render

def reply_feedback(request, id):
    return render(request, 'admin/feedback_reply_form.html', )
