from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from django.db import models

from .models import Post, Category
from .forms import CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Post.objects.filter(status='published', published_at__lte=timezone.now())
        
        # Filter by category if provided
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        # Filter by tag if provided
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
            
        # Search query
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q) | queryset.filter(content__icontains=q)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).annotate(
            post_count=Count('posts', filter=models.Q(posts__status='published'))
        )
        context['recent_posts'] = Post.objects.filter(status='published').order_by('-published_at')[:5]
        
        # Add active category if filtering by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['active_category'] = get_object_or_404(Category, slug=category_slug)
            
        # Add active tag if filtering by tag
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            from taggit.models import Tag
            context['active_tag'] = get_object_or_404(Tag, slug=tag_slug)
            
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status='published', published_at__lte=timezone.now())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True).annotate(
            post_count=Count('posts', filter=models.Q(posts__status='published'))
        )
        context['recent_posts'] = Post.objects.filter(status='published').exclude(id=self.object.id).order_by('-published_at')[:5]
        context['related_posts'] = Post.objects.filter(
            category=self.object.category,
            status='published'
        ).exclude(id=self.object.id).order_by('-published_at')[:3]
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['comment_form'] = CommentForm()
        
        # Get post tags
        post_tags_ids = self.object.tags.values_list('id', flat=True)
        if post_tags_ids:
            similar_posts = Post.objects.filter(
                status='published',
                tags__in=post_tags_ids
            ).exclude(id=self.object.id)
            similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-published_at')[:3]
            context['similar_posts'] = similar_posts
            
        return context
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Your comment has been submitted and is awaiting approval.")
            return redirect('post_detail', slug=post.slug)
        
        # If form is invalid, re-render the page with form errors
        context = self.get_context_data(object=post)
        context['comment_form'] = form
        return self.render_to_response(context)