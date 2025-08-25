from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.conf import settings


# ---------------- Custom User ----------------
class CustomUserManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    # Keep username as primary login
    email = models.EmailField(unique=True, blank=True, null=True)

    # Avoid clashes with auth.User
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username


# ---------------- Profile ----------------
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    picture = models.URLField(max_length=200, blank=True, null=True)


# ---------------- Tags ----------------
class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# ---------------- Posts ----------------
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


# ---------------- Comments ----------------
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} on {self.post}"

