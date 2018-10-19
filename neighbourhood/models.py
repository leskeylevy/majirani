from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    dp = models.ImageField(upload_to='images')
    career = models.CharField(max_length=100)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile(cls, id):
        profile = cls.objects.all()
        return profile

    @classmethod
    def update_profile(cls, id, update):
        profile_update = cls.objects.filter(id=id).update(profile=update)
        return profile_update

    def __str__(self):
        return self.user.username
