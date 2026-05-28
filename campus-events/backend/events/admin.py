from django.contrib import admin
from .models import Activity, Comment, Favorite, Registration

admin.site.register(Activity)
admin.site.register(Comment)
admin.site.register(Favorite)
admin.site.register(Registration)
