from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from django.views.generic import ListView

from blog.models import Post, Category


class Home(View):

    def get(self, request):
       
        context = {

        }

        return render(request, 'blog/home.html', context)

class PostList(View):

    def get_queryset(self):
        return Post.objects.filter(published=True, published_date__lte=datetime.now())

    def get(self, request, category_slug=None):
        category = Category.objects.get(slug=category_slug)
        if category_slug is not None:
            posts = self.get_queryset().filter(category__slug=category_slug, category__published=True)
        else:
            posts = self.get_queryset()
        paginator = Paginator(posts, 4)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            posts = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page(paginator.num_pages)

        context = {
            'posts': posts,
            'category': category,

        }

        return render(request, 'blog/list.html', context)

class PostDetail(View):

    def get(self, request, **kwargs):
        post = get_object_or_404(Post, slug=kwargs.get("slug"))
        photoitems = post.photoitems.all()
        fileitems = post.fileitems.all()
        posts_similar = Post.objects.filter(tags__in=post.tags.all())
        context = {
            'post': post,
            'photoitems': photoitems,
            'posts_similar': posts_similar,
            'fileitems': fileitems
        }
        return render(request, 'blog/detail.html', context)