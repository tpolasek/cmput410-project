from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from social.forms import UserForm, AuthorForm

from social.models import Post, Author, Image, Friend
from django.contrib.auth.models import User

# Create your views here.

def index( request ):
    context = RequestContext( request )
    return render_to_response('social/index.html',{},context)

def get_all_authors(request):
    context = RequestContext( request )

    #Get all authors
    a = Author.objects.all()
    context_dict  = {'authors': a}
    return render_to_response('social/authors.html', context_dict, context )

#get specific author information
def get_author(request, author_name = None):
    context = RequestContext( request )

     #get User object then find the Author object from it
    u = User.objects.get(username__iexact=author_name)
    a = Author.objects.get(user=u)

    # FOR BENSON:
    #  We gotta get the posts for this author.
    #  Posts should be gotten based on relationship to the user.
    #  If current user is the author, then we can show all posts.
    #  If current user is friend, show friend posts, etc.
    #  If no user is logged in, show all public posts.

    #Display the posts on the profile page
    return render_to_response('social/profile.html', {'author': a, 'user': u}, context )

def get_author_images(request, author_name, image_id = None ):
    context = RequestContext( request )
    
    #get User object then find the Author object from it
    u = User.objects.get(username__icontains=author_name)
    a = Author.objects.get(user=u)
    context_dict = {}
    
    if image_id is not None:
        try:
            context_dict['image'] = Image.objects.get(id=image_id)
        except ObjectDoesNotExist:
            pass #do nothing for now
        
        return render_to_response('social/images.html', context_dict, context )

    context_dict['user_images'] = Image.objects.filter(author=a)
    
    #no content
    return render_to_response('social/images.html', context_dict, context )

def get_author_posts(request, author_name, post_id = None ):
    context = RequestContext( request )

    #get User object then find the Author object from it
    u = User.objects.get(username__iexact=author_name)
    a = Author.objects.get(user=u)
    context_dict = {}
    context_dict['author'] = a

    if post_id is not None:
        try:
            post = Post.objects.get(id=post_id)
            context_dict['post']= post
        except ObjectDoesNotExist:
            pass #do nothing for now

        return render_to_response('social/post.html', context_dict, context )

    posts = Post.objects.filter(author=a)
    context_dict['user_posts'] = posts

    #no content
    return render_to_response('social/posts.html', context_dict, context )

def get_author_friends(request, author_name, friend_name = None):
    context = RequestContext( request )

    u = User.objects.get(username__iexact=author_name)
    a = Author.objects.get(user=u)
    context_dict = {}

    if friend_name is not None:
        try:
            friend = Friend.objects.get(name=friend_name)
            context_dict['friend'] = friend
        except ObjectDoesNotExist:
            pass # Do nothing for now

        return render_to_response('social/friends.html', context_dict, context )

    friend = Friend.objects.filter(author=a)
    context_dict['user_friends'] = friend
    context_dict['author'] = a

    #no content
    return render_to_response('social/friends.html', context_dict, context )

def add_remote_friend(request, author_name):
    context = RequestContext(request)
    u = User.objects.get(username__iexact=author_name)
    a = Author.objects.get(user = u)
    return render_to_response('social/addRemoteFriend.html', {'author': a}, context)

def create_post(request, author_name):
    context = RequestContext(request)
    u = User.objects.get(username__iexact=author_name)
    a = Author.objects.get(user = u)
    return render_to_response('social/createPost.html', {'author': a}, context)

def user_register(request):

    if request.user.is_authenticated():
        return redirect("/")

    context = RequestContext(request)

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        author_form = AuthorForm()

        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            author = author_form.save(commit=False)
            author.user = user

            author.save()

            registered = True

        else:
            print user_form.errors

    else:
        user_form = UserForm()

    context_dict = {'user_form': user_form, 'registered': registered }

    return render_to_response('social/register.html', context_dict, context)

def user_login(request):
    if request.user.is_authenticated():
        return redirect("/")

    context = RequestContext(request)

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                return render_to_response('social/login.html', {'disabled_account':True }, context)
        else:
            return render_to_response('social/login.html', {'bad_details': True }, context)
    else:
        return render_to_response('social/login.html',{},context)

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect("/")