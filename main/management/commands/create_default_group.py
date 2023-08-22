"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['operators', 'content']
MODELS = ['mailing list', 'message', 'mailing effort', 'Client', 'blog']
PERMISSIONS = ['view', 'change', 'delete', 'add']


class Command(BaseCommand):

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = 'Can {} {}'.format(permission, model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        print("Permission not found with name '{}'.".format(name))
                        continue

                    new_group.permissions.add(model_add_perm)
