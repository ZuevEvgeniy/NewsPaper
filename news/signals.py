from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from news.models import PostCategory
from django.core.mail import EmailMultiAlternatives
from NewsPaper import settings
from django.template.loader import render_to_string


def send_alerts (preview, pk, head_name, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            "link": f'{settings.SITE_URL}/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=head_name,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to = subscribers,
    )
    msg.attach_alternative(html_content,"text/html")
    msg.send()


#@receiver(m2m_changed, sender = PostCategory)
def alert_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscribers_emails =[]
        for c in categories:
            subscribers =c.subscribers.all()
            subscribers_emails +=[s.email for s in subscribers]

        send_alerts(instance.preview(), instance.pk, instance.head_name, subscribers_emails)
