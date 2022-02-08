from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import  post_save
from django.urls import reverse
from cloudinary.models import CloudinaryField
from tinymce.models import HTMLField
import uuid
class Profile(models.Model):
  bio = models.TextField(max_length = 100)
  profile_photo = CloudinaryField('images')
  user = models.OneToOneField(User, on_delete=models.CASCADE )
  
  def __str__(self):
    return self.user.username
  
  def save_profile(self):
    self.save()

class  Post(models.Model):
  id= models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  image = CloudinaryField('images')
  image_name = models.CharField(max_length=30,blank=True)
  image_caption = models.CharField(max_length=250,default ='')
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  likes = models.IntegerField(default=0)
  profile = models.ForeignKey(Profile,on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)
  def save_image(self):
    self.save()
  
  def delete_image(self):
    self.delete()  

  def __str__(self):
    return self.image_name
  
  @classmethod
  def search_by_name(cls,search_name):
    user = cls.objects.filter(username__icontains=search_name)
    return user
  
  
  def get_absolute_url(self):
    return reverse('post_details', args=[str(self.id)])
  
class Likes(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_like')
  post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_likes")
  
  def __str__(self):
    return self.user.username
  
class  Comment(models.Model):
     post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_comment")
     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_commeent')
     comment = models.TextField()
     date = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
  following = models.ForeignKey(User,on_delete=models.CASCADE, related_name='following') 
  follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='follower')
  
class  Stream(models.Model):
  # follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='stream_follower')
  following = models.ForeignKey(User,on_delete=models.CASCADE, related_name='stream_following') 
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  post = models.ForeignKey(Post,on_delete=models.CASCADE)
  date = models.DateTimeField()
  
  def add_post(sender,instance,*args, **kwargs):
    post= instance
    user= post.user
    followers = Follow.objects.all().filter(following=user)
    for follower in followers:
      stream = Stream(post=post,user=follower.follower, date = post.date, following = user)
      stream.save()

post_save.connect(Stream.add_post,sender=Post)      
