from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# Create your models here.
class UserProfileManager(BaseUserManager):
    """Helps to work with the custom user models"""

    def Create_user(self, email, name, password):
        """Creating a new user Profile"""

        #validating user inputs
        if not email:
            raise ValueError('Users must have email address')
    
        #normalize email (converting all to lowercase)
        email = self.normalize_email(email)
        #create a new user object
        user = self.model(email= email, name=name)

        #setting the password
        user.set_password(password)
        user.save(using = self._db) #using the same model created for the profile

        return user

    def create_superuser(self,name,email,password):
        """ create and saves a new superuser with given details"""

        user = self.Create_user(email,name,password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Represent a user profile inside the API"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length = 255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #managing the UserProfile
    objects = UserProfileManager()

    #logging in with email address instaed
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    #helper functions to get user info
    def get_full_name(self):
        """Required to use the user profile with the admin"""

        return self.name
        
    
    def get_short_name():
        """Users short name"""

        return self.name

    def __str__(self):
        """Uses this function to convert an object to string"""
        return self.name


class ProfileFeedItem(models.Model):
    """Used to get the status of profile update"""

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        """Returns model as a string"""
        return self.status_text