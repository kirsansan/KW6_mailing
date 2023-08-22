

from django.core.management import BaseCommand

from KW6_mailing import settings
from main.models import Client
from users.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='manager@example.com',
            first_name='manager',
            last_name='manager_last',
            is_staff=True,
            is_superuser=False)
        user.set_password('12345')
        user.save()
        group = Group.objects.create(name='Managers')
        content_type1 = ContentType.objects.get_for_model(Client)
        permission1, __ = Permission.objects.get_or_create(codename='main.add_client',
                                                          name='Can add clients',
                                                          content_type=content_type1)
        content_type2 = ContentType.objects.get_for_model(User)
        permission2 = Permission.objects.get(codename='change_user',
                                                          content_type=content_type2)
        group.permissions.add(permission1)
        group.permissions.add(permission2)
        group.user_set.add(user)

