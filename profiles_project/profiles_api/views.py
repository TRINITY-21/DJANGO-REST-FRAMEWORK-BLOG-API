from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import filters #searching
from rest_framework.authtoken.serializers import AuthTokenSerializer #Built in API for Auth
from rest_framework.authtoken.views import ObtainAuthToken #Obtain n trick as viewset
from rest_framework.authentication import  TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import UserProfile,ProfileFeedItem
from .permissions import UpdateOwnProfile, PostOwnStatus

# Create your views here.

class HelloApiView(APIView):
    """Test API View"""

    serializer_class = serializers.HelloSerializer


    def get(self,request,format=None):
        """Returns a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as function (get,post,put,delete)',
            'similar to traditional django',
            'its mapped manually to Urls',
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self,request):
        """Create a hello message with our name"""

        serializer = serializers.HelloSerializer(data=request.data)

    #validating our request from the serializer
        if serializer.is_valid():
            name = serializer.data.get('name')
            message  = 'Hello {0} Welcome'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=400)

    def put(self,request,pk=None):
        """Handles Updating an Object or Post"""

        return Response({'method':'put'})

    def patch(self,request,pk=None):
        """Patch request, only updates the fields provided in the request"""

        return Response({'method':'patch'})


    def delete(self,request,pk=None):
        """Delete request, only deletes an object"""

        return Response({'method':'delete'})


class HelloViewSet(viewsets.ViewSet):
    """Tests API Viewsets"""

    serializer_class = serializers.HelloSerializer

    def list(self,request):
        """Returns a hello message"""

        a_viewset = [
            'uses actions(list, create, retrieve, update, partial update',
            'automatically maps to URLs using Routers',
            'more functionallity with less code',
        ]

        return Response({'message':'Hello', "a_viewset": a_viewset})

    
    def create(self,request):
        """Creates a new hello message"""

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = "hello {0}, welcome".format(name)
            return Response({"message": message})
        else:
            return Response(serializer.errors,status=404)
    

    def retrieve(self, request,pk=None):
        """Handles the object by its ID"""

        return Response({"method": "GET"})

    def update(self,request,pk=None):
        """Handles the updaing object by its ID"""
        
        return Response({"method": "PUT"})

    
    def partialupdate(self,request,pk=None):
        """Handles the updaing part of object by its ID"""
        
        return Response({"method": "PATCH"})



    def destroy(self,request,pk=None):
        """Handles the Removing an object by its ID"""
        
        return Response({"method": "DELETE"})


class UserProfileViewset(viewsets.ModelViewSet):
    """handles creating, reading and updating profiles"""

    serializer_class = serializers.UserProfileSerializer

    #how to retrieve info from database
    queryset = UserProfile.objects.all()

    #authorizations
    authentication_classes = (TokenAuthentication,) # created as a tuple u need to attach the (,)
    permission_classes = (UpdateOwnProfile,)

    #serching through the profile
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)


class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use the obtainAPIView to validate and create a token"""
  
        return ObtainAuthToken().post(request)

class UserProfileFeedItemViewSet(viewsets.ModelViewSet):
        """handles creating, reading and updating profiles"""

        
        queryset = ProfileFeedItem.objects.all()
        serializer_class = serializers.ProfileFeedItemSerializer
        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,PostOwnStatus,)

        def perform_create(self, serializers):
            """Sets the user profile to the logged in user"""

            serializers.save(user_profile = self.request.user)
