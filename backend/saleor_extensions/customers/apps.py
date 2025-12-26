from django.apps import AppConfig


class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saleor_extensions.customers'
    verbose_name = 'Customers'


