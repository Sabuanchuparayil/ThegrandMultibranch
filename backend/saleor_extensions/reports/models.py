from django.db import models
from saleor_extensions.branches.models import Branch


class ReportDefinition(models.Model):
    """Report definitions and configurations"""
    REPORT_TYPE_CHOICES = [
        ('SALES', 'Sales Report'),
        ('INVENTORY', 'Inventory Report'),
        ('CUSTOMER', 'Customer Report'),
        ('OPERATIONAL', 'Operational Report'),
        ('FINANCIAL', 'Financial Report'),
        ('CUSTOM', 'Custom Report'),
    ]
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    description = models.TextField(blank=True)
    
    # Configuration
    query_config = models.JSONField(default=dict)  # Report query configuration
    column_config = models.JSONField(default=list)  # Column definitions
    filters_config = models.JSONField(default=dict)  # Available filters
    
    # Access
    is_active = models.BooleanField(default=True)
    requires_permission = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'report_definitions'
        verbose_name = 'Report Definition'
        verbose_name_plural = 'Report Definitions'
        ordering = ['report_type', 'name']
        indexes = [
            models.Index(fields=['code', 'is_active']),
            models.Index(fields=['report_type']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class ReportExecution(models.Model):
    """Report execution logs and generated reports"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('RUNNING', 'Running'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    report_definition = models.ForeignKey(
        ReportDefinition,
        on_delete=models.CASCADE,
        related_name='executions'
    )
    
    # Execution parameters
    filters = models.JSONField(default=dict)  # Applied filters
    date_from = models.DateField(null=True, blank=True)
    date_to = models.DateField(null=True, blank=True)
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='report_executions'
    )
    country = models.CharField(max_length=100, blank=True, default='')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Results
    result_data = models.JSONField(default=dict, blank=True)  # Report data
    file_url = models.URLField(blank=True)  # Exported file URL (CSV, PDF, Excel)
    file_format = models.CharField(max_length=20, blank=True)  # CSV, PDF, XLSX
    
    # Execution details
    executed_by = models.CharField(max_length=255, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'report_executions'
        verbose_name = 'Report Execution'
        verbose_name_plural = 'Report Executions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['report_definition', 'status', 'created_at']),
            models.Index(fields=['branch', 'country', 'created_at']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.report_definition.name} - {self.status} ({self.created_at.date()})"


class ScheduledReport(models.Model):
    """Scheduled report generation"""
    report_definition = models.ForeignKey(
        ReportDefinition,
        on_delete=models.CASCADE,
        related_name='schedules'
    )
    
    name = models.CharField(max_length=200)
    
    # Schedule configuration
    FREQUENCY_CHOICES = [
        ('DAILY', 'Daily'),
        ('WEEKLY', 'Weekly'),
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('YEARLY', 'Yearly'),
    ]
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    
    # Default filters
    default_filters = models.JSONField(default=dict)
    default_branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    default_country = models.CharField(max_length=100, blank=True, default='')
    
    # Recipients
    email_recipients = models.JSONField(default=list)  # List of email addresses
    
    # Format
    file_format = models.CharField(max_length=20, default='PDF')  # PDF, CSV, XLSX
    
    # Schedule
    is_active = models.BooleanField(default=True)
    next_run_at = models.DateTimeField(null=True, blank=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'scheduled_reports'
        verbose_name = 'Scheduled Report'
        verbose_name_plural = 'Scheduled Reports'
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_active', 'next_run_at']),
            models.Index(fields=['frequency']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_frequency_display()}"


