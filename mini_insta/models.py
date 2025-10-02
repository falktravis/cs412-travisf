# File: models.py
# Author: Travis Falk(travisf@bu.edu), 9/25/2025
# Description: Model definitions for mini_insta app


from django.db import models

# Create your models here.
class Profile(models.Model):
    """Profile model to store user profile information."""
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.display_name} (@{self.username})"
    
    def get_all_posts(self):
        """Retrieve all posts associated with this profile as a QuerySet containing posts."""
        return Post.objects.filter(profile=self)
    
class Post(models.Model):
    """Post model to store user posts."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Post by {self.profile.display_name} at {self.timestamp}"
    
    def get_all_photos(self):
        """Retrieve all photos associated with this post as a QuerySet containing photos."""
        return Photo.objects.filter(post=self)
    
class Photo(models.Model):
    """Photo model to store photos associated with posts."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for Post ID {self.post.id} at {self.timestamp}"