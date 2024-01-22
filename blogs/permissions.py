from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'You are not creator of this blog'

    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """


    def has_permission(self, request, view):
        print("coderscoderscoders")
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        print("jkahsdkjahsdjkhasjikd")
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user