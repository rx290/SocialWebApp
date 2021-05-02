
from django.contrib import admin
from django.urls import path

#importing views from our custom apps
from Posts import views as PostViews
from Users import views

urlpatterns = [
    path('admin/', admin.site.urls),

    #post view

    ## This views is responsible to create posts
    path('create', PostViews.Createpost),
    
    ## This views is responsible to show timeline of a user
    path('<str:username>/', PostViews.Timeline), 
    
    ## This views is responsible to invoke delete fucntion on a post
    path('<int:post_id>/delete', PostViews.Deletepost),
    
    ## This views is responsible to show specific post of a user
    path('<int:post_id>', PostViews.Showpost), 
    
    ## This views is responsible to show pagged view of all posts of a user and it is also being used for debugging
    path('all_posts', PostViews.all_posts), 


    #User Views

    ## This view is responsible to let a user Register
    path('signup', views.AccountSignup),
    
    ## These three views are interlinked with each other
    # These views are responsible for authentication session keeping of the current user
    path('login', views.Login),
    path('token', views.GetToken),
    path('auth', views.Auth),

    # path('<str:username>/account', views.AccountUpdate),
    
    ## This view is responsible to let a user to follow someone
    path('<str:loggedin_user>/<str:user>/follow', views.FollowUser),
    
    ## This view is responsible to see who has followed the user
    path('<str:username>/followers', views.GetFollowers),

    ## This view is responsible to see who the user is following
    path('<str:username>/following', views.GetFollowing),

    ## This is a view tho see all the users available in the database
    path('users',views.users), 
]
