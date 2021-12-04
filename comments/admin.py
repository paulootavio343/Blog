from django.contrib import admin
from .models import Comentaries


class ComentariesAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'comment_title', 'post_comment',
                    'comment_created', 'comment_updated', 'comment_published')
    list_editable = ('comment_published',)
    list_display_links = ('id', 'email', 'comment_title')


admin.site.register(Comentaries, ComentariesAdmin)
