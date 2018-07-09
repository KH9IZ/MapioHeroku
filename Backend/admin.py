from django.contrib import admin

# Register your models here.
from Backend.models import Square, UserProfile

admin.site.register(Square)
admin.site.register(UserProfile)