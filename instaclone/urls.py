from django.urls import path
from . import views


urlpatterns = [
  path('',views.index,name='index'),
  path('posts/',views.new_post, name ='new_post'),
  path('profile/<username>',views.profile, name='profile'),
  path('post/<uuid:post_id>',views.post_details,name='post_details'),
  path('post/<uuid:post_id>/likes',views.likes,name='postlikes'),
  path('profile/<username>/follow/<option>',views.follow,name ='follow'),
  path('profile/<username>/new',views.update_profile,name ='update_profile'),
  path('search/',views.search_results,name ='search_results'),
  
  
  
]