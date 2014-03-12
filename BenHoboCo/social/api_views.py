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
from django.core import serializers
from django.forms.models import model_to_dict

import json

# Create your views here.

def get_authors(request):
    a = Author.objects.all()
    #return HttpResponse( serializers.serialize( 'json', a ) )

    if request.method == "POST":
        #Implement the creation of author with json data
        pass

    data = [ author.json() for author in a ]
    return HttpResponse( json.dumps(data), content_type="application/json")