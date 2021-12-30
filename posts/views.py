#Python
from typing import Dict, Any

#Django
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

#Models
from posts.models import Post

#Posts
from posts.forms import PostForm

class PostFeedView(LoginRequiredMixin, ListView):
    template_name = "posts/feed.html"
    model = Post
    ordering = ('-created')
    paginate_by = 10
    context_object_name = 'posts'

class PostDetailView(LoginRequiredMixin, DetailView):
    template_name = 'posts/detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'

class CreatePostView(LoginRequiredMixin, CreateView):
    template_name = 'posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts/feed')

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['profile'] = self.request.user.profile
        return context
