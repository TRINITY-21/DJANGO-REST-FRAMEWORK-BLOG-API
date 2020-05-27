from rest_framework import serializers
from .models import UserProfile,ProfileFeedItem

class HelloSerializer(serializers.Serializer):
    """serializers a name field for testing our API View"""

    name = serializers.CharField(max_length = 10)


class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile objects"""

    class Meta:
        model = UserProfile
        fields = ['id','name','email','password']
        extra_kwargs = {'password':{'write_only':True}}

        def create(self, validated_data):
            """create and return a new user"""
            
            user = UserProfile(
                email = validated_data['email'],
                name  = validated_data['name'],
            )

            user.set_password(validated_data['password'])
            user.save()

            return user

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """A serializer for profile feed"""


    class Meta:
        model= ProfileFeedItem
        fields = ['id','user_profile','status_text','created_on']
        extra_kwargs = {'user_profile': {'write_only':True}}

