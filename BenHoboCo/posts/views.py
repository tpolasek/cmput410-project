from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from django.http import HttpResponseRedirect

from authors.models import Author
from posts.models import Post
from .models import Comment

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
