from django.contrib import admin
from app.models import *

class MovieAdmin(admin.ModelAdmin):
    pass

class OpinionAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

class PhotoAdmin(admin.ModelAdmin):
    pass

class ActorAdmin(admin.ModelAdmin):
    pass

class PhotoActorAdmin(admin.ModelAdmin):
    pass

class CastAdmin(admin.ModelAdmin):
    pass

class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(Movie, MovieAdmin)
admin.site.register(Opinion, OpinionAdmin)
admin.site.register(Post, CommentAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(PhotoActor, PhotoActorAdmin)
admin.site.register(Cast, CastAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
