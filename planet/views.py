# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from planet.models import Blog, Feed, Author, Post, Category
from planet.forms import SearchForm

from tagging.models import Tag, TaggedItem


from planet.models import Post, Blog, Feed, Category
from planet.serializers import PostSerializer,FeedSerializer,CategorySerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework import filters
import django_filters


class PostFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(name="category__title")

    class Meta:
        model = Post
        fields = ['category', 'cluster_id']

class PostViewSet(viewsets.ModelViewSet):
	queryset=Post.objects.all()
	serializer_class=PostSerializer
	filter_class=PostFilter
	filter_backends = (filters.OrderingFilter,)
	ordering_fields = ('rank',)
    	ordering = ('-rank',)

	


class FeedViewSet(viewsets.ModelViewSet):
	queryset=Feed.objects.all()
	serializer_class=FeedSerializer

class CategoryViewSet(viewsets.ModelViewSet):
	queryset=Category.objects.all()
	serializer_class=CategorySerializer


#def index(request):
#    posts = Post.site_objects.all().order_by("-date_modified")
#
#    return render_to_response("planet/posts/list.html", {"posts": posts},
#        context_instance=RequestContext(request))
#
#
#def blogs_list(request):
#    blogs_list = Blog.site_objects.all()
#
#    return render_to_response("planet/blogs/list.html",
#        {"blogs_list": blogs_list}, context_instance=RequestContext(request))
#
#
#def blog_detail(request, blog_id, slug=None):
#    blog = get_object_or_404(Blog, pk=blog_id)
#
#    if slug is None:
#        return redirect(blog, permanent=True)
#
#    posts = Post.site_objects.filter(feed__blog=blog).order_by("-date_modified")
#
#    return render_to_response("planet/blogs/detail.html",
#                              {"blog": blog, "posts": posts},
#        context_instance=RequestContext(request))
#
#
#def feeds_list(request):
#    feeds_list = Feed.site_objects.all()
#
#    return render_to_response("planet/feeds/list.html",
#        {"feeds_list": feeds_list}, context_instance=RequestContext(request))
#
#
#def feed_detail(request, feed_id, tag=None, slug=None):
#    feed = get_object_or_404(Feed, pk=feed_id)
#
#    if not slug:
#        return redirect(feed, permanent=True)
#
#    if tag:
#        tag = get_object_or_404(Tag, name=tag)
#
#        posts = TaggedItem.objects.get_by_model(
#            Post.site_objects, tag).filter(feed=feed).order_by("-date_modified")
#    else:
#        posts = Post.site_objects.filter(feed=feed).order_by("-date_modified")
#
#    return render_to_response("planet/feeds/detail.html",
#        {"feed": feed, "posts": posts, "tag": tag},
#        context_instance=RequestContext(request))
#
#
#def authors_list(request):
#    authors = Author.site_objects.all()
#
#    return render_to_response("planet/authors/list.html",
#        {"authors_list": authors},
#        context_instance=RequestContext(request))
#
#
#def author_detail(request, author_id, tag=None, slug=None):
#    author = get_object_or_404(Author, pk=author_id)
#
#    if not slug:
#        return redirect(author, permanent=True)
#
#    if tag:
#        tag = get_object_or_404(Tag, name=tag)
#
#        posts = TaggedItem.objects.get_by_model(Post.site_objects, tag).filter(
#            authors=author).order_by("-date_modified")
#    else:
#        posts = Post.site_objects.filter(
#            authors=author).order_by("-date_modified")
#
#    return render_to_response("planet/authors/detail.html",
#        {"author": author, "posts": posts, "tag": tag},
#        context_instance=RequestContext(request))
#
#
#def posts_list(request):
#    posts = Post.site_objects.all().select_related("feed", "blog", "authors")\
#        .order_by("-date_modified")
#
#    return render_to_response("planet/posts/list.html", {"posts": posts},
#        context_instance=RequestContext(request))
#
#
#def post_detail(request, post_id, slug=None):
#    post = get_object_or_404(
#        Post.objects.select_related("feed", "authors", "blog"), pk=post_id)
#
#    if not slug:
#        return redirect(post, permanent=True)
#
#    return render_to_response("planet/posts/detail.html", {"post": post},
#        context_instance=RequestContext(request))
#
#
#def tag_detail(request, tag):
#    tag = get_object_or_404(Tag, name=tag)
#
#    posts = TaggedItem.objects.get_by_model(
#        Post.site_objects, tag).order_by("-date_modified")
#
#    return render_to_response("planet/tags/detail.html", {"posts": posts,
#        "tag": tag}, context_instance=RequestContext(request))
#
#
#def tag_authors_list(request, tag):
#    tag = get_object_or_404(Tag, name=tag)
#
#    posts_list = TaggedItem.objects.get_by_model(Post.site_objects, tag)
#
#    authors = set()
#    for post in posts_list:
#        for author in post.authors.all():
#            authors.add(author)
#
#    return render_to_response("planet/authors/list_for_tag.html",
#        {"authors": list(authors), "tag": tag},
#        context_instance=RequestContext(request))
#
#
#def tag_feeds_list(request, tag):
#    tag = get_object_or_404(Tag, name=tag)
#
#    post_ids = TaggedItem.objects.get_by_model(Post.site_objects, tag
#        ).values_list("id", flat=True)
#
#    feeds_list = Feed.site_objects.filter(post__in=post_ids).distinct()
#
#    return render_to_response("planet/feeds/list_for_tag.html",
#        {"feeds_list": feeds_list, "tag": tag},
#        context_instance=RequestContext(request))
#
#
#def tags_cloud(request, min_posts_count=1):
#
#    tags_cloud = Tag.objects.cloud_for_model(Post)
#
#    return render_to_response("planet/tags/cloud.html",
#        {"tags_cloud": tags_cloud}, context_instance=RequestContext(request))
#
#
#def foaf(request):
#    # TODO: use http://code.google.com/p/django-foaf/ instead of this
#    feeds = Feed.site_objects.all().select_related("blog")
#
#    return render_to_response("planet/microformats/foaf.xml", {"feeds": feeds},
#        context_instance=RequestContext(request), mimetype="text/xml")
#
#
#def opml(request):
#    feeds = Feed.site_objects.all().select_related("blog")
#
#    return render_to_response("planet/microformats/opml.xml", {"feeds": feeds},
#        context_instance=RequestContext(request), mimetype="text/xml")
#
#
#def search(request):
#    if request.method == "GET" and request.GET.get("search") == "go":
#        search_form = SearchForm(request.GET)
#
#        if search_form.is_valid():
#            query = search_form.cleaned_data["q"]
#
#            if search_form.cleaned_data["w"] == "posts":
#                params_dict = {"title__icontains": query}
#
#                posts = Post.site_objects.filter(**params_dict
#                    ).distinct().order_by("-date_modified")
#
#                return render_to_response("planet/posts/list.html",
#                    {"posts": posts}, context_instance=RequestContext(request))
#
#            elif search_form.cleaned_data["w"] == "tags":
#                params_dict = {"name__icontains": query}
#
#                tags_list = Tag.objects.filter(**params_dict
#                    ).distinct().order_by("name")
#
#                return render_to_response("planet/tags/list.html",
#                    {"tags_list": tags_list},
#                    context_instance=RequestContext(request))
#
#            elif search_form.cleaned_data["w"] == "blogs":
#                params_dict = {"title__icontains": query}
#
#                blogs_list = Blog.site_objects.filter(**params_dict
#                    ).order_by("title")
#
#                return render_to_response("planet/blogs/list.html",
#                    {"blogs_list": blogs_list},
#                    context_instance=RequestContext(request))
#
#            elif search_form.cleaned_data["w"] == "feeds":
#                params_dict = {"title__icontains": query}
#
#                feeds_list = Feed.site_objects.filter(**params_dict
#                    ).order_by("title")
#
#                return render_to_response("planet/feeds/list.html",
#                    {"feeds_list": feeds_list},
#                    context_instance=RequestContext(request))
#
#            elif search_form.cleaned_data["w"] == "authors":
#                params_dict = {"name__icontains": query}
#
#                authors_list = Author.site_objects.filter(**params_dict
#                    ).order_by("name")
#
#                return render_to_response("planet/authors/list.html",
#                    {"authors_list": authors_list},
#                    context_instance=RequestContext(request))
#
#            else:
#                return HttpResponseRedirect(reverse("planet_post_list"))
#
#        else:
#            return HttpResponseRedirect(reverse("planet_post_list"))
#
#    else:
#        return HttpResponseRedirect(reverse("planet_post_list"))
