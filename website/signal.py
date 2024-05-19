# Dans le fichier signals.py de votre application Django

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def set_user_as_client(sender, instance, created, **kwargs):
    if created and not instance.is_superuser and not instance.is_client:
        instance.is_client = True
        instance.save()
