from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect

from authors.forms import AuthorForm

from authors.models import Author
from posts.models import Post
from friends.models import Friend
from images.models import Image

from django.contrib.auth.models import User

# Create your views here.
@login_required
def get_all_authors(request):
    context = RequestContext( request )
    # We grab all the authors that aren't the currently logged in user.
    a = Author.objects.exclude(user=request.user)

    context_dict  = {'authors': a}
    return render_to_response('social/authors.html', context_dict, context )

#get specific author information
@login_required
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

        posts = Post.objects.all()
    
        # IN HERE WE ONLY WANT TO SEE THE FRIEND POSTS AND MY POSTS
        # WE ONLY SHOW ALL PUBLIC POSTS IN THE INDEX PAGE
        #First get all the posts that are public
        current_user_friends = request.user.author.friends.all()
        public_posts = posts.filter(visibility="PUBLIC").filter(author__in = current_user_friends )

        #Visible to friends
        friend_posts = posts.filter(visibility="FRIENDS").filter(author__in = current_user_friends )

        private_posts = posts.filter(visibility="PRIVATE").filter(author = request.user.author )

        posts = public_posts | friend_posts | private_posts 

        images = Image.objects.filter(author=a)
        friend_guids.append(Author.objects.get(user=request.user).guid)

        context_dict = {'author':a, 'user_posts': posts, 'our_friends': friend_guids, 'user_images': images}

        return render_to_response('social/profile.html', context_dict, context )
    elif request.method == "POST":
        if u.username == request.user.username:
            form = AuthorForm(request.POST, instance=a)
            form.save()
        return HttpResponseRedirect("/authors/%s/" % author_guid)


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
    
    #First get all the posts that are public
    public_posts = posts.filter(visibility="PUBLIC")

    #Visible to friends
    current_user_friends = request.user.author.friends.all()
    friend_posts = posts.filter(visibility="FRIENDS").filter(author__in = current_user_friends )

    private_posts = posts.filter(visibility="PRIVATE").filter(author = request.user.author )

    posts = public_posts | friend_posts | private_posts 

    context_dict['user_posts'] = posts

    return render_to_response('social/posts.html', context_dict, context )


