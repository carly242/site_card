from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from .managers import CustomUserManager
from django.utils.text import slugify


#User = get_user_model()


#class pour les utilisateurs 
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.urls import reverse



class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, default="Your Name")
    function = models.CharField(max_length=100, null=True, default="Function")
    email = models.EmailField(max_length=100, null=True, default="Email")
    email_bureau = models.EmailField(max_length=100, null=True, default="Office Email")
    city = models.CharField(max_length=100, null=True, default="City")
    adress_link = models.CharField(max_length=5000, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, default="Phone Number")
    office_number = models.CharField(max_length=100, null=True, default="Office Number")
    website = models.CharField(max_length=500, blank=True, null=True, default="Website")
    entreprise = models.CharField(max_length=100, null=True, default="entreprise")
    facebook = models.CharField(max_length=255, null=True, blank=True)
    twitter = models.CharField(max_length=255, null=True, blank=True)
    linkedin = models.CharField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    profile_views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.username)
            unique_slug = base_slug
            counter = 1
            while User.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_profile', kwargs={'slug': self.slug})

    def __str__(self):
        return self.username




def get_current_user(request):
    return get_user(request)

#class pour les documents
class Document(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='PDF/')
