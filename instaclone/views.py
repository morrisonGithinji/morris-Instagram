from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .email import send_welcome_email
from .forms import PostForm, CommentForm, ProfileForm
from .models import *
from django.urls import  reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db import transaction
# Create your views here.
def index(request):
  post = Post.objects.all()
  
  
  return render(request,'index.html',{'post':post})
@login_required
def profile(request,username):
  
  user = get_object_or_404(User,username=username)
  post = Post.objects.filter(user=user)
  profile = Profile.objects.get(user=user)
  
  follow_status = Follow.objects.filter(following=user, follower =request.user).exists()
  return render(request,'profile.html',{'user':user, 'post':post, 'profile':profile,'follow_status':follow_status})

@login_required
def new_post(request):
  user =  Profile.objects.get(user=request.user)
  if request.method == 'POST':
    form = PostForm(request.POST,request.FILES)
    if form.is_valid():
      post= form.save(commit=False)
      post.profile = user
      post.user = request.user
      post.save()
    return redirect('index')  
  else:
    form = PostForm()
  return render(request,'new_post.html', {'form':form})  

@login_required
def post_details(request, post_id):
  post = Post.objects.get(id=post_id)
  user = request.user
  
  comments = Comment.objects.filter(post=post).order_by('date')
  
  if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
      comment = form.save(commit=False)
      comment.post= post
      comment.user = user 
      comment.save()
      return HttpResponseRedirect(reverse('post_details', args=[post_id]))       
  else:
    form = CommentForm()
 
  
  return render(request,'post_detail.html',{'post':post, 'form':CommentForm, 'comments':comments})
  
  
@login_required
def likes(request,post_id):
  user = request.user
  post = get_object_or_404(Post,id=post_id)
  post_likes = post.likes
  
  liked = Likes.objects.filter(user=user,post=post).count()
  if not liked:
    like = Likes.objects.create(user=user,post=post)
    post_likes = post_likes +1
    
  else:
    Likes.objects.filter(user=user,post=post).delete()  
    post_likes = post_likes -1
    
  post.likes = post_likes
  post.save()
  
  return redirect(reverse('index'))
  
@login_required
def follow(request,username,option):
  user = request.user
  following = get_object_or_404(User,username=username)
  
  try:
    f, created= Follow.objects.get_or_create(follower=user,following=following)
    
    if int(option) == 0:
      f.delete() 
      Stream.objects.filter(following=following,user=user).all().delete()
      
    else:
      posts = Post.objects.all().filter(user=following)[:10]
      
      with transaction.atomic():
        for post in posts:
          stream = Stream(post=post,user=user,following=following,date=post.date)
          stream.save()
          
    return redirect(reverse('profile', args=[username])) 
  except User.DoesNotExist:
    return redirect(reverse('profile', args=[username]))       
 
@login_required
def update_profile(request,username):
  user = get_object_or_404(User,username=username)
  new_user = request.user
  if request.method == 'POST':
    
    form = ProfileForm(request.POST, request.FILES)
    if form.is_valid():
      profile = form.save(commit=False)
      profile.user = new_user
      profile.save()
      
      return redirect(reverse('index' ) )  
    else:
      form = ProfileForm()  
    
  return render(request, 'new_profile.html',{'user':user, 'form':ProfileForm})  

@login_required
def search_results(request):
  if 'user' in request.GET and request.GET['user']:
    search_name = request.GET.get('user')
    searched_users = Post.search_by_name(search_name)
    message = f"{search_name}"
    
    return render(request,'search.html',{"message":message,"users":searched_users})
  else:
    message ="Please enter a username"
    return render(request,'search.html',{'message':message})
    