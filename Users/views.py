from django.shortcuts import render
from Users.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Users.serializer import UserSerializer
import json
import logging
import datetime
from django.conf import settings
import jwt

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG,)

EXP_TIME = datetime.timedelta(hours=1)

# This method allows user to signup
@api_view(['POST'])
def AccountSignup(request):
    # This is a validation statement which is validating things on the serializer side 
    # if they are valid they're saved else an error is thrown
    serializer = UserSerializer(data=request.query_params)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

def GetToken(username):
    try:
        user = User.objects.get(username=username)
        if user:
            try:
                payload = {'id':user.id,'username':user.username,'exp':datetime.datetime.utcnow()+EXP_TIME}
                token = {'token':jwt.encode(payload,settings.AUTH_TOKEN).decode('utf8')}
                                # jwt.encode({'exp': datetime.utcnow()}, 'secret')
                return token
            except Exception as e:
                error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Error generating Auth Token"}
                logger.error(e)
                return Response(error, status=status.HTTP_403_FORBIDDEN)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid Username or Password"}
            return Response(error, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Internal Server Error"}
        logger.error(e) 
        return Response(error,status=status.HTTP_400_BAD_REQUEST)   

@api_view(['POST'])
def Login(request,username=None,password=None):
    
    username = request.query_params.get('username')
    password = request.query_params.get('password')
    try:
        user = User.objects.get(username=username)
        if user.password == password:
            token = GetToken(username)
            user.token = token['token']
            user.save()
            request.session['authtoken'] = token
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid Username or Password"}
            return Response(error,status=status.HTTP_400_BAD_REQUEST) 
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid Username"}
        logger.error(e) 
        return Response(error,status=status.HTTP_400_BAD_REQUEST)         

def Auth(request,username):
    try:
        token = request.session.get('authtoken').get('token')
        payload = jwt.decode(token,settings.AUTH_TOKEN)
        user = User.objects.get(username=username)
        if payload.get('username') == user.username:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_403_FORBIDDEN,
                        'Error_Message': "Invalid User"}
            logger.error(error)
            return Response(error,status=status.HTTP_403_FORBIDDEN) 
    except (jwt.ExpiredSignature, jwt.DecodeError, jwt.InvalidTokenError) as e:
        error = {'Error_code': status.HTTP_403_FORBIDDEN,
                        'Error_Message': "Token is Invalid/Expired"}
        logger.error(e)
        return Response(error,status=status.HTTP_403_FORBIDDEN) 
    except Exception as e:
        error = {'Error_code': status.HTTP_403_FORBIDDEN,
                        'Error_Message': "Internal Server Error"}
        logger.error(e) 
        return Response(error,status=status.HTTP_403_FORBIDDEN) 
 
def is_autherized(request,username):
    validation = Auth(request,username)
    if validation.status_code == 200:
        return True
    else:
        return False

# This methods allow users to update their account details
@api_view(['PUT'])
def AccountUpdate(request,username):
    try:
        country = request.query_params.get('country')
        user = User.objects.get(username=username)
        user.country = country
        user.save()
        serializer = UserSerializer(user)
        logger.error("Account Update successful")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid details"}
        logger.error("AccountUpdate: Error: "+str(e))
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

# This methods allow users to follow other users
@api_view(['PUT'])
def FollowUser(request,loggedin_user,user):
    try:
        cur_user=User.objects.get(username=loggedin_user)
        fol_user=User.objects.get(username=user)
        cur_user.following.add(fol_user)
        cur_user.save()
        serializer = UserSerializer(cur_user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Request Failed. Invalid Details"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)  


# This methods allow users to unfollow other users
@api_view(['PUT'])
def unfollow(request,loggedin_user,user):
    try:
        cur_user=User.objects.get(username=loggedin_user)
        fol_user=User.objects.get(username=user)
        cur_user.following.remove(fol_user)
        cur_user.save()
        serializer = UserSerializer(cur_user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Request Failed. Invalid Details"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)  


# This methods allow users to see who are following them
@api_view(['GET'])
def GetFollowers(request,username):
    try:
        user = User.objects.get(username=username)
        followers = user.followers.all()
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "User does not exist"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST)            


# This methods allow users to see all users they're following
@api_view(['GET'])
def GetFollowing(request,username):
    try:
        user = User.objects.get(username=username)
        following = user.following.all()
        serializer = UserSerializer(following, many=True)
        return Response(serializer.data)
    except Exception as e:
        error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "User does not exist"}
        logger.error(e)
        return Response(error, status=status.HTTP_400_BAD_REQUEST) 

       

@api_view(['GET'])
def users(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)        