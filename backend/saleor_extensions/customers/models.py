from django.db import models
from saleor_extensions.branches.models import Branch


class CustomerGroup(models.Model):
    """Customer groups (Retail, Loyalty, etc.)"""
    GROUP_TYPE_CHOICES = [
        ('RETAIL', 'Retail Customer'),
        ('LOYALTY', 'Loyalty Customer'),
        ('VIP', 'VIP Customer'),
        ('WHOLESALE', 'Wholesale Customer'),
        ('CORPORATE', 'Corporate Customer'),
    ]
    
    name = models.CharField(max_length=200, unique=True)
    group_type = models.CharField(max_length=50, choices=GROUP_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    # Benefits
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        null=True,
        blank=True
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customer_groups'
        verbose_name = 'Customer Group'
        verbose_name_plural = 'Customer Groups'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CustomerProfile(models.Model):
    """Extended customer profile information"""
    # Link to Saleor User model
    customer = models.OneToOneField(
        'account.User',
        on_delete=models.CASCADE,
        related_name='customer_profile'
    )
    
    # Basic information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Group assignment
    customer_group = models.ForeignKey(
        CustomerGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='customers'
    )
    
    # Preferences
    preferred_branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_customers'
    )
    preferred_currency = models.CharField(max_length=3, blank=True)
    preferred_language = models.CharField(max_length=10, default='en')
    
    # Loyalty information
    loyalty_points = models.IntegerField(default=0)
    total_spent = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total_orders = models.IntegerField(default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
    email_opt_in = models.BooleanField(default=True)
    sms_opt_in = models.BooleanField(default=False)
    
    # Metadata
    notes = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_order_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'customer_profiles'
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profiles'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['customer_group', 'is_active']),
            models.Index(fields=['preferred_branch']),
            models.Index(fields=['loyalty_points']),
        ]
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"


class LoyaltyTransaction(models.Model):
    """Loyalty points transactions"""
    TRANSACTION_TYPE_CHOICES = [
        ('EARNED', 'Points Earned'),
        ('REDEEMED', 'Points Redeemed'),
        ('EXPIRED', 'Points Expired'),
        ('ADJUSTED', 'Points Adjusted'),
    ]
    
    customer_profile = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='loyalty_transactions'
    )
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    points = models.IntegerField()
    balance_after = models.IntegerField()
    
    # Reference
    reference_type = models.CharField(max_length=50, blank=True)  # e.g., "ORDER", "MANUAL"
    reference_id = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'loyalty_transactions'
        verbose_name = 'Loyalty Transaction'
        verbose_name_plural = 'Loyalty Transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['customer_profile', 'created_at']),
            models.Index(fields=['reference_type', 'reference_id']),
        ]
    
    def __str__(self):
        return f"{self.transaction_type} - {self.points} points for {self.customer_profile.email}"


class CustomerSupportTicket(models.Model):
    """Customer support tickets"""
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    
    ticket_number = models.CharField(max_length=100, unique=True)
    customer_profile = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name='support_tickets'
    )
    
    subject = models.CharField(max_length=500)
    description = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    
    # Assignment
    assigned_to = models.CharField(max_length=255, blank=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='support_tickets'
    )
    
    # Resolution
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customer_support_tickets'
        verbose_name = 'Customer Support Ticket'
        verbose_name_plural = 'Customer Support Tickets'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ticket_number']),
            models.Index(fields=['customer_profile', 'status']),
            models.Index(fields=['status', 'priority', 'created_at']),
        ]
    
    def __str__(self):
        return f"Ticket {self.ticket_number} - {self.subject}"

