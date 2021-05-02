from datetime import datetime
from Users.models import User
from Users.views import is_autherized
from Posts.models import Post
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Posts.serializer import PostsSerializer, PostValidator
from django.core.paginator import Paginator
import json
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log',level=logging.DEBUG)

def get_user_obj(user=None):
    #Returns User Objects corresponding to the username
    return User.objects.get(username=user)

# This method is there to create posts
@api_view(['POST'])
def Createpost(request):
   
    if request.method == "POST":
        username = request.query_params.get('username')
        text = request.query_params.get('text')
        if is_autherized(request,username):
            validate = PostValidator(request.query_params,request.FILES)
            if not validate.is_valid():
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Invalid username or post text"}
                logger.error(error)                    
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)

            try:
                user = get_user_obj(username)
                new_post = Post(username=user,text=text)
                new_post.save()
                serializer = PostsSerializer(new_post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "User Does not exist"}
                logger.error(e)                    
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)        

# This method displays all tweets in a paged faishon
@api_view(['GET'])
def Timeline(request,username):
    
    if is_autherized(request,username):
        try:
            page_no = int(request.query_params.get('page',1))
            userObj = get_user_obj(username)
            if page_no < 1:
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Please pass an integer value (starting with 1) as Page Number"}
                logger.error(error)                    
                return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)
            
            posts = Post.objects.filter(username=userObj)
            paginator = Paginator(posts,5) #shows 5 posts per page
            page_num = paginator.get_page(page_no)
            post_objs = page_num.object_list 
            serializer = PostsSerializer(post_objs,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "No posts to show"}
            logger.error(e)                    
            return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST) 
    else:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                            'Error_Message': "Authentication failed. Please login"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)        

# This method deletes the post by id
@api_view(['DELETE'])
def Deletepost(request,post_id=None):
   
    try:
        post = Post.objects.get(id=post_id)
        username = post.username.username
        if is_autherized(request,username):
            serializer = PostsSerializer(post)
            post.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)       
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_Message': "This post no longer exists"}
        logger.error(e)    
        return Response(json.dumps(error), status=status.HTTP_400_BAD_REQUEST)     

#This method shows specific posts as per id
@api_view(['GET'])
def Showpost(request,post_id=None):
    try:
        post = Post.objects.filter(id=post_id)
        username = post.username.username
        if is_autherized(request,username):
            replies = Post.objects.get(id=post_id).reply.all()
            postNreply = post.union(replies)
            serializer = PostsSerializer(postNreply,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                                'Error_Message': "Authentication failed. Please login"}
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(e)
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                    'Error_Message': "This post no longer exists"}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def all_posts(request):
   
    posts = Post.objects.all()
    serializer = PostsSerializer(posts,many=True)