# File: views.py
# Author: Travis Falk(travisf@bu.edu), 9/25/2025
# Description: View definitions for mini_insta app

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse

# Create your views here.
class ProfileListView(ListView):
    '''Define a view to list all profiles'''

    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

class ProfileDetailView(DetailView):
    '''Define a view to show profile details'''

    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

class PostDetailView(DetailView):
    '''Define a view to show post details'''

    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class ShowFollowersDetailView(DetailView):
    '''Define a view to show followers for a profile'''

    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    '''Define a view to show profiles that a profile is following'''

    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class PostFeedListView(ListView):
    '''Define a view to show the post feed for a profile'''

    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        '''Return the QuerySet of posts for the feed'''
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        return profile.get_post_feed()
    
    def get_context_data(self, **kwargs):
        '''Add the profile to the context data'''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

class SearchView(ListView):
    '''Define a view to search for profiles and posts'''

    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''Handle the request and return the appropriate template'''
        # Check if query is present in GET parameters
        if 'query' not in self.request.GET:
            pk = self.kwargs['pk']
            profile = Profile.objects.get(pk=pk)
            return render(request, 'mini_insta/search.html', {'profile': profile})
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
        
        # Get the profile from URL
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        
        # Get the query
        query = self.request.GET.get('query', '')
        context['query'] = query
        
        # Get matching profiles
        matching_profiles = Profile.objects.filter(username__icontains=query) | Profile.objects.filter(display_name__icontains=query) | Profile.objects.filter(bio_text__icontains=query)
        context['profiles'] = matching_profiles
        
        return context

class CreatePostView(CreateView):
    '''Define a view to create a new post'''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template.'''

        # calling the superclass method
        context = super().get_context_data()

        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this profile into the context dictionary:
        context['profile'] = profile
        return context
        
        
    def form_valid(self, form):
        '''This method handles the form submission and saves the 
        new object to the Django database.
        We need to add the foreign key (of the Profile) to the Post
        object before saving it to the database.
        '''
        
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
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
 
        # create and return a URL:
        pk = self.kwargs['pk']
        # call reverse to generate the URL to the profile
        return reverse('show_profile', kwargs={'pk':pk})


class UpdateProfileView(UpdateView):
    '''Update an existing Profile.'''

    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'


class UpdatePostView(UpdateView):
    '''Update an existing Post (caption).'''

    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

    def get_success_url(self):
        '''Provide a URL to redirect to after updating a Post.'''

        # create and return a URL:
        pk = self.kwargs['pk']
        # call reverse to generate the URL to the profile
        return reverse('show_post', kwargs={'pk':pk})


class DeletePostView(DeleteView):
    '''Delete a Post.'''

    model = Post
    template_name = 'mini_insta/delete_post_form.html'
    context_object_name = 'post'

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
        return context

    def get_success_url(self):
        '''Provide a URL to redirect to after deleting a Post.'''

        # find the post associated with this view
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)

        # find the profile associated with this post
        profile = post.profile

        return reverse('show_profile', kwargs={'pk': profile.pk})
