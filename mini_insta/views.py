# File: views.py
# Author: Travis Falk(travisf@bu.edu), 9/25/2025
# Description: View definitions for mini_insta app

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.shortcuts import render, redirect
from .models import Profile, Post, Photo, Follow, Like
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.
class CustomLoginRequiredMixin(LoginRequiredMixin):
    '''Custom mixin to require login and provide helper methods.'''
    
    def get_login_url(self) -> str:
        '''Return the URL required for login.'''
        return reverse('login')
    
    def get_profile(self):
        '''Return the Profile for the logged in user.'''
        return Profile.objects.get(user=self.request.user)

class ProfileListView(ListView):
    '''Define a view to list all profiles'''

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        """Add viewer_profile for navbar links when authenticated."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['viewer_profile'] = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                context['viewer_profile'] = None
        else:
            context['viewer_profile'] = None
        return context

class ProfileDetailView(DetailView):
    '''Define a view to show profile details'''

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        """Add flags related to the viewing user for template logic."""
        context = super().get_context_data(**kwargs)
        # Determine if logged-in user follows this profile
        if self.request.user.is_authenticated:
            try:
                viewer_profile = Profile.objects.get(user=self.request.user)
                context['viewer_profile'] = viewer_profile
                context['is_following'] = Follow.objects.filter(
                    profile=self.object,
                    follower_profile=viewer_profile
                ).exists()
            except Profile.DoesNotExist:
                context['viewer_profile'] = None
                context['is_following'] = False
        else:
            context['viewer_profile'] = None
            context['is_following'] = False
        return context

class PostDetailView(DetailView):
    '''Define a view to show post details'''

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Add flags for ownership and like status to the context."""
        context = super().get_context_data(**kwargs)
        is_owner = False
        is_liked = False
        if self.request.user.is_authenticated:
            try:
                viewer_profile = Profile.objects.get(user=self.request.user)
                is_owner = (self.object.profile == viewer_profile)
                is_liked = Like.objects.filter(post=self.object, profile=viewer_profile).exists()
                context['viewer_profile'] = viewer_profile
            except Profile.DoesNotExist:
                context['viewer_profile'] = None
        context['is_owner'] = is_owner
        context['is_liked'] = is_liked
        return context

class ShowFollowersDetailView(DetailView):
    '''Define a view to show followers for a profile'''

    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        """Add viewer_profile for navbar links when authenticated."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['viewer_profile'] = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                context['viewer_profile'] = None
        else:
            context['viewer_profile'] = None
        return context

class ShowFollowingDetailView(DetailView):
    '''Define a view to show profiles that a profile is following'''

    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        """Add viewer_profile for navbar links when authenticated."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['viewer_profile'] = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                context['viewer_profile'] = None
        else:
            context['viewer_profile'] = None
        return context

class PostFeedListView(CustomLoginRequiredMixin, ListView):
    '''Define a view to show the post feed for a profile'''

    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        '''Return the QuerySet of posts for the feed'''
        # Get profile from logged in user
        profile = self.get_profile()
        return profile.get_post_feed()
    
    def get_context_data(self, **kwargs):
        '''Add the profile to the context data'''
        context = super().get_context_data(**kwargs)
        # Get profile from logged in user
        profile = self.get_profile()
        context['profile'] = profile
        # Add viewer_profile for navbar
        context['viewer_profile'] = profile
        return context

class SearchView(CustomLoginRequiredMixin, ListView):
    '''Define a view to search for profiles and posts'''

    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''Handle the request and return the appropriate template'''
        # Check if query is present in GET parameters
        if 'query' not in self.request.GET:
            # Get profile from logged in user
            profile = self.get_profile()
            return render(request, 'mini_insta/search.html', {'profile': profile, 'viewer_profile': profile})
        else:
            # Continue with ListView processing
            return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''Return the QuerySet of posts that match the search query'''
        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__icontains=query)
    
    def get_context_data(self, **kwargs):
        '''Add additional context data for the template'''
        context = super().get_context_data(**kwargs)
        
        # Get the profile from logged in user
        profile = self.get_profile()
        context['profile'] = profile
        # Add viewer_profile for navbar
        context['viewer_profile'] = profile
        
        # Get the query
        query = self.request.GET.get('query', '')
        context['query'] = query
        
        # Get matching profiles
        matching_profiles = Profile.objects.filter(username__icontains=query) | Profile.objects.filter(display_name__icontains=query) | Profile.objects.filter(bio_text__icontains=query)
        context['profiles'] = matching_profiles
        
        return context

