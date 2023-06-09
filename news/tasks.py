from celery import shared_task
import time
from news.models import Post, Category
import datetime
from django.core.mail import EmailMultiAlternatives
from NewsPaper import settings
from django.template.loader import render_to_string
from django.http import HttpResponse
from NewsPaper.settings import DEFAULT_FROM_EMAIL
@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")

@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)

@shared_task
def weekly_sending():
    #  Your job processing logic here...
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte = last_week)
    categories = set(posts.values_list('category__name_category', flat = True))
    subscribers = set(Category.objects.filter(name_category__in = categories).values_list('subscribers__email', flat = True))

    html_contetnt = render_to_string(
        "weekly_post.html",
        {
            'link': settings.SITE_URL,
            'posts': posts
        }

    )

    msg = EmailMultiAlternatives(
        subject=" Статьи за неделю",
        body= "",
        from_email= settings.DEFAULT_FROM_EMAIL,
        to= subscribers,
    )

    msg.attach_alternative(html_contetnt, 'text/html')
    msg.send()

    #return HttpResponse("Weekly news sent successfully!")


@shared_task
def send_email_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    title = post.head_name
    subscribers_emails = []
    for category in categories:
        subscribers_users = category.subscribers.all()
        for user in subscribers_users:
            subscribers_emails.append(user.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': post.preview,
            'link': f'{settings.SITE_URL}/news/{pk}',

        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    #return HttpResponse("New news sent successfully!")