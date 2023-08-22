"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from main.models import Client
from users.models import User

GROUPS1 = ['operators']
MODELS1 = ['mailing list', 'message', 'mailing efforts log', 'Client', 'blog']
PERMISSIONS1 = ['view', 'change', 'delete', 'add']

GROUPS2 = ['contents']
MODELS2 = ['blog']
PERMISSIONS2 = ['view', 'change', 'delete', 'add']

GROUPS3 = ['managers']
MODELS3 = ['user', 'Client']
PERMISSIONS3 = ['view', 'change']


class Command(BaseCommand):

    def handle(self, *args, **options):
        # groups creating
        self.create_permission_for_group(GROUPS1, MODELS1, PERMISSIONS1)
        self.create_permission_for_group(GROUPS2, MODELS2, PERMISSIONS2)
        self.create_permission_for_group(GROUPS3, MODELS3, PERMISSIONS3)
        # add manager
        user = User.objects.create(
            email='manager@example.com',
            first_name='manager_first',
            last_name='manager_last',
            is_staff=True,
            is_superuser=False)
        user.set_password('1234')
        user.save()
        group = Group.objects.get(name='managers')
        group.user_set.add(user)
        # add easy user
        user = User.objects.create(
            email='test@example.com',
            first_name='test_first',
            last_name='test_last',
            is_staff=True,
            is_superuser=False)
        user.set_password('123')
        user.save()

    @staticmethod
    def create_permission_for_group(groups, models, permissions):
        for group in groups:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in models:
                for permission in permissions:
                    name = 'Can {} {}'.format(permission, model)
                    print("Creating {}".format(name))
                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        print("Permission not found with name '{}'.".format(name))
                        continue
                    new_group.permissions.add(model_add_perm)
