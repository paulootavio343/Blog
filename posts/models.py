from django.db import models
from django.utils.text import slugify
from category.models import Category
import os
from PIL import Image
from Blog import settings
from django.contrib.auth import get_user_model
User = get_user_model()


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
        max_length=255, blank=False, null=False, default='Blog, Django, Bootstrap', verbose_name='Palavras chave'
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
        super().save(*args, **kwargs)

        if self.image:
            self.resize_image(self.image.name, 800)

        if not self.slug:
            new_slug = slugify(self.title)
            self.slug = new_slug

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
