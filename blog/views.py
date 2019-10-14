from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView,
                                 DetailView,
                                 CreateView,
                                 UpdateView,
                                 DeleteView)
from .models import Post


# Create your views here.

def home(request):
    posts= Post.objects.all()
    return render (request,'blog/home.html',{'posts':posts})


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name='posts'
    ordering =['-date_posted']
    paginate_by = 5



class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name='posts'
    
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields =['title','content']
    template_name = 'blog/create.html'

    def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']
    template_name = 'blog/update.html'

    def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    fields =['title','content']
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

   
 

def about(request):
    return render (request,'blog/about.html')