class CreatePostView(CustomLoginRequiredMixin, CreateView):
    '''Define a view to create a new post'''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # Get profile from logged in user
        profile = self.get_profile()

        # add this profile into the context dictionary:
        context['profile'] = profile
        # Add viewer_profile for navbar
        context['viewer_profile'] = profile
        return context
        
        
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Post
        object before saving it to the database.
        '''
        
        # Get profile from logged in user
        profile = self.get_profile()
        # attach this profile to the post
        form.instance.profile = profile # set the FK
        
        # delegate the work to the superclass method form_valid:
        response = super().form_valid(form)

        files = self.request.FILES.getlist('files')
        for f in files:
            Photo.objects.create(
                post=self.object,
                image_file=f
            )
        
        return response

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Post.'''
 
        # Get profile from logged in user
        profile = self.get_profile()
        # call reverse to generate the URL to the profile
        return reverse('show_profile', kwargs={'pk':profile.pk})


class UpdateProfileView(CustomLoginRequiredMixin, UpdateView):
    '''Update an existing Profile.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'
    
    def get_object(self):
        '''Return the Profile object for the logged in user.'''
        return self.get_profile()

    def get_context_data(self, **kwargs):
        """Provide profile and viewer_profile to templates/nav."""
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context['profile'] = profile
        context['viewer_profile'] = profile
        return context


class UpdatePostView(CustomLoginRequiredMixin, UpdateView):
    '''Update an existing Post (caption).'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_queryset(self):
        """Restrict updates to posts owned by the logged-in user."""
        return Post.objects.filter(profile__user=self.request.user)

    def get_success_url(self):
        '''Provide a URL to redirect to after updating a Post.'''

        # create and return a URL:
        pk = self.kwargs['pk']
        # call reverse to generate the URL to the profile
        return reverse('show_post', kwargs={'pk':pk})

    def get_context_data(self, **kwargs):
        """Add viewer_profile for navbar links when authenticated."""
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                context['viewer_profile'] = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                context['viewer_profile'] = None
        else:
            context['viewer_profile'] = None
        return context


class DeletePostView(CustomLoginRequiredMixin, DeleteView):
    '''Delete a Post.'''

    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    context_object_name = 'post'

    def get_queryset(self):
        """Restrict deletes to posts owned by the logged-in user."""
        return Post.objects.filter(profile__user=self.request.user)

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data(**kwargs)

        # find/add the profile to the context data
        pk = self.kwargs['pk']
        post = Post.objects.get(pk=pk)
        profile = post.profile

        # add this profile into the context dictionary:
        context['post'] = post
        context['profile'] = profile
        # Add viewer_profile for navbar
        if self.request.user.is_authenticated:
            try:
                context['viewer_profile'] = Profile.objects.get(user=self.request.user)
            except Profile.DoesNotExist:
                context['viewer_profile'] = None
        else:
            context['viewer_profile'] = None
        return context

    def get_success_url(self):
        '''Provide a URL to redirect to after deleting a Post.'''

        # find the post associated with this view
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)

        # find the profile associated with this post
        profile = post.profile

        return reverse('show_profile', kwargs={'pk': profile.pk})


class LogoutConfirmationView(TemplateView):
    '''Display a logout confirmation page.'''
    
    template_name = 'mini_insta/logged_out.html'


