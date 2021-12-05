from .models import Comentaries
from .models import Category
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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'category_slug')
    list_display_links = ('id', 'category_name')


admin.site.register(Category, CategoryAdmin)


class ComentariesAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'comment_title', 'post_comment',
                    'comment_created', 'comment_updated', 'comment_published')
    list_editable = ('comment_published',)
    list_display_links = ('id', 'email', 'comment_title')


admin.site.register(Comentaries, ComentariesAdmin)
