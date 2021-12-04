from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from .models import Posts
from category.models import Category
from comments.models import Comentaries
from django.db.models import Q, Count, Case, When
from comments.forms import FormComentario
from comments.models import Comentaries
import requests
from Blog import settings


class PostIndex(ListView):
    template_name = 'index.html'
    paginate_by = 6
    model = Posts
    context_object_name = 'posts'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = Posts.objects.filter(published=True).order_by('-id')
        qs = qs.annotate(
            comments_numbers=Count(
                Case(
                    When(comentaries__comment_published=True, then=1)
                )
            )
        )

        return qs


class PostDetail(UpdateView):
    template_name = 'detalhes.html'
    model = Posts
    form_class = FormComentario
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentaries.objects.filter(
            post_comment=post.id, comment_published=True).order_by('-id')
        contexto['comments'] = comentarios

        return contexto

    def get_queryset(self):
        qs = super().get_queryset()
        qs = Posts.objects.filter(published=True).order_by('-id')
        return qs

    def form_valid(self, form):
        post = self.get_object()
        comentario = Comentaries(**form.cleaned_data)
        comentario.post_comment = post

        recaptcha_response = self.request.POST['g-recaptcha-response']

        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
        )
        recaptcha_result = recaptcha_request.json()

        if not recaptcha_result.get('success'):
            messages.error(
                self.request, 'Confirme que você não é um robô clicando no reCaptcha.')
            return redirect('posts:details', pk=post.pk, slug=post.slug)

        comentario.save()
        messages.success(
            self.request, 'Comentário enviado para revisão com sucesso.')
        return redirect('posts:details', pk=post.pk, slug=post.slug)


class PostCategory(PostIndex):
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()

        categoria = self.kwargs.get('category_slug', None)
        categoria = Category.objects.get(category_slug=categoria)

        if not categoria:
            return qs

        qs = qs.filter(post_category=categoria.id,
                       published=True).order_by('-id')

        return qs


class PostSearch(PostIndex):
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        termo = self.request.GET.get('termo')

        if not termo:
            return qs

        qs = qs.filter(
            Q(title__icontains=termo) |
            Q(slug__icontains=termo) |
            Q(user__first_name__iexact=termo) |
            Q(content__icontains=termo) |
            Q(post_category__category_name__icontains=termo) |
            Q(post_category__category_slug__icontains=termo) |
            Q(publication_date__icontains=termo) |
            Q(update_date__icontains=termo)
        ).order_by('-id')

        return qs
