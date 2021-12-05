from django.db import models
from django.utils.text import slugify
import os
from PIL import Image
from Blog import settings
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    category_name = models.CharField(
        max_length=64, unique=True, verbose_name='Nome')
    category_slug = models.SlugField(
        blank=True, null=True, unique=True, verbose_name='Slug')

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.category_slug:
            new_slug = slugify(self.category_name)
            self.category_slug = new_slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Posts(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Usuário'
    )
    post_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Categoria'
    )
    title = models.CharField(
        max_length=64, blank=False, null=False, verbose_name='Título'
    )
    excerpt = models.CharField(
        max_length=255, blank=False, null=False, verbose_name='Excerto'
    )
    keywords = models.CharField(
        max_length=255, blank=False, null=False, verbose_name='Palavras chave'
    )
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField(
        blank=False, null=False, verbose_name='Conteúdo'
    )
    image = models.ImageField(
        blank=True, null=True, upload_to='post_img/%Y/%m/%d', verbose_name='Imagem'
    )
    publication_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Publicação'
    )
    update_date = models.DateTimeField(
        auto_now=True, verbose_name='Atualização'
    )
    published = models.BooleanField(default=False, verbose_name='Publicado')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.title)
            self.slug = new_slug

        super().save(*args, **kwargs)

        if self.image:
            self.resize_image(self.image.name, 800)

    @staticmethod
    def resize_image(img_name, new_width):
        img_path = os.path.join(settings.MEDIA_ROOT, img_name)
        img = Image.open(img_path)
        width, height = img.size
        new_height = round((new_width * height) / width)

        if width <= new_width:
            img.close()
            return

        new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        new_img.save(
            img_path,
            optimize=True,
            quality=60
        )
        new_img.close()

    class Meta:
        verbose_name = 'Postagem'
        verbose_name_plural = 'Postagens'


class Comentaries(models.Model):
    post_comment = models.ForeignKey(
        Posts, on_delete=models.CASCADE, blank=False, null=False, verbose_name='Post'
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
