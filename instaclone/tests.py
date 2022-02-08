from django.test import TestCase
from django.contrib.auth.models import User
from .models import *

import datetime as dt
# Create your tests here.

class ProfileTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(username='ebay',password= 'qwerty')
    self.ebay =Profile(bio='i love code',user=user)
  def test_instance(self):
    self.assertTrue(isinstance(self.ebay,Profile))  
    
  def test_save_method(self):
      self.ebay.save_profile()
      profiles =Profile.objects.all()
      self.assertTrue(len(profiles)>0)
      
      
class LikesTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(username='ebay',password= 'qwerty')
    profile = Profile.objects.create(user=user,bio='music and code', profile_photo ='ebay.jpg')
    post = Post.objects.create(user=user,image='ebay.jpg', image_name='me',image_caption= 'i can',profile=profile,likes=2,date='2020-12-02' )
    Likes.objects.create(user=user,post=post)
    
    self.ebay=Likes(user=user)
    
  def test_instance(self):
    self.assertTrue(isinstance(self.ebay,Likes))  
    
class CommentTestCase(TestCase):    
  def setUp(self):
    user = User.objects.create(username='ebay',password= 'qwerty')
    profile = Profile.objects.create(user=user,bio='music and code', profile_photo ='ebay.jpg')
    post = Post.objects.create(user=user,image='ebay.jpg', image_name='me',image_caption= 'i can',profile=profile,likes=2,date='2020-12-02' )
    
    self.ebay=Comment(user=user, date='2020-12-2',post=post,comment="yes we can")
  def test_instance(self):
    self.assertTrue(isinstance(self.ebay,Comment))
    
    
class FollowTest(TestCase):
  def setUp(self):
    user = User.objects.create(username='ebay',password= 'qwerty')
    
    self.ebay=Follow(follower=user,following=user)
    
  def test_instance(self):
    self.assertTrue(isinstance(self.ebay,Follow))
  
class PostTest(TestCase):
  def setUp(self):
    user = User.objects.create(username='ebay',password= 'qwerty')
    profile = Profile.objects.create(user=user,bio='music and code', profile_photo ='ebay.jpg')

    self.ebay =Post(user=user,image='ebay.jpg',image_name='me',image_caption= 'i can',profile=profile,likes=2,date='2020-12-02')
    
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