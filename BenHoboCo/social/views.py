from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from social.forms import UserForm, AuthorForm, ImageUploadForm
from django.db.models import Q

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

    #friends of author
    friends = Friend.objects.filter( author = Author.objects.get(user=request.user) )

    #Get the posts where the author is the user signed in
    # and also where the author is in the list of friends
    friend_names = [ friend.name for friend in friends ]
    users = User.objects.filter(username__in=friend_names)

    authors = Author.objects.filter(user__in=users)

    p = Post.objects.filter(Q(author = a) | Q(author = authors))

    friend_names.append(request.user.username)
    context_dict = {'author':a, 'user_posts': p, 'our_friends': friend_names }

    # DO NOT PASS THE USER IN IT WILL OVERWRITE THE CURRENTLY SIGNED IN USER

    return render_to_response('social/profile.html', context_dict, context )

def get_author_images(request, author_name, image_id = None ):
    context = RequestContext( request )
    
    #get User object then find the Author object from it
    u = User.objects.get(username__iexact=author_name)
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

def get_author_posts(request, author_name ):
    context = RequestContext( request )

    #get User object then find the Author object from it
    u = User.objects.get(username__iexact=author_name)
    a = Author.objects.get(user=u)
    context_dict = {}
    context_dict['author'] = a

    posts = Post.objects.filter(author=a)
    context_dict['user_posts'] = posts

    return render_to_response('social/posts.html', context_dict, context )

def delete_friend(request, author_name, friend_name):
    context = RequestContext( request )

    #get User object then find the Author object from it
    if request.method == "POST":
        u = User.objects.get(username__iexact=author_name)
        a = Author.objects.get(user=u)

        friend_location = request.POST["friend_location"]

        # Is it us trying to delete our own friend?
        if u.username == request.user.username:
            friend = Friend.objects.get(name=friend_name, author=a, location=friend_location)
            friend.delete()

    return HttpResponseRedirect("/authors/%s/friends/" % author_name) 

def get_author_friends(request, author_name, friend_name = None):
    context = RequestContext( request )

    u = User.objects.get(username__iexact=author_name)
    a = Author.objects.get(user=u)
    context_dict = {}

    if request.method == "POST":
        new_friend_name = request.POST['friend_name']
        new_friend_location = request.POST['friend_location']

        if not Friend.objects.filter(author=a, name=new_friend_name, location=new_friend_location):
            new_friend = Friend(name=new_friend_name, location=new_friend_location, author=a)
            new_friend.save()

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
    context_dict = {'author': a}

    if request.method == "POST":
        friend_name = request.POST["friend_name"]
        friend_location = 'http://127.0.0.1:8000' #TODO turn this into something more permanent!
        context_dict['friend_name'] = friend_name
        context_dict['friend_location'] = friend_location

    return render_to_response('social/addRemoteFriend.html', context_dict, context)

@login_required
def create_post(request, author_name = None ):
    context = RequestContext(request)
    u = request.user
    a = Author.objects.get(user = u)

    context_dict = {'author': a, 'success': False }

    if request.method == "POST":
        access = request.POST['access']
        c = request.POST['content']
        
        t = request.POST['content_type']
        if t == "markup":
            import markdown2
            c = markdown2.markdown(c)
        elif t == "text":
            c = "<pre>"+c+"</pre>"
        else:
            pass

        p = Post(author=a, accessibility=access, content=c)
        p.save()

        return HttpResponseRedirect("/authors/" + u.username )

    return render_to_response('social/createPost.html', context_dict, context)

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

@login_required
def posts(request, post_id = None):

    context = RequestContext( request )
    context_dict = {}

    if post_id is not None:
        p = Post.objects.get(id = post_id )
        context_dict['user_posts'] = p
    else:
        p = Post.objects.filter(accessibility="public")
        context_dict['user_posts'] = p

    return render_to_response('social/posts.html', context_dict, context )

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


    return HttpResponseRedirect("/authors/" + u.username )

def upload_image(request, author_name ):
    print "Got here"
    if request.method == "POST":
        
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print "Form is valid"
            author = Author.objects.get(user=request.user)
            author.image = form.cleaned_data['image']
            author.save()

    return HttpResponseRedirect("/authors/"+ request.user.username )

