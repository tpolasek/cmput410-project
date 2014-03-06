from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from social.models import Post, Author

# Create your views here.
def authors(request, user_name = None):
    RequestContext( request )

    #Get specific posts for a certain author
    if( not user_name is None ):

        #get User object then find the Author object from it
        u = User.objects.get(username__icontains=user_name)
        a = Author.objects.get(user=u)

        posts = Post.objects.filter(author=a)
        context_dict = {'user_posts': posts }

        return render_to_response('social/authors.html', context_dict, context )

    
    #Get all authors
    a = Author.objects.all()
    context_dict  = {'authors': a}
    return render_to_response('social/authors.html', context_dict, context )

