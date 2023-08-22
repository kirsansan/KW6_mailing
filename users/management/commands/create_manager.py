

from django.core.management import BaseCommand

from users.models import User
from django.contrib.auth.models import Group, Permission

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
        permission = Permission.objects.get_or_create(codename='main.add_clients')
        group.permissions.add(permission)
        group.user_set.add(user)

