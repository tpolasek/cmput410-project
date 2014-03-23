from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from social.forms import UserForm, AuthorForm, ImageUploadForm
from django.db.models import Q
from django.conf import settings
from datetime import datetime

from social.models import *
from django.contrib.auth.models import User

import json

# Create your views here.

def index( request ):
    context = RequestContext( request )
    try: 
        if request.user.is_authenticated():
            a = Author.objects.get(user = request.user)
            p = Post.objects.filter(visibility = "PUBLIC")
            return render_to_response('social/personalhomePage.html',{'author': a, 'posts': p}, context)
    except:
        pass
    return render_to_response('social/index.html',{},context)

@login_required
def get_all_authors(request):
    context = RequestContext( request )
    # We grab all the authors that aren't the currently logged in user.
    a = Author.objects.exclude(user=request.user)

    context_dict  = {'authors': a}
    return render_to_response('social/authors.html', context_dict, context )

#get specific author information
def get_author(request, author_guid = None):
    context = RequestContext( request )

    try:
        u = User.objects.get(username=author_guid)
        a = Author.objects.get(user=u)
    except User.DoesNotExist:
        a = Author.objects.get(guid=author_guid)
        u = a.user
    
    if request.method == "GET":

        #in my profile I want to see posts that are private to me
        #posts that are from my friends that are shared as "friends of friends"
        #posts that are shared to me by local_friends

        #posts that are shared to me by global_friends
        #posts that are shared to me by friends of friends

        #friends of author
        friends = Friend.objects.filter( author = Author.objects.get(user=request.user) )

        #Get the posts where the author is the user signed in
        # and also where the author is in the list of friends
        friend_names = [ friend.friend_name for friend in friends ]
        friend_guids = [ friend.friend_guid for friend in friends ]

        users = User.objects.filter(username__in=friend_names)

        authors = Author.objects.filter(user__in=users)

        #If the post is private, we won't show it. 
        #If the post is friends_of_friends we will show it
        #If the post is local then the user will be registered. Since we are only polling
        #users that are registered and finding the authors that way, we will only
        #have local friends atm.
        p = Post.objects.filter( ~Q(visibility = "PRIVATE" )).filter(( Q(author = a) | Q(author__in = authors) ) )

    	images = Image.objects.filter(author=a)
	friend_guids.append(Author.objects.get(user=request.user).guid)
        
	context_dict = {'author':a, 'user_posts': p, 'our_friends': friend_guids, 'user_images': images}

        return render_to_response('social/profile.html', context_dict, context )
    elif request.method == "POST":
        if u.username == request.user.username:
            form = AuthorForm(request.POST, instance=a)
            form.save()
        return HttpResponseRedirect("/authors/%s/" % author_guid) 
    

def get_author_images(request, author_guid = None, image_id = None ):
    context = RequestContext( request )
    
    
    #get User object then find the Author object from it
    if author_guid is not None:
        a = Author.objects.get(guid=author_guid)
    else:
        a = Author.objects.get(user=request.user)
        
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

def get_author_posts(request, author_guid ):
    context = RequestContext( request )

    #get User object then find the Author object from it
    a = Author.objects.get(guid=author_guid)
    context_dict = {}
    context_dict['author'] = a

    posts = Post.objects.filter(author=a)
    context_dict['user_posts'] = posts

    return render_to_response('social/posts.html', context_dict, context )

def search_friend(request):
    context = RequestContext(request)
    context_dict = {}

    context_dict['hosts'] = settings.ALLOWED_HOSTS

    # TODO Remco - Decide whether it is the local or a remote server
    if request.method == "POST":
        name = request.POST["friend_name"]
        host = request.POST["host_name"]

        print "HOST: ", host
        # Some error checking
        if host == "Select Host":
            context_dict["host_unselected"] = True
            return render_to_response('social/friendSearch.html', context_dict, context)

        if host == "127.0.0.1:8000":
            authors_json = json.dumps( [ author.json() for author in Author.objects.all() ] )

        else:
            authors_json = "[]"

        # At this point we should have an authors JSON object
        all_authors = json.loads( authors_json )

        selected_authors = []
        for author in all_authors:
            if name in author['displayname']:
                selected_authors.append( { 'name': author['displayname'], 'host': host, 'guid': author['id'] } )

        context_dict['found_authors'] = selected_authors


    return render_to_response('social/friendSearch.html', context_dict, context)

