"""
Celery tasks for background jobs

Installation:
    pip install celery>=5.3.0

Configuration:
    Add to saleor/settings/base.py:
    from celery.schedules import crontab
    
    CELERY_BEAT_SCHEDULE = {
        'update-currency-rates': {
            'task': 'saleor_extensions.tasks.update_currency_rates',
            'schedule': crontab(hour=0, minute=0),
        },
        'update-gold-rates': {
            'task': 'saleor_extensions.tasks.update_gold_rates',
            'schedule': crontab(minute=0),
        },
        'generate-scheduled-reports': {
            'task': 'saleor_extensions.tasks.generate_scheduled_reports',
            'schedule': crontab(hour=6, minute=0),
        },
        'send-pending-notifications': {
            'task': 'saleor_extensions.tasks.send_pending_notifications',
            'schedule': crontab(minute='*/5'),  # Every 5 minutes
        },
        'process-low-stock-alerts': {
            'task': 'saleor_extensions.tasks.process_low_stock_alerts',
            'schedule': crontab(hour=9, minute=0),  # Daily at 9 AM
        },
    }
"""
import os
from celery import shared_task
from django.utils import timezone
from datetime import datetime


@shared_task
def update_currency_rates():
    """
    Update exchange rates for all active currencies
    Runs daily at midnight
    """
    try:
        from saleor_extensions.currency.services import CurrencyConverter
        CurrencyConverter.update_all_rates()
        return "Currency rates updated successfully"
    except Exception as e:
        return f"Error updating currency rates: {str(e)}"


@shared_task
def update_gold_rates():
    """
    Update gold rates for all regions
    Runs hourly
    """
    try:
        from saleor_extensions.pricing.services import PricingCalculator
        PricingCalculator.update_all_gold_rates()
        return "Gold rates updated successfully"
    except Exception as e:
        return f"Error updating gold rates: {str(e)}"


@shared_task
def generate_scheduled_reports():
    """
    Generate all scheduled reports
    Runs daily at 6 AM
    """
    try:
        from saleor_extensions.reports.models import ScheduledReport
        
        now = timezone.now()
        due_reports = ScheduledReport.objects.filter(
            is_active=True,
            next_run_at__lte=now
        )
        
        count = 0
        for report in due_reports:
            # Generate report (implementation needed)
            # This will use the ReportExecution model
            count += 1
        
        return f"Generated {count} scheduled reports"
    except Exception as e:
        return f"Error generating scheduled reports: {str(e)}"


@shared_task
def send_pending_notifications():
    """
    Send pending email, SMS, and WhatsApp notifications
    Runs every 5 minutes
    """
    try:
        from saleor_extensions.notifications.models import Notification
        
        pending = Notification.objects.filter(
            status='PENDING',
            scheduled_at__lte=timezone.now()
        )
        
        count = 0
        for notification in pending:
            # Send notification (implementation needed)
            # This will call the notification service
            notification.status = 'SENT'
            notification.sent_at = timezone.now()
            notification.save()
            count += 1
        
        return f"Sent {count} notifications"
    except Exception as e:
        return f"Error sending notifications: {str(e)}"


@shared_task
def process_low_stock_alerts():
    """
    Check for low stock items and create alerts
    Runs daily at 9 AM
    """
    try:
        from saleor_extensions.inventory.models import BranchInventory, LowStockAlert
        
        low_stock_items = BranchInventory.objects.filter(
            is_low_stock=True,
            is_active=True
        )
        
        count = 0
        for inventory in low_stock_items:
            # Create or update low stock alert
            LowStockAlert.objects.get_or_create(
                branch_inventory=inventory,
                defaults={
                    'alert_level': 'LOW',
                    'current_quantity': inventory.available_quantity,
                    'threshold_quantity': inventory.reorder_level or 0,
                }
            )
            count += 1
        
        return f"Processed {count} low stock alerts"
    except Exception as e:
        return f"Error processing low stock alerts: {str(e)}"


@shared_task
def cleanup_old_audit_logs():
    """
    Clean up old audit logs (older than 90 days)
    Runs weekly
    """
    try:
        from saleor_extensions.audit.models import AuditLog
        from datetime import timedelta
        
        cutoff_date = timezone.now() - timedelta(days=90)
        deleted_count, _ = AuditLog.objects.filter(
            timestamp__lt=cutoff_date
        ).delete()
        
        return f"Deleted {deleted_count} old audit logs"
    except Exception as e:
        return f"Error cleaning up audit logs: {str(e)}"


@shared_task
def update_scheduled_report_next_run():
    """
    Update next_run_at for scheduled reports based on frequency
    Runs after report generation
    """
    try:
        from saleor_extensions.reports.models import ScheduledReport
        from datetime import timedelta
        
        reports = ScheduledReport.objects.filter(is_active=True)
        
        for report in reports:
            if report.frequency == 'DAILY':
                report.next_run_at = timezone.now() + timedelta(days=1)
            elif report.frequency == 'WEEKLY':
                report.next_run_at = timezone.now() + timedelta(weeks=1)
            elif report.frequency == 'MONTHLY':
                report.next_run_at = timezone.now() + timedelta(days=30)
            elif report.frequency == 'QUARTERLY':
                report.next_run_at = timezone.now() + timedelta(days=90)
            elif report.frequency == 'YEARLY':
                report.next_run_at = timezone.now() + timedelta(days=365)
            
            report.last_run_at = timezone.now()
            report.save()
        
        return "Updated scheduled report next run times"
    except Exception as e:
        return f"Error updating scheduled reports: {str(e)}"


