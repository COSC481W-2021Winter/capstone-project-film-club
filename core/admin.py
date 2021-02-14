from django.contrib import admin

from core.models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Review)