def delete_friend(request, author_guid, friend_guid):
    context = RequestContext( request )

    if request.method == "POST":
        a = Author.objects.get(guid=author_guid)
        u = a.user

        # Is it us trying to delete our own friend?
        if u.username == request.user.username:
            friend = Friend.objects.get(friend_guid=friend_guid, author=a )
            friend.delete()

    return HttpResponseRedirect("/authors/%s/friends/" % a.guid) 

def get_author_friends(request, author_guid, friend_guid = None):
    context = RequestContext( request )

    a = Author.objects.get(guid=author_guid)
    u = a.user
    context_dict = {}

    if friend_guid is not None:
        try:
            friend = Friend.objects.get(friend_guid=friend_guid, author=a)
            context_dict['friend'] = friend
        except ObjectDoesNotExist:
            pass # Do nothing for now

        return render_to_response('social/friends.html', context_dict, context )

    friend = Friend.objects.filter(author=a)
    context_dict['user_friends'] = friend
    context_dict['author'] = a

    #no content
    return render_to_response('social/friends.html', context_dict, context )

# Accepts a friend request.
def add_friend(request, author_guid):
    context = RequestContext(request)

    try:
        u = User.objects.get(username=author_guid)
        a = Author.objects.get(user=u)
    except User.DoesNotExist:
        a = Author.objects.get(guid=author_guid)
        u = a.user

    context_dict = {'author': a}

    if request.method == "POST":
        new_friend_name = request.POST['friend_name']
        new_friend_guid = request.POST['friend_guid']
        new_friend_location = request.POST['friend_location']

        # If it is blank, we will be assuming it came from the best host of all!
        if not new_friend_location:
            new_friend_location = settings.ALLOWED_HOSTS[0]

        if not Friend.objects.filter(author=a, friend_guid=new_friend_guid):
            new_friend = Friend(friend_name=new_friend_name, host=new_friend_location, friend_guid=new_friend_guid, author=a)
            new_friend.save()
        else:
            print "Already a friend!"

        # TODO add friend request?

    return HttpResponseRedirect('/authors/%s/friends/' % author_guid)

@login_required
def create_post(request, author_name = None ):
    context = RequestContext(request)
    u = request.user
    a = Author.objects.get(user = u)

    context_dict = {'author': a, 'success': False }

    if request.method == "POST":
        access = request.POST['access']
        c = request.POST['content']
        post_title = request.POST['title']
        t = request.POST['content_type']
        if t == "markup":
            import markdown2
            c = markdown2.markdown(c)
        elif t == "text":
            c = c
        else:
            pass

        p = Post(author=a, visibility=access, content=c, title=post_title)
        p.save()

        return HttpResponseRedirect("/posts/")

    return render_to_response('social/createPost.html', context_dict, context)



@login_required
def create_image(request, author_guid = None ):
    context = RequestContext(request)
    u = request.user
    a = Author.objects.get(user = u)

    context_dict = {'author': a, 'success': False }
    return render_to_response('social/createImage.html', context_dict, context)


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
            
            site_config = SiteConfiguration.objects.get()
            if site_config.manual_user_signup:
                 user.is_active = False

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

# POST: Updates the User and its associated Author object
# GET: Presents the Account Management page.
@login_required
def manage_account(request):
    context = RequestContext(request)

    u = request.user
    a = Author.objects.get(user = u)

    # Update the user account information.
    #if request.method == "POST":

    return render_to_response('social/manageProfile.html', {'author': a, 'user': u}, context)

