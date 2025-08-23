from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q

from .models import CustomUser, Post, Comment
from .forms import ProfileForm, CreatePostForm, CommentForm


# ----------------- Authentication -----------------
class RegistrationForm(UserCreationForm):
    """Custom user registration form with email field."""
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ["email"]


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


class CustomLoginView(AuthLoginView):
    """Custom login view using a specific template."""
    template_name = "login.html"


# ----------------- Profile -----------------
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


@login_required
def profile(request):
    """Display the user profile."""
    return render(request, "profile.html", {"user": request.user})


# ----------------- Posts -----------------
class PostListView(ListView):
    """List all blog posts."""
    model = Post
    template_name = "post_list.html"


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
    success_url = "/list/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    """Update an existing post."""
    model = Post
    template_name = "post_edit.html"


class PostDeleteView(UserPassesTestMixin, DeleteView):
    """Delete a post (only allowed by the author)."""
    model = Post
    context_object_name = "post"
    template_name = "post_delete.html"
    success_url = "/list/"

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
        return super().form_valid(form)


class CommentUpdateView(UpdateView):
    """Edit a comment."""
    model = Comment
    template_name = "comment_update.html"


class CommentDeleteView(DeleteView):
    """Delete a comment."""
    model = Comment
    template_name = "comment_delete.html"


# ----------------- Search -----------------
@login_required
def search_posts(request):
    """
    Search posts by title, content, or tags.
    Uses Q objects for flexible filtering.
    """
    query = request.GET.get("q")
    results = []

    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags_name_icontains=query)
        ).distinct()

    return render(request, "search_results.html", {
        "results": results,
        "query": query
    })
