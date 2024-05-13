from rest_framework.permissions import BasePermission

class IsManager(BasePermission):
    """
    Custom permission class to allow access only to users in the "Manager" group.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and belongs to the "Manager" group
        return request.user.groups.filter(name='Manager').exists()

class IsDeliveryCrew(BasePermission):
    """
    Custom permission class to allow access only to users in the "Delivery Crew" group.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and belongs to the "Delivery Crew" group
        return request.user.groups.filter(name='Delivery Crew').exists()
    
class IsDeliveryCrewOrManager(BasePermission):
    def has_permission(self, request, view):
        return (
            IsDeliveryCrew().has_permission(request, view) or
            IsManager().has_permission(request, view)
        )