# Changes a user's password.
# Only accepts posts, and returns back to the management page.
@login_required
def user_change_password(request):
    context = RequestContext(request)

    u = request.user
    a = Author.objects.get(user = u)

    # Update the user account information.
    if request.method == "POST":
        newPassword = request.POST['newPassword']
        passwordConfirm = request.POST['confirmPassword']

        if newPassword != passwordConfirm:
            return render_to_response('social/manageProfile.html', {'author': a, 'user': u, 'password_not_same': True}, context)
        else:
            u.set_password(newPassword)
            u.save()
            return render_to_response('social/manageProfile.html', {'author': a, 'user': u, 'password_change_success': True}, context)
    return render_to_response('social/manageProfile.html', {'author': a, 'user': u}, context)

# Updates the Author information.
# Only accepts posts, and returns back to the management page.
@login_required
def user_update_author(request):
    context = RequestContext(request)

    u = request.user
    a = Author.objects.get(user = u)

    # Update the user account information.
    if request.method == "POST":
        newGithub = request.POST['gitHub']
        a.github = newGithub
        a.save()
    	return render_to_response('social/manageProfile.html', {'author': a, 'user': u, 'github_success': True}, context)

    return render_to_response('social/manageProfile.html', {'author': a, 'user': u }, context)


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect("/")

@login_required
def posts(request, post_id = None):

    context = RequestContext( request )
    context_dict = {}
    user = request.user
    context_dict['user'] = user


    if post_id is not None:
        # Single post.
        p = Post.objects.get(id = post_id )
        context_dict['user_post'] = p
        return render_to_response('social/post.html', context_dict, context)
    else:
        a = Author.objects.get(user = user)
        p = Post.objects.filter(author=a)
        if not p:
            context_dict['user_posts'] = None
        else:
            context_dict['user_posts'] = p

    return render_to_response('social/posts.html', context_dict, context )

@login_required
def friends(request, friend_id = None):
    context = RequestContext( request )
    context_dict = {}
    user = request.user
    context_dict['user'] = user

    if friend_id is not None:
        f = Friend.objects.get(id = friend_id)
        context_dict['user_friend'] = f
        return render_to_response('social/friend.html', context_dict, context)
    else:
        a = Author.objects.get(user = user)
        f = Friend.objects.filter(author = a)
        if not f:
            context_dict['user_friends'] = None
        else:
            context_dict['user_friends'] = f

    return render_to_response('social/friends.html', context_dict, context)


@login_required
def delete_post(request, post_id ):
    #Deleting a post
    if request.method == "POST":

        # in the template, I have ensured that the user can only
        # see the delete button if they are signed in as that user
        # and viewing a post that they posted
        try:
            post = Post.objects.get(id=post_id)
            post.delete()
        except ObjectDoesNotExist:
            pass

        u = request.user
        a = Author.objects.get(user = u)

        posts = Post.objects.filter(author=a)


    return HttpResponseRedirect("/posts/")

@login_required
def upload_profile_image(request):
    context = RequestContext(request)
    user=request.user
    author = Author.objects.get(user=user)
    if request.method == "POST":     
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            im = form.cleaned_data['image']
            author.image = im
            author.save()
    #TODO add notificiation
    return render_to_response('social/manageProfile.html', {'author': author, 'user': user, 'image_change_success' : True}, context)

@login_required
def upload_image(request):
    if request.method == "POST":
        context = RequestContext(request)
    	auth = Author.objects.get(user=request.user)
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            url = "/media/Images/" + str(form.cleaned_data['image']) 
            image = Image(image=form.cleaned_data['image'],url=url, visibility='PUBLIC', author=auth)
            image.save()
    return HttpResponseRedirect("/images/")

@login_required
def add_comment(request, post_id):
    context = RequestContext(request)
    if request.method == "POST":
        u = request.user
        commented_post = Post.objects.get(id = post_id)
        author = Author.objects.get(user = u)
        content = request.POST["content"]

        c = Comment(author = author, comment = content, pubDate = datetime.now(), post = commented_post)
        c.save()

    return HttpResponseRedirect("/posts/" + post_id)
