"""
Middleware for automatic audit logging
"""
import json
from django.utils.deprecation import MiddlewareMixin
from saleor_extensions.audit.models import AuditLog


class AuditLogMiddleware(MiddlewareMixin):
    """
    Middleware to automatically log user activities
    """
    def process_request(self, request):
        # Store request info for later use in views
        request._audit_info = {
            'ip_address': self.get_client_ip(request),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'request_path': request.path,
        }
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    @staticmethod
    def log_action(request, action, model_name=None, object_id=None, 
                   object_repr=None, changes=None, branch_id=None, region_code=None):
        """
        Helper method to create audit log entry
        
        Args:
            request: HttpRequest object
            action: Action type (CREATE, UPDATE, DELETE, etc.)
            model_name: Model name
            object_id: Object ID
            object_repr: String representation of object
            changes: Dict of field changes
            branch_id: Branch ID (if applicable)
            region_code: Region code (if applicable)
        """
        audit_info = getattr(request, '_audit_info', {})
        
        # Get user information
        user = getattr(request, 'user', None)
        user_id = str(user.id) if user and hasattr(user, 'id') and user.is_authenticated else ''
        username = user.username if user and hasattr(user, 'username') and user.is_authenticated else ''
        user_email = user.email if user and hasattr(user, 'email') and user.is_authenticated else ''
        
        AuditLog.objects.create(
            user_id=user_id,
            username=username,
            user_email=user_email,
            action=action,
            model_name=model_name or '',
            object_id=str(object_id) if object_id else '',
            object_repr=object_repr or '',
            changes=changes or {},
            ip_address=audit_info.get('ip_address'),
            user_agent=audit_info.get('user_agent', ''),
            request_path=audit_info.get('request_path', ''),
            branch_id=str(branch_id) if branch_id else '',
            region_code=region_code or '',
        )


