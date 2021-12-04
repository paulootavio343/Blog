from django.db import models
from posts.models import Posts


class Comentaries(models.Model):
    post_comment = models.ForeignKey(
        Posts, on_delete=models.CASCADE, blank=False, null=False, default=1, verbose_name='Post'
    )
    name = models.CharField(
        max_length=64, blank=False, null=False, verbose_name='Nome'
    )
    email = models.EmailField(
        max_length=64, blank=False, null=False, verbose_name='E-mail'
    )
    comment_title = models.CharField(
        max_length=255, blank=False, null=False, verbose_name='Título'
    )
    message = models.TextField(
        blank=False, null=False, verbose_name='Comentário'
    )
    comment_published = models.BooleanField(
        default=False, verbose_name='Publicado'
    )
    comment_created = models.DateTimeField(
        auto_now_add=True, verbose_name='Publicação'
    )
    comment_updated = models.DateTimeField(
        auto_now=True, verbose_name='Atualização'
    )

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
