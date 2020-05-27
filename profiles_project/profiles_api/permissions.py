#if user has permission to make commit/changes to the data

from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allows users to edit thier own profile given the permissions"""

    def has_object_permission(self,request,view,obj):
        """ Check user is trying to edit thier own profile"""

        if request.method in permissions.SAFE_METHODS:
            return True

        #objects(updating own profile) the user is trying to edit has the same user id
        return obj.id == request.user.id
        


class PostOwnStatus(permissions.BasePermission):
    """"Allow users to update thier own status"""

    def has_object_permission(self, request, view, obj):

        """ Check user is trying to edit thier own Status"""

        #can view other stats but cant edit
        if request.method in permissions.SAFE_METHODS:
            return True
            
          #objects(updating own profile) the user is trying to edit has the same user id
        return obj.id == request.user.id
