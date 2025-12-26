from django.db import models


class IntegrationConfig(models.Model):
    """External system integration configurations"""
    INTEGRATION_TYPE_CHOICES = [
        ('PAYMENT_GATEWAY', 'Payment Gateway'),
        ('LOGISTICS', 'Logistics/Courier'),
        ('ERP', 'ERP System'),
        ('POS', 'POS System'),
        ('ACCOUNTING', 'Accounting System'),
        ('MARKETING', 'Marketing Platform'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    integration_type = models.CharField(max_length=50, choices=INTEGRATION_TYPE_CHOICES)
    provider_name = models.CharField(max_length=200)  # e.g., "Shiprocket", "Razorpay"
    
    # Configuration
    api_endpoint = models.URLField(blank=True)
    api_key = models.CharField(max_length=500, blank=True)
    api_secret = models.CharField(max_length=500, blank=True)
    configuration = models.JSONField(default=dict, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_test_mode = models.BooleanField(default=False)
    
    # Webhooks
    webhook_url = models.URLField(blank=True)
    webhook_secret = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'integration_configs'
        verbose_name = 'Integration Configuration'
        verbose_name_plural = 'Integration Configurations'
        indexes = [
            models.Index(fields=['integration_type', 'is_active']),
            models.Index(fields=['provider_name', 'region']),
        ]
    
    def __str__(self):
        return f"{self.provider_name} ({self.get_integration_type_display()})"


class WebhookEvent(models.Model):
    """Webhook events from external systems"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('PROCESSED', 'Processed'),
        ('FAILED', 'Failed'),
    ]
    
    integration = models.ForeignKey(
        IntegrationConfig,
        on_delete=models.CASCADE,
        related_name='webhook_events'
    )
    
    event_type = models.CharField(max_length=100)
    payload = models.JSONField(default=dict)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    # Request information
    headers = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    received_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'webhook_events'
        verbose_name = 'Webhook Event'
        verbose_name_plural = 'Webhook Events'
        ordering = ['-received_at']
        indexes = [
            models.Index(fields=['integration', 'status', 'received_at']),
            models.Index(fields=['event_type', 'received_at']),
        ]
    
    def __str__(self):
        return f"{self.integration.provider_name} - {self.event_type} ({self.status})"


class APILog(models.Model):
    """API call logs for integrations"""
    integration = models.ForeignKey(
        IntegrationConfig,
        on_delete=models.CASCADE,
        related_name='api_logs'
    )
    
    request_method = models.CharField(max_length=10)  # GET, POST, etc.
    endpoint = models.CharField(max_length=500)
    request_data = models.JSONField(default=dict, blank=True)
    
    response_status = models.IntegerField(null=True, blank=True)
    response_data = models.JSONField(default=dict, blank=True)
    
    duration_ms = models.IntegerField(null=True, blank=True)  # Request duration in milliseconds
    
    is_success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'api_logs'
        verbose_name = 'API Log'
        verbose_name_plural = 'API Logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['integration', 'created_at']),
            models.Index(fields=['is_success', 'created_at']),
            models.Index(fields=['response_status']),
        ]
    
    def __str__(self):
        status = "Success" if self.is_success else "Failed"
        return f"{self.integration.provider_name} - {self.request_method} {self.endpoint} ({status})"


