from django.shortcuts import render, redirect
from blogpost.models import *
from django.contrib.auth import login, authenticate, logout #add this
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm #add this
from .forms import AccountAuthenticationForm
from numerize import numerize 

# Create your views here.
def index(request, *args, **kwargs):
    context = {}
    user = request.user
    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
        posts = Post.objects.filter(profile=profile, isPublished=True)
        profilepost = numerize.numerize(profile.total_posts)
        publishedpost = numerize.numerize(profile.published_post)
        draftpost = numerize.numerize(profile.draft_posts)
        profilecomment = numerize.numerize(profile.total_comments)
        profileimpressions = numerize.numerize(profile.totalpost_impressions)
        context['user'] = user
        context['posts'] = posts
        context['profile'] = profile
        context['profilepost'] = profilepost
        context['publishedpost'] = publishedpost
        context['draftpost'] = draftpost
        context['profilecomment'] = profilecomment
        context['profileimpressions'] = profileimpressions
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
			
            form.save(request)
            return redirect("index")

        else:
            context['login_form'] = form

    
    
    
    return render(request, "index.html", context)


def logout_view(request):
	logout(request)
	return redirect("index")

def editbio(request):
    user = request.user
    context = {
        "user": user
    }

    if user.is_authenticated:
        profile = Profile.objects.get(user=user)
        if request.POST:
            profile.bio = request.POST.get("bio")
            profile.save()
            return redirect("index")
    else:
        return redirect("index")
    
    return render(request, "edit_bio.html", context)

def createpost(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    style = Tag.objects.get(tag="Style")
    relationship = Tag.objects.get(tag="Relationship")
    design = Tag.objects.get(tag="Design")
    food = Tag.objects.get(tag="Food")
    wellbeing = Tag.objects.get(tag="Wellbeing")
    context={
        "style": style,
        "relationship": relationship,
        "design": design,
        "food": food,
        "wellbeing": wellbeing,
    }

    if user.is_authenticated == False:
        return redirect("index")
    
    if request.POST:
        tag = Tag.objects.get(tag=request.POST.get("tag"))
        newpost = Post(title=request.POST.get("title"), breif=request.POST.get("breif"), snippet=request.POST.get("snippet"), headimg=request.FILES.get("image"), tag=tag, profile=profile)
        newpost.save()
        profile.draft_posts = profile.draft_posts + 1
        profile.total_posts = profile.total_posts + 1
        profile.save()
        return redirect("index")
    
    return render(request, "create_post.html", context)

def draftedpost(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(profile=profile, isPublished=False).order_by("-timestamp")
    context ={
        "profile": profile,
        "posts": posts
    }

    if user.is_authenticated == False:
        return redirect("index")
    
    return render(request, "draftedpost.html", context)
    
def editpost(request, pk):
    user = request.user
    profile = Profile.objects.get(user=user)
    post = Post.objects.get(slug=pk)
    context = {
        "profile": profile,
        "post": post,
    }

    sections = Section.objects.filter(blogpost=post)

    if sections:
        context["sections"] = sections

    

    if user.is_authenticated == False:
        return redirect("index") 
    
    return render(request, "editpost.html", context)

def createsection(request, pk):
    user = request.user
    post = Post.objects.get(slug=pk)

    context ={}

    if user.is_authenticated == False:
        return redirect("index")


def publishpost(request, pk):
    user = request.user
    post = Post.objects.get(slug=pk)
    context ={
        "user": user,
        "post": post,
    }

    if user.is_authenticated == False:
        return redirect("index")
    else:
        post.isPublished = True
        post.save()
    
    return render(request, "published.html", context)