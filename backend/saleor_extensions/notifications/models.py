from django.db import models


class EmailTemplate(models.Model):
    """Email notification templates"""
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=500)
    
    # Template content
    body_text = models.TextField(blank=True)  # Plain text version
    body_html = models.TextField(blank=True)  # HTML version
    
    # Variables that can be used in template (documentation)
    available_variables = models.JSONField(default=list, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    
    # Metadata
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)  # e.g., "order", "customer", "marketing"
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'email_templates'
        verbose_name = 'Email Template'
        verbose_name_plural = 'Email Templates'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['code', 'is_active']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class SMSTemplate(models.Model):
    """SMS notification templates"""
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=100, unique=True)
    
    # Template content (SMS has character limits)
    message = models.CharField(max_length=1600)  # SMS can be up to 1600 chars with encoding
    
    # Variables that can be used
    available_variables = models.JSONField(default=list, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    
    # Metadata
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sms_templates'
        verbose_name = 'SMS Template'
        verbose_name_plural = 'SMS Templates'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['code', 'is_active']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class WhatsAppTemplate(models.Model):
    """WhatsApp Business API templates"""
    name = models.CharField(max_length=200, unique=True)
    template_id = models.CharField(max_length=200, unique=True)  # WhatsApp template ID
    
    # Template content (WhatsApp has specific format requirements)
    header = models.CharField(max_length=60, blank=True)
    body = models.TextField()  # Main message body
    footer = models.CharField(max_length=60, blank=True)
    
    # Button configuration (WhatsApp supports buttons)
    buttons_config = models.JSONField(default=list, blank=True)
    
    # Variables that can be used
    available_variables = models.JSONField(default=list, blank=True)
    
    # Settings
    is_active = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en')
    
    # Metadata
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'whatsapp_templates'
        verbose_name = 'WhatsApp Template'
        verbose_name_plural = 'WhatsApp Templates'
        ordering = ['category', 'name']
        indexes = [
            models.Index(fields=['template_id', 'is_active']),
            models.Index(fields=['category', 'language']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.template_id})"


class NotificationLog(models.Model):
    """Log of sent notifications"""
    NOTIFICATION_TYPE_CHOICES = [
        ('EMAIL', 'Email'),
        ('SMS', 'SMS'),
        ('WHATSAPP', 'WhatsApp'),
        ('PUSH', 'Push Notification'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SENT', 'Sent'),
        ('DELIVERED', 'Delivered'),
        ('FAILED', 'Failed'),
        ('BOUNCED', 'Bounced'),
    ]
    
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    template_code = models.CharField(max_length=100)
    
    # Recipient
    recipient_email = models.EmailField(blank=True)
    recipient_phone = models.CharField(max_length=20, blank=True)
    recipient_name = models.CharField(max_length=255, blank=True)
    
    # Content
    subject = models.CharField(max_length=500, blank=True)
    message = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Provider response
    provider_message_id = models.CharField(max_length=255, blank=True)
    provider_response = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    
    # Context
    triggered_by = models.CharField(max_length=100, blank=True)  # e.g., "order.created"
    reference_type = models.CharField(max_length=50, blank=True)  # e.g., "ORDER"
    reference_id = models.CharField(max_length=255, blank=True)
    
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notification_logs'
        verbose_name = 'Notification Log'
        verbose_name_plural = 'Notification Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['notification_type', 'status', 'created_at']),
            models.Index(fields=['recipient_email', 'created_at']),
            models.Index(fields=['recipient_phone', 'created_at']),
            models.Index(fields=['reference_type', 'reference_id']),
            models.Index(fields=['provider_message_id']),
        ]
    
    def __str__(self):
        recipient = self.recipient_email or self.recipient_phone
        return f"{self.notification_type} to {recipient} - {self.status}"


class NotificationTrigger(models.Model):
    """Configure which notifications to send for specific events"""
    TRIGGER_EVENT_CHOICES = [
        ('ORDER_CREATED', 'Order Created'),
        ('ORDER_CONFIRMED', 'Order Confirmed'),
        ('ORDER_SHIPPED', 'Order Shipped'),
        ('ORDER_DELIVERED', 'Order Delivered'),
        ('ORDER_CANCELLED', 'Order Cancelled'),
        ('PAYMENT_RECEIVED', 'Payment Received'),
        ('RETURN_REQUESTED', 'Return Requested'),
        ('RETURN_APPROVED', 'Return Approved'),
        ('CLICK_COLLECT_READY', 'Click & Collect Ready'),
        ('LOW_STOCK_ALERT', 'Low Stock Alert'),
        ('CUSTOMER_REGISTERED', 'Customer Registered'),
        ('LOYALTY_POINTS_EARNED', 'Loyalty Points Earned'),
        ('PROMOTION_AVAILABLE', 'Promotion Available'),
    ]
    
    trigger_event = models.CharField(max_length=50, choices=TRIGGER_EVENT_CHOICES, unique=True)
    
    # Template assignments
    email_template = models.ForeignKey(
        EmailTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='email_triggers'
    )
    sms_template = models.ForeignKey(
        SMSTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sms_triggers'
    )
    whatsapp_template = models.ForeignKey(
        WhatsAppTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='whatsapp_triggers'
    )
    
    # Settings
    send_email = models.BooleanField(default=True)
    send_sms = models.BooleanField(default=False)
    send_whatsapp = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_triggers'
        verbose_name = 'Notification Trigger'
        verbose_name_plural = 'Notification Triggers'
        ordering = ['trigger_event']
    
    def __str__(self):
        return f"{self.get_trigger_event_display()}"

