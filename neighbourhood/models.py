from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Neighbourhood(models.Model):
    Name = models.TextField()
    display = models.ImageField(upload_to='groups/', default='groups/group.png')
    admin = models.ForeignKey("Profile", related_name='hoods')
    description = models.TextField(default='Random group')
    police = models.TextField(default="999")
    health = models.TextField(default="213")

    def __str__(self):
        return self.Name


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    Name = models.TextField(default="Anonymous")
    dp = models.ImageField(upload_to='users/', default='users/thanos.jpg')
    bio = models.TextField(default="I'm using majirani")
    neighbourhood = models.ForeignKey(Neighbourhood, blank=True, null=True, related_name='people')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return f'Profile {self.user.username}'


class Business(models.Model):
    business_name = models.TextField()
    owner = models.ForeignKey(Profile)
    show_my_email = models.BooleanField(default=True)
    description = models.TextField(default='Local business')
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='business')

    @property
    def email(self):
        return self.owner.user.email


class Post(models.Model):
    user = models.ForeignKey(Profile)
    Text = models.CharField(max_length=250)
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='posts')


class Location(models.Model):
    name = models.CharField(max_length=30)


    def save_location(self):
        self.save()

    def delete_location(self):
        self.delete()

    def __str__(self):
        return self.name