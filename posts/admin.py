from django.contrib import admin
from .models import Posts
from django_summernote.admin import SummernoteModelAdmin


class PostsAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title', 'user', 'update_date',
                    'publication_date', 'post_category', 'published',)
    list_editable = ('published',)
    list_display_links = ('id', 'title',)
    summernote_fields = ('content', )


admin.site.register(Posts, PostsAdmin)
