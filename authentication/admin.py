from django.contrib import admin
import authentication.models as auth_models

# Register your models here.
admin.site.register(auth_models.User)
admin.site.register(auth_models.PrivateChat)
admin.site.register(auth_models.Group)
admin.site.register(auth_models.GroupMessage)
admin.site.register(auth_models.Friendship)