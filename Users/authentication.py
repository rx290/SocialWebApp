import jwt
import datetime
from Users.models import User
from rest_framework import status
from requests.models import Response
from joblib import logger
from Users.serializer import UserSerializer
from SocialWebApp import settings
  
#session expiry time
EXP_TIME = datetime.timedelta(minutes=5)
 


## This method is defined to get generated access token from the server side to maintain a session
def GetToken(username):

    try:
        # search the user class objects and see whether there is an object of 
        # the particular username passed as a pram?
        user = User.objects.get(username=username)
        # if the user does esxist then fetch it's id, username and set the session expiry time from above 
        if user:
            try:
                # then encode the entire data along with the recieved authentication token and set decoding format as utf8
                # send it back as a json response
                payload = {'id':user.id,'username':user.username,'exp':datetime.datetime.utcnow()+EXP_TIME}
                token = {'token':jwt.encode(payload,settings.AUTH_TOKEN).decode('utf8')}
                return token

            # if something isn't going according to the plane then raise some exception
            except Exception as e:
                # from status fetch the 400 bad request error to create a log and to 
                # notify the user that server side isn't generating access tokens
                error = {'Error_code': status.HTTP_403_FORBIDDEN ,
                        'Error_Message': "Error generating Auth Token"}
                # adding the errors to the run log of the application
                logger.error(e)
                return Response(error, status=status.HTTP_403_FORBIDDEN)
        else:
            # if the user does not exist then post an error of sending 
            # a bad request to the server as no such user exists
            error = {'Error_code': status.HTTP_400_BAD_REQUEST,
                        'Error_Message': "Invalid Username or Password"}
            return Response(error, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        # if all the cases mentioned above fails then there is a proxy or server side communication issues
        # hence raise a 500 error
        error = {'Error_code': status.HTTP_500_INTERNAL_SERVER_ERROR ,
                        'Error_Message': "Internal Server Error"}
        logger.error(e) 
        return Response(error,status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 

# This function is responsible to authenticate the user and make them signin into the syste
# an access token is required for auth to work     
def Auth(request,username):
   
   # here we are trying to decode the access token and then trying to find the user if user is found
   # and access token is verified then they're allowed to sign in as an 
   # authentic user
    try:
        token = request.session.get('authtoken').get('token')
        payload = jwt.decode(token,settings.AUTH_TOKEN)
        user = User.objects.get(username=username)
        if payload.get('username') == user.username:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            error = {'Error_code': status.HTTP_404_NOT_FOUND,
                        'Error_Message': "Invalid User"}
            logger.error(error)
            return Response(error,status=status.HTTP_404_NOT_FOUND) 
    
    # this block of code is verifying generated access token
    except (jwt.ExpiredSignature, jwt.DecodeError, jwt.InvalidTokenError) as e:
        error = {'Error_code': status.HTTP_403_FORBIDDEN,
                        'Error_Message': "Token is Invalid/Expired"}
        logger.error(e)
        return Response(error,status=status.HTTP_403_FORBIDDEN) 
    except Exception as e:
        error = {'Error_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'Error_Message': "Internal Server Error"}
        logger.error(e) 
        return Response(error,status=status.HTTP_403_FORBIDDEN) 
 

# This is a function which compares the given prams to the recorded prams and let us know 
# if they match or not
@api_view(['POST'])
def Login(request,username=None,password=None):

    # fetching username and password via request module
    username = request.query_params.get('username')
    password = request.query_params.get('password')
    try:
        # verifying credentials and validating access token
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