from django.db import models
from saleor_extensions.branches.models import Branch


class Role(models.Model):
    """User roles for access control"""
    ROLE_CHOICES = [
        ('SUPER_ADMIN', 'Super Admin'),
        ('ADMIN', 'Admin'),
        ('BRANCH_MANAGER', 'Branch Manager'),
        ('SALES_EXECUTIVE', 'Sales Executive'),
        ('INVENTORY_STAFF', 'Inventory Staff'),
        ('PROCESS_EXECUTIVE', 'Process Executive'),
        ('ACCOUNTANT', 'Accountant'),
        ('CUSTOMER_SERVICE', 'Customer Service'),
    ]
    
    code = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    # Branch access
    can_access_all_branches = models.BooleanField(default=False)
    default_branches = models.ManyToManyField(
        Branch,
        related_name='default_roles',
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Permission(models.Model):
    """Menu-level and feature-level permissions"""
    PERMISSION_TYPE_CHOICES = [
        ('MENU', 'Menu Access'),
        ('MODULE', 'Module Access'),
        ('ACTION', 'Action Permission'),
        ('DATA', 'Data Access'),
    ]
    
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=200)
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    # Menu/module information
    menu_path = models.CharField(max_length=200, blank=True)  # e.g., "orders.fulfillment"
    module_name = models.CharField(max_length=100, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'permissions'
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'
        ordering = ['permission_type', 'name']
        indexes = [
            models.Index(fields=['permission_type', 'is_active']),
            models.Index(fields=['module_name']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class RolePermission(models.Model):
    """Many-to-many relationship between roles and permissions"""
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='permissions'
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name='roles'
    )
    
    # Optional: allow/deny override
    allowed = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'role_permissions'
        verbose_name = 'Role Permission'
        verbose_name_plural = 'Role Permissions'
        unique_together = [['role', 'permission']]
        indexes = [
            models.Index(fields=['role', 'allowed']),
        ]
    
    def __str__(self):
        status = "Allowed" if self.allowed else "Denied"
        return f"{self.role.name} - {self.permission.name} ({status})"


class UserRole(models.Model):
    """User role assignments"""
    # Link to Saleor User
    user = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        related_name='user_roles'
    )
    
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='users'
    )
    
    # Branch access restrictions
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='assigned_users',
        null=True,
        blank=True
    )
    can_access_all_branches = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    assigned_by = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'user_roles'
        verbose_name = 'User Role'
        verbose_name_plural = 'User Roles'
        unique_together = [['user', 'role', 'branch']]
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['role', 'is_active']),
            models.Index(fields=['branch']),
        ]
    
    def __str__(self):
        branch_str = f" at {self.branch.name}" if self.branch else " (All branches)"
        user_id = str(self.user.id) if hasattr(self.user, 'id') else 'N/A'
        return f"User {user_id} - {self.role.name}{branch_str}"


class BranchAccess(models.Model):
    """Explicit branch access for users (when not using role-based)"""
    # Link to Saleor User
    user = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        related_name='branch_accesses'
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='access_users'
    )
    
    is_active = models.BooleanField(default=True)
    granted_at = models.DateTimeField(auto_now_add=True)
    granted_by = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'branch_access'
        verbose_name = 'Branch Access'
        verbose_name_plural = 'Branch Access'
        unique_together = [['user', 'branch']]
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        user_id = str(self.user.id) if hasattr(self.user, 'id') else 'N/A'
        return f"User {user_id} - {self.branch.name}"

