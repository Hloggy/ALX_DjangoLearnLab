from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    # Add any existing fields you have
    
    # Add the following field for user relationships
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    
    def follow(self, user):
        """Follow another user"""
        if user != self and user not in self.following.all():
            self.following.add(user)
            return True
        return False
    
    def unfollow(self, user):
        """Unfollow a user"""
        if user in self.following.all():
            self.following.remove(user)
            return True
        return False
    
    def is_following(self, user):
        """Check if following a specific user"""
        return self.following.filter(id=user.id).exists()
    
    def get_following_count(self):
        """Get number of users being followed"""
        return self.following.count()
    
    def get_followers_count(self):
        """Get number of followers"""
        return self.followers.count()
    
    class Meta:
        # Add this if you want to ensure unique email addresses
        # constraints = [
        #     models.UniqueConstraint(fields=['email'], name='unique_email')
        # ]
        pass

    def __str__(self):
        return self.username