class CreateProfileView(CreateView):
    '''Create a new Profile and associated User account.'''
    
    form_class = CreateProfileForm
    template_name = 'mini_insta/create_profile_form.html'
    
    def get_context_data(self, **kwargs):
        '''Add UserCreationForm to context data.'''
        
        # Call the superclass method
        context = super().get_context_data(**kwargs)
        
        # Create an instance of UserCreationForm and add to context
        context['user_form'] = UserCreationForm()
        
        return context
    
    def form_valid(self, form):
        '''Handle form submission: create User and Profile.'''
        
        # Reconstruct the UserCreationForm from POST data
        user_form = UserCreationForm(self.request.POST)
        
        # Save the User object
        user = user_form.save()
        
        # Log the user in
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        # Attach the User to the Profile instance
        form.instance.user = user
        
        # Delegate to superclass to save the Profile
        return super().form_valid(form)


class FollowProfileView(CustomLoginRequiredMixin, TemplateView):
    '''Create a Follow relationship between logged-in user and another profile.'''
    
    def dispatch(self, request, *args, **kwargs):
        '''Handle the follow operation.'''
        
        # Get the profile to follow (from URL parameter)
        profile_to_follow = Profile.objects.get(pk=self.kwargs['pk'])
        
        # Get the logged-in user's profile
        logged_in_profile = self.get_profile()

        # Prevent self-follow and duplicates
        if profile_to_follow != logged_in_profile and not Follow.objects.filter(
            profile=profile_to_follow,
            follower_profile=logged_in_profile
        ).exists():
            # Create Follow object (logged-in user follows the other profile)
            Follow.objects.create(
                profile=profile_to_follow,
                follower_profile=logged_in_profile
            )
        
        # Redirect to the profile page
        return redirect('show_profile', pk=profile_to_follow.pk)


class UnfollowProfileView(CustomLoginRequiredMixin, TemplateView):
    '''Delete a Follow relationship between logged-in user and another profile.'''
    
    def dispatch(self, request, *args, **kwargs):
        '''Handle the unfollow operation.'''
        
        # Get the profile to unfollow (from URL parameter)
        profile_to_unfollow = Profile.objects.get(pk=self.kwargs['pk'])
        
        # Get the logged-in user's profile
        logged_in_profile = self.get_profile()
        
        # Find and delete the Follow object
        Follow.objects.filter(
            profile=profile_to_unfollow,
            follower_profile=logged_in_profile
        ).delete()
        
        # Redirect to the profile page
        return redirect('show_profile', pk=profile_to_unfollow.pk)


class LikePostView(CustomLoginRequiredMixin, TemplateView):
    '''Create a Like relationship between logged-in user and a post.'''
    
    def dispatch(self, request, *args, **kwargs):
        '''Handle the like operation.'''
        
        # Get the post to like (from URL parameter)
        post_to_like = Post.objects.get(pk=self.kwargs['pk'])
        
        # Get the logged-in user's profile
        logged_in_profile = self.get_profile()

        # Prevent self-like and duplicates
        if post_to_like.profile != logged_in_profile and not Like.objects.filter(
            post=post_to_like,
            profile=logged_in_profile
        ).exists():
            # Create Like object
            Like.objects.create(
                post=post_to_like,
                profile=logged_in_profile
            )
        
        # Redirect to the post page
        return redirect('show_post', pk=post_to_like.pk)


class UnlikePostView(CustomLoginRequiredMixin, TemplateView):
    '''Delete a Like relationship between logged-in user and a post.'''
    
    def dispatch(self, request, *args, **kwargs):
        '''Handle the unlike operation.'''
        
        # Get the post to unlike (from URL parameter)
        post_to_unlike = Post.objects.get(pk=self.kwargs['pk'])
        
        # Get the logged-in user's profile
        logged_in_profile = self.get_profile()
        
        # Find and delete the Like object
        Like.objects.filter(
            post=post_to_unlike,
            profile=logged_in_profile
        ).delete()
        
        # Redirect to the post page
        return redirect('show_post', pk=post_to_unlike.pk)
