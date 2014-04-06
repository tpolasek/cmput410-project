from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from images.forms import ImageUploadForm
from authors.forms import UserForm, AuthorForm
from .models import SiteConfiguration


from authors.models import Author
from posts.models import Post

# Create your views here.
def index( request ):
    context = RequestContext( request )
    print "META %s" % request.META['REMOTE_ADDR']
    try:
        if request.user.is_authenticated():
            a = Author.objects.get(user = request.user)
            p = Post.objects.filter(visibility = "PUBLIC")
            return render_to_response('social/personalhomePage.html',{'author': a, 'posts': p}, context)
    except:
        pass
    return render_to_response('social/index.html',{},context)

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect("/")

def user_login(request):
    if request.user.is_authenticated():
        return redirect("/")

    print "HTTP_HOST: %s" % request.META['HTTP_HOST']

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

            author.host = request.META['HTTP_HOST']
            author.url = "http://%s/authors/%s" % ( request.META['HTTP_HOST'], author.guid )
            print author.url

            author.save()

            registered = True

        else:
            print user_form.errors

    else:
        user_form = UserForm()

    context_dict = {'user_form': user_form, 'registered': registered }

    return render_to_response('social/register.html', context_dict, context)

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