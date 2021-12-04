from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    category_name = models.CharField(
        max_length=64, unique=True, default='category', verbose_name='Nome')
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
