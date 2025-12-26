"""
Utility functions for permission checking
"""
from typing import List, Optional
from saleor_extensions.permissions.models import (
    Role, Permission, RolePermission, UserRole, BranchAccess
)


class PermissionChecker:
    """Utility class for checking user permissions"""
    
    @staticmethod
    def has_permission(user_id: str, permission_code: str) -> bool:
        """
        Check if user has a specific permission
        
        Args:
            user_id: User ID
            permission_code: Permission code to check
        
        Returns:
            bool: True if user has permission
        """
        try:
            permission = Permission.objects.get(code=permission_code, is_active=True)
        except Permission.DoesNotExist:
            return False
        
        # Get user roles
        user_roles = UserRole.objects.filter(
            user_id=user_id,
            is_active=True
        ).select_related('role').prefetch_related('role__permissions__permission')
        
        for user_role in user_roles:
            # Check if role has permission
            role_permission = RolePermission.objects.filter(
                role=user_role.role,
                permission=permission,
                allowed=True
            ).first()
            
            if role_permission:
                return True
        
        return False
    
    @staticmethod
    def has_menu_access(user_id: str, menu_path: str) -> bool:
        """
        Check if user has access to a menu/module
        
        Args:
            user_id: User ID
            menu_path: Menu path (e.g., "orders.fulfillment")
        
        Returns:
            bool: True if user has access
        """
        permissions = Permission.objects.filter(
            menu_path=menu_path,
            permission_type__in=['MENU', 'MODULE'],
            is_active=True
        )
        
        for permission in permissions:
            if PermissionChecker.has_permission(user_id, permission.code):
                return True
        
        return False
    
    @staticmethod
    def can_access_branch(user_id: str, branch_id: str) -> bool:
        """
        Check if user can access a specific branch
        
        Args:
            user_id: User ID
            branch_id: Branch ID
        
        Returns:
            bool: True if user can access branch
        """
        # Check explicit branch access
        branch_access = BranchAccess.objects.filter(
            user_id=user_id,
            branch_id=branch_id,
            is_active=True
        ).first()
        
        if branch_access:
            return True
        
        # Check via user roles
        user_roles = UserRole.objects.filter(
            user_id=user_id,
            is_active=True
        ).select_related('role')
        
        for user_role in user_roles:
            # Check if role allows all branches
            if user_role.can_access_all_branches or user_role.role.can_access_all_branches:
                return True
            
            # Check if branch is assigned to role
            if user_role.branch_id == branch_id:
                return True
            
            # Check default branches for role
            if user_role.role.default_branches.filter(id=branch_id).exists():
                return True
        
        return False
    
    @staticmethod
    def get_user_branches(user_id: str) -> List[str]:
        """
        Get list of branch IDs user can access
        
        Args:
            user_id: User ID
        
        Returns:
            List of branch IDs
        """
        branch_ids = set()
        
        # Get explicit branch access
        explicit_access = BranchAccess.objects.filter(
            user_id=user_id,
            is_active=True
        ).values_list('branch_id', flat=True)
        
        branch_ids.update(str(bid) for bid in explicit_access)
        
        # Get via roles
        user_roles = UserRole.objects.filter(
            user_id=user_id,
            is_active=True
        ).select_related('role')
        
        for user_role in user_roles:
            if user_role.can_access_all_branches or user_role.role.can_access_all_branches:
                # User can access all branches - return empty list to indicate all
                return []
            
            if user_role.branch:
                branch_ids.add(str(user_role.branch.id))
            
            # Add default branches for role
            default_branches = user_role.role.default_branches.values_list('id', flat=True)
            branch_ids.update(str(bid) for bid in default_branches)
        
        return list(branch_ids)
    
    @staticmethod
    def get_user_permissions(user_id: str) -> List[str]:
        """
        Get all permission codes for a user
        
        Args:
            user_id: User ID
        
        Returns:
            List of permission codes
        """
        permission_codes = set()
        
        user_roles = UserRole.objects.filter(
            user_id=user_id,
            is_active=True
        ).select_related('role').prefetch_related(
            'role__permissions__permission'
        )
        
        for user_role in user_roles:
            role_permissions = RolePermission.objects.filter(
                role=user_role.role,
                allowed=True
            ).select_related('permission')
            
            for role_permission in role_permissions:
                if role_permission.permission.is_active:
                    permission_codes.add(role_permission.permission.code)
        
        return list(permission_codes)


