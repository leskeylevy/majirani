from django.contrib import admin
from .models import Profile,Neighbourhood, Business

# Register your models here.
admin.site.register(Neighbourhood)
admin.site.register(Profile)
admin.site.register(Business)