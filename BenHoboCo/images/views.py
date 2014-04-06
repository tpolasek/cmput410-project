from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponseRedirect

from images.forms import ImageUploadForm

from authors.models import Author
from images.models import Image

@login_required
def create_image(request, author_guid = None ):
    context = RequestContext(request)
    u = request.user
    a = Author.objects.get(user = u)

    context_dict = {'author': a, 'success': False }
    return render_to_response('social/createImage.html', context_dict, context)

@login_required
def upload_image(request):
    if request.method == "POST":
        context = RequestContext(request)
        auth = Author.objects.get(user=request.user)
        form = ImageUploadForm(request.POST, request.FILES)
        access = request.POST['access']
        if form.is_valid():
            url = "/media/Images/" + str(form.cleaned_data['image']) 
            image = Image(image=form.cleaned_data['image'],url=url, visibility=access, author=auth)
            image.save()
    return HttpResponseRedirect("/images/")