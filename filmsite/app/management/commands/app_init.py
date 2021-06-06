from app.models import UserProfile
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission

class Command(BaseCommand):
    
    def handle(self, *args, **kwargs):
        # create superuser
        if not User.objects.filter(username='_admin').exists():
            admin_user = User.objects.create_superuser('_admin', 'admin@example.com', '_admin')
            
            profile = UserProfile(user=admin_user)
            profile.save()

        # create moderator
        moderator_user = User()
        if not User.objects.filter(username='_mod').exists():
            moderator_user = User.objects.create_user('_mod', 'mod@example.com', '_mod')
            moderator_user.is_staff = True
            moderator_user.save()
            
            profile = UserProfile(user=moderator_user)
            profile.save()
        else:
            moderator_user = User.objects.filter(username='_mod').first()
        
        # create moderator group
        moderator_group, created = Group.objects.get_or_create(name='Moderator')

        model_names = ['movie', 'actor', 'cast', 'photoactor', 'photo',]
        for model_name in model_names:        
            permissions = Permission.objects.filter(codename__contains=model_name)
            for perm in permissions:
                moderator_group.permissions.add(perm)

        moderator_group.user_set.add(moderator_user)
        
        # create user
        if not User.objects.filter(username='_user').exists():
            user = User.objects.create_user('_user', 'user@example.com', '_user')

            profile = UserProfile(user=user)
            profile.save()
