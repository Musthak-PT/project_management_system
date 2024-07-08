from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.core.mail import  get_connection
from project_management import settings
import threading

class SendEmails:
    
    def __init__(self, *args, **kwargs):
        pass
    
    def sendTemplateEmail(self, subject, request, context, template, email_host, user_email):
        sending_status = False
        sender_name = settings.EMAIL_SENDER_NAME

        try:
            connection        = get_connection()
            connection.open()
            context           = context
            image             = request.build_absolute_uri("/")
            # Social-Logo

            html_content      = render_to_string(str(template), {'context':context})
            text_content      = strip_tags(html_content)
            send_e            = EmailMultiAlternatives(subject, text_content, f'{sender_name} <{context["email"]}>', [context["email"]], connection=connection)
            send_e.attach_alternative(html_content, "text/html")
            
            send_e.send()
            connection.close()
            sending_status    = True
        except Exception as es:
            pass
        return sending_status


from django.template.loader import get_template
template_path = 'notifications/templates/mail.html'
full_template_path = settings.BASE_DIR / template_path 
template = get_template(full_template_path)


def send_email_notification(request, instance):
    try:
        admin_email = settings.ADMIN_MAIL
        subject = "Task Notification"
        context = {
            'email'         : admin_email,
            'user_email'    : instance.user.email,
            'message'       : instance.message,
            'domain'        : settings.EMAIL_DOMAIN,
            'protocol'      : 'https',
        }

        send_email = SendEmails()
        x = threading.Thread(target=send_email.sendTemplateEmail, args=(subject, request, context, template, settings.EMAIL_HOST_USER, admin_email))
        x.start()
    except Exception as es:
        print(">>>>>>>>>>>>>>send mail>>>>>>>>>>>>>>>",es)
        pass