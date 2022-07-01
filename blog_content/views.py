from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from .models import Posts, Category, Comentaries
from .forms import FormComentario
from django.db.models import Q, Count, Case, When
import requests
from Blog import settings


class PostIndex(ListView):
    template_name = 'index.html'
    paginate_by = 9
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

    def get_queryset(self):
        qs = super().get_queryset()
        qs = Posts.objects.filter(published=True).order_by('-id')
        return qs

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        post = self.get_object()
        comentarios = Comentaries.objects.filter(
            post_comment=post.id, comment_published=True).order_by('-id')
        contexto['comments'] = comentarios

        return contexto

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
            return redirect('blog_content:details', pk=post.pk, slug=post.slug)

        comentario.save()
        messages.success(
            self.request, 'Comentário enviado para revisão com sucesso.')
        return redirect('blog_content:details', pk=post.pk, slug=post.slug)


class PostCategory(PostIndex):
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()

        category = self.kwargs.get('category_slug', None)
        category = Category.objects.get(category_slug=category)

        if not category:
            return qs

        qs = qs.filter(post_category=category.id,
                       published=True).order_by('-id')

        return qs


class PostSearch(PostIndex):
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.GET.get('search')

        if not search:
            return qs

        qs = qs.filter(
            Q(title__icontains=search) |
            Q(slug__icontains=search) |
            Q(user__first_name__iexact=search) |
            Q(content__icontains=search) |
            Q(excerpt__icontains=search) |
            Q(keywords__icontains=search) |
            Q(post_category__category_name__icontains=search) |
            Q(post_category__category_slug__icontains=search) |
            Q(publication_date__icontains=search) |
            Q(update_date__icontains=search)
        ).order_by('-id')

        return qs
