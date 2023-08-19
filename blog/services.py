from django.core.mail import send_mail

from KW6_mailing import settings
from blog.models import Blog
from config.config import THRESHOLD_VIEW_FOR_EMAIL

def send_mail_to_admin(blog_pk):
    article = Blog.objects.get(pk=blog_pk)

    # print(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    send_mail(
        'Congratulations!',
        f"Article {article.title} has been published and counter of views has been more then {THRESHOLD_VIEW_FOR_EMAIL} now",
        settings.EMAIL_HOST_USER,
        ['kirill_home@mail.ru'])
