from django.urls import path
from Posts import views
 
urlpatterns = [
    path('create', views.Createpost),
    path('<str:username>/', views.Timeline), 
    path('<int:post_id>/delete', views.Deletpost),
    path('<int:post_id>', views.Showpost), 
    path('all_posts', views.all_posts), #debugging
]