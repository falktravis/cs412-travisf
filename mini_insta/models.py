# File: models.py
# Author: Travis Falk(travisf@bu.edu), 9/25/2025
# Description: Model definitions for mini_insta app


from django.db import models
from django.urls import reverse

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

    def get_absolute_url(self):
        '''return URL to this profile (used after update)'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_followers(self):
        """Return a list of Profile objects who are followers of this profile."""
        # Get all Follow objects where this profile is being followed
        follows = Follow.objects.filter(profile=self)
        # Return a list of the follower profiles
        return [follow.follower_profile for follow in follows]
    
    def get_num_followers(self):
        """Return the count of followers for this profile."""
        return len(self.get_followers())
    
    def get_following(self):
        """Return a list of Profile objects that this profile is following."""
        # Get all Follow objects where this profile is the follower
        follows = Follow.objects.filter(follower_profile=self)
        # Return a list of the profiles being followed
        return [follow.profile for follow in follows]
    
    def get_num_following(self):
        """Return the count of profiles being followed by this profile."""
        return len(self.get_following())
    
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
    
    def get_all_comments(self):
        """Retrieve all comments associated with this post."""
        return Comment.objects.filter(post=self)
    
    def get_likes(self):
        """Retrieve all likes associated with this post."""
        return Like.objects.filter(post=self)
    
class Photo(models.Model):
    """Photo model to store photos associated with posts."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Reflect where the image actually lives: URL vs file
        if self.image_url:
            return f"Photo(URL) for Post {self.post.id} at {self.image_url}"
        
        return f"Photo(File) for Post {self.post.id} at {self.image_file.url}"

    def get_image_url(self):
        """Return the URL to the image regardless of storage."""
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file.url
        return ''

class Follow(models.Model):
    """Follow model to represent one profile following another."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower_profile.display_name} follows {self.profile.display_name}"

class Comment(models.Model):
    """Comment model to represent a profile's comment on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)

    def __str__(self):
        return f"Comment by {self.profile.display_name} on Post {self.post.pk}: {self.text[:50]}"

class Like(models.Model):
    """Like model to represent a profile liking a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.profile.display_name} on Post {self.post.pk}"