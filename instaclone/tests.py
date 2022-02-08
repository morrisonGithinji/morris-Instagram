from django.test import TestCase
from django.contrib.auth.models import User
from .models import *

import datetime as dt
# Create your tests here.

class ProfileTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(username='morris',password= '5431140')
    self.ebay =Profile(bio='Programming is life',user=user)
  def test_instance(self):
    self.assertTrue(isinstance(self.morris,Profile))  
    
  def test_save_method(self):
      self.ebay.save_profile()
      profiles =Profile.objects.all()
      self.assertTrue(len(profiles)>0)
      
      
class LikesTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(username='morris',password= '5431140')
    profile = Profile.objects.create(user=user,bio='code and fun', profile_photo ='morris.jpg')
    post = Post.objects.create(user=user,image='morris.jpg', image_name='me',image_caption= 'i can',profile=profile,likes=2,date='2022-02-05' )
    Likes.objects.create(user=user,post=post)
    
    self.ebay=Likes(user=user)
    
  def test_instance(self):
    self.assertTrue(isinstance(self.ebay,Likes))  
    
class CommentTestCase(TestCase):    
  def setUp(self):
    user = User.objects.create(username='morris',password= '5431140')
    profile = Profile.objects.create(user=user,bio='code and fun', profile_photo ='morris.jpg')
    post = Post.objects.create(user=user,image='morris.jpg', image_name='me',image_caption= 'i can',profile=profile,likes=2,date='2022-02-05' )
    
    self.ebay=Comment(user=user, date='2022-02-05',post=post,comment="yes we can")
  def test_instance(self):
    self.assertTrue(isinstance(self.ebay,Comment))
    
    
class FollowTest(TestCase):
  def setUp(self):
    user = User.objects.create(username='morris',password= '5431140')
    
    self.ebay=Follow(follower=user,following=user)
    
  def test_instance(self):
    self.assertTrue(isinstance(self.ebay,Follow))
  
class PostTest(TestCase):
  def setUp(self):
    user = User.objects.create(username='morris',password= '5431140')
    profile = Profile.objects.create(user=user,bio='code and fun', profile_photo ='morris.jpg')

    self.ebay =Post(user=user,image='morris.jpg',image_name='me',image_caption= 'i can',profile=profile,likes=2,date='2022-02-05')
    
  def test_instance(self):
    self.assertTrue(isinstance(self.ebay,Post))
  
  def test_save(self):
    self.ebay.save_image()
    saved = Post.objects.all()
    self.assertTrue(len(saved)>0)
    
  def test_delete(self):
    self.ebay.delete_image()
    deleted = Post.objects.all()
    self.assertTrue(len(deleted)==0)
    
  def tearDown(self):
    Post.objects.all().delete()    