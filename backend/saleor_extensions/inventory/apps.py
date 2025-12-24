from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'saleor_extensions.inventory'
    verbose_name = 'Inventory Management'

    def ready(self):
        # Import schema to register GraphQL types
        try:
            import saleor_extensions.inventory.schema  # noqa: F401
        except ImportError:
            pass
