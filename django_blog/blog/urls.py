from django.urls import path
from .views import (
    CustomLoginView, register, LogoutView, profile, edit_profile,
    PostCreateView, PostUpdateView, PostDetailView, PostDeleteView, PostListView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    search_posts, PostByTagListView
)

urlpatterns = [
    # Authentication
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", register, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # Profile
    path("profile/", profile, name="profile"),
    path("edit_profile/", edit_profile, name="edit_profile"),

    # Posts
    path("post/new/", PostCreateView.as_view(), name="new"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="detail"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="delete"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="update"),

    # Tags
    path("tags/<slug:tag_slug>/", PostByTagListView.as_view(), name="posts_by_tag"),

    # Search
    path("search/", search_posts, name="search_posts"),

    # Comments
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="new_comment"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),
]
