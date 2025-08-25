from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy

from .models import CustomUser, Post, Comment
from .forms import ProfileForm, CreatePostForm, CommentForm

# ----------------- Authentication -----------------
class RegistrationForm(UserCreationForm):
    """Custom user registration form with email field."""
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password1", "password2"]


def register(request):
    """Handle user registration."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})


class CustomLoginView(LoginView):
    """Custom login view using a specific template."""
    template_name = "login.html"


class CustomLogoutView(LogoutView):
    """Custom logout view redirecting to login page."""
    next_page = reverse_lazy("login")


# ----------------- Profile -----------------
@login_required
def profile(request):
    """Display the user profile."""
    return render(request, "profile.html", {"user": request.user})


@login_required
def edit_profile(request):
    """Allow users to edit their profile."""
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "edit_profile.html", {"form": form})


# ----------------- Posts -----------------
class PostListView(ListView):
    """List all blog posts."""
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    """View a single post in detail."""
    model = Post
    template_name = "post_view.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post."""
    model = Post
    form_class = CreatePostForm
    template_name = "post_create.html"
    success_url = reverse_lazy("posts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing post."""
    model = Post
    form_class = CreatePostForm
    template_name = "post_edit.html"
    success_url = reverse_lazy("posts")

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a post (only allowed by the author)."""
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("posts")

    def test_func(self):
        return self.get_object().author == self.request.user


# ----------------- Comments -----------------
class CommentCreateView(LoginRequiredMixin, CreateView):
    """Add a comment to a post."""
    model = Comment
    form_class = CommentForm
    template_name = "comment_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs.get("pk")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit a comment."""
    model = Comment
    form_class = CommentForm
    template_name = "comment_update.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a comment."""
    model = Comment
    template_name = "comment_delete.html"

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()


# ----------------- Search -----------------
@login_required
def search_posts(request):
    """Search posts by title, content, or tags."""
    query = request.GET.get("q")
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()

    return render(request, "search_results.html", {
        "results": results,
        "query": query
    })


# ----------------- Tags -----------------
from taggit.models import Tag

class PostByTagListView(ListView):
    """Display posts filtered by tag."""
    model = Post
    template_name = "posts_by_tag.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag_slug = self.kwargs.get("tag_slug")
        if tag_slug:
            return Post.objects.filter(tags__slug=tag_slug)
        return Post.objects.all()

