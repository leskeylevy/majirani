from django.db import models
from django.contrib.auth.models import User


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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.TextField(default="Anonymous")
    profile_picture = models.ImageField(upload_to='users/', default='users/user.png')
    bio = models.TextField(default="I'm using hoodwatch")
    neighbourhood = models.ForeignKey(Neighbourhood, blank=True, null=True, related_name='people')

    def __str__(self):
        return f'Profile {self.user.username}'


class Business(models.Model):
    Name = models.TextField()
    owner = models.ForeignKey(Profile)
    show_my_email = models.BooleanField(default=True)
    description = models.TextField(default='Local business')
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='business')

    @property
    def email(self):
        return self.owner.user.email


class Post(models.Model):
    user = models.ForeignKey(Profile)
    Text = models.TextField()
    neighbourhood = models.ForeignKey(Neighbourhood, related_name='posts')