from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post

# --- Home Page ---
class HomePageView(TemplateView):
    template_name = 'app/home.html'

# --- About Page ---
class AboutPageView(TemplateView):
    template_name = 'app/about.html'

# --- Blog List ---
class BlogListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'app/blog_list.html'

# --- Blog Detail ---
class BlogDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/blog_detail.html'

# --- Blog Create ---
class BlogCreateView(CreateView):
    model = Post
    fields = ['title', 'author', 'body']
    template_name = 'app/blog_create.html'
    success_url = reverse_lazy('blog')

# --- Blog Update ---
class BlogUpdateView(UpdateView):
    model = Post
    fields = ['title', 'body']
    template_name = 'app/blog_update.html'
    success_url = reverse_lazy('blog')

# --- Blog Delete ---
class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'app/blog_delete.html'
    success_url = reverse_lazy('blog')