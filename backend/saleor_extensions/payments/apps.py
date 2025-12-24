from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saleor_extensions.payments'
    verbose_name = 'Payments'

