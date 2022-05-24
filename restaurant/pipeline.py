from django.contrib.auth.models import Group

def add_group(backend, user, response, *args, **kwargs):
        group = Group.objects.get(name='Customer')
        user.groups.add(group)