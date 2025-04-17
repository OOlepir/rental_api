from rest_framework.permissions import BasePermission


class OnlyOwnerChangeStatus(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["PUT", "PATCH"]:
            if status := request.data.get('status'):
                if status != obj.status:
                    return obj.property.owner == request.user
        return True