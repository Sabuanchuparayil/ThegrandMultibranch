"""
GraphQL API for Branch Inventory Operations and Stock Management
"""
import json
import os
import time

import graphene
from django.core.exceptions import ValidationError
from django.db.models import Q
from decimal import Decimal

from saleor_extensions.inventory.models import (
    BranchInventory,
    StockMovement,
    StockTransfer,
    LowStockAlert,
)
from saleor_extensions.branches.models import Branch

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".cursor", "debug.log")


def _inventory_log(location, message, data, hypothesis_id):
    try:
        abs_path = os.path.abspath(LOG_PATH)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        entry = {
            "sessionId": "debug-session",
            "runId": "debug-run1",
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data,
            "timestamp": int(time.time() * 1000),
        }
        with open(abs_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass

# Try to import DateTime and Decimal from Saleor to avoid duplicate type errors
try:
    from saleor.graphql.core.scalars import DateTime, Decimal
except ImportError:
    # Fallback to graphene types if Saleor's types are not available
    DateTime = graphene.DateTime
    Decimal = graphene.Decimal

# Import BranchType using lambda to avoid circular imports and duplicate registration
# Lambda ensures the import happens at schema creation time, not at module import time
def _get_branch_type():
    # #region agent log
    import json
    import os
    import time
    try:
        log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
        if not os.path.exists(os.path.dirname(log_path)):
            log_path = '/tmp/debug.log'
        with open(log_path, 'a') as f:
            f.write(json.dumps({
                'timestamp': int(time.time() * 1000),
                'location': 'inventory/schema.py:_get_branch_type',
                'message': 'Attempting to import BranchType',
                'data': {},
                'sessionId': 'debug-session',
                'runId': 'schema-load',
                'hypothesisId': 'H6'
            }) + '\n')
    except:
        pass
    # #endregion
    try:
        from saleor_extensions.branches.schema import BranchType
        # #region agent log
        try:
            with open(log_path, 'a') as f:
                f.write(json.dumps({
                    'timestamp': int(time.time() * 1000),
                    'location': 'inventory/schema.py:_get_branch_type',
                    'message': 'BranchType imported successfully',
                    'data': {'branch_type_module': BranchType.__module__, 'branch_type_name': BranchType.__name__},
                    'sessionId': 'debug-session',
                    'runId': 'schema-load',
                    'hypothesisId': 'H6'
                }) + '\n')
        except:
            pass
        # #endregion
        return BranchType
    except Exception as e:
        # #region agent log
        try:
            with open(log_path, 'a') as f:
                f.write(json.dumps({
                    'timestamp': int(time.time() * 1000),
                    'location': 'inventory/schema.py:_get_branch_type',
                    'message': 'BranchType import failed',
                    'data': {'error': str(e), 'error_type': type(e).__name__},
                    'sessionId': 'debug-session',
                    'runId': 'schema-load',
                    'hypothesisId': 'H6'
                }) + '\n')
        except:
            pass
        # #endregion
        raise

# Try to import BaseMutation and Error from Saleor, fallback to graphene.Mutation
try:
    from saleor.graphql.core.mutations import BaseMutation
    from saleor.graphql.core.types import Error
    _SALEOR_AVAILABLE = True
except ImportError:
    # Fallback if Saleor's BaseMutation is not available
    # Define Error class first
    class Error(graphene.ObjectType):
        field = graphene.String()
        message = graphene.String()
    
    class BaseMutation(graphene.Mutation):
        """Base mutation class"""
        class Meta:
            abstract = True
        
        @classmethod
        def perform_mutation(cls, root, info, **kwargs):
            raise NotImplementedError("Subclasses must implement perform_mutation")
        
        @classmethod
        def mutate(cls, root, info, **kwargs):
            try:
                result = cls.perform_mutation(root, info, **kwargs)
                return result
            except ValidationError as e:
                if hasattr(result, 'errors'):
                    result.errors = [Error(field=str(e), message=str(e))]
                return result
            except Exception as e:
                return cls(errors=[Error(field='__all__', message=str(e))])


# ============================================================================
# Object Types
# ============================================================================

class InventoryProductType(graphene.ObjectType):
    """Minimal Product type for admin inventory views (renamed to avoid conflict with Saleor's ProductType)."""

    id = graphene.ID()
    name = graphene.String()


class InventoryProductVariantType(graphene.ObjectType):
    """Minimal ProductVariant type for admin inventory views (renamed to avoid conflict with Saleor's ProductVariantType)."""

    id = graphene.ID()
    name = graphene.String()
    sku = graphene.String()
    product = graphene.Field(InventoryProductType)


# BranchType is imported from saleor_extensions.branches.schema to avoid duplicate type definition


class BranchInventoryType(graphene.ObjectType):
    """Branch Inventory GraphQL Type (no graphene-django dependency)."""

    id = graphene.ID()
    product_variant = graphene.Field(InventoryProductVariantType)
    branch = graphene.Field(lambda: _get_branch_type())  # Lazy import to avoid duplicate type registration
    quantity = graphene.Int()
    reserved_quantity = graphene.Int()
    low_stock_threshold = graphene.Int()
    last_updated = DateTime()
    created_at = DateTime()
    available_quantity = graphene.Int()
    is_low_stock = graphene.Boolean()

    def resolve_available_quantity(self, info):
        return getattr(self, "available_quantity", None)

    def resolve_is_low_stock(self, info):
        return getattr(self, "is_low_stock", None)


class StockMovementType(graphene.ObjectType):
    """Stock Movement GraphQL Type (no graphene-django dependency)."""

    id = graphene.ID()
    branch = graphene.Field(lambda: _get_branch_type())  # Lazy import to avoid duplicate type registration
    product_variant = graphene.Field(InventoryProductVariantType)
    movement_type = graphene.String()
    quantity = graphene.Int()
    reference_number = graphene.String()
    notes = graphene.String()
    created_by = graphene.String()
    created_at = DateTime()


class StockTransferType(graphene.ObjectType):
    """Stock Transfer GraphQL Type (no graphene-django dependency)."""

    id = graphene.ID()
    transfer_number = graphene.String()
    from_branch = graphene.Field(lambda: _get_branch_type())  # Lazy import to avoid duplicate type registration
    to_branch = graphene.Field(lambda: _get_branch_type())  # Lazy import to avoid duplicate type registration
    quantity = graphene.Int()
    status = graphene.String()
    requested_by = graphene.String()
    notes = graphene.String()
    created_at = DateTime()
    updated_at = DateTime()
    status_display = graphene.String()

    def resolve_status_display(self, info):
        try:
            return self.get_status_display()
        except Exception:
            return getattr(self, "status", None)


class LowStockAlertType(graphene.ObjectType):
    """Low Stock Alert GraphQL Type (no graphene-django dependency)."""

    id = graphene.ID()
    branch_inventory = graphene.Field(BranchInventoryType)
    current_quantity = graphene.Int()
    threshold_quantity = graphene.Int()
    status = graphene.String()
    notified_at = DateTime()
    resolved_at = DateTime()
    created_at = DateTime()


# ============================================================================
# Input Types
# ============================================================================

class StockAdjustmentInput(graphene.InputObjectType):
    """Input for stock adjustment"""
    branch_id = graphene.ID(required=True)
    product_variant_id = graphene.ID(required=True)
    quantity = graphene.Int(required=True)
    movement_type = graphene.String(required=True)
    reference_number = graphene.String()
    notes = graphene.String()
    reason = graphene.String()


class StockTransferInput(graphene.InputObjectType):
    """Input for stock transfer"""
    from_branch_id = graphene.ID(required=True)
    to_branch_id = graphene.ID(required=True)
    product_variant_id = graphene.ID(required=True)
    quantity = graphene.Int(required=True)
    notes = graphene.String()


class BulkStockAdjustmentInput(graphene.InputObjectType):
    """Input for bulk stock adjustments"""
    branch_id = graphene.ID(required=True)
    adjustments = graphene.List(graphene.NonNull(lambda: StockAdjustmentItemInput), required=True)
    reference_number = graphene.String()
    notes = graphene.String()


class StockAdjustmentItemInput(graphene.InputObjectType):
    """Input for individual stock adjustment item"""
    product_variant_id = graphene.ID(required=True)
    quantity = graphene.Int(required=True)
    movement_type = graphene.String(required=True)
    reason = graphene.String()


# ============================================================================
# Queries
# ============================================================================

class InventoryQueries(graphene.ObjectType):
    """Inventory-related queries"""
    
    # Get branch inventory by branch
    branch_inventory = graphene.List(
        BranchInventoryType,
        branch_id=graphene.ID(),
        branchId=graphene.ID(),
        search=graphene.String(),
        low_stock_only=graphene.Boolean(default_value=False),
        description="Get inventory for a specific branch"
    )
    
    # Get inventory for a specific product variant
    product_variant_inventory = graphene.List(
        BranchInventoryType,
        product_variant_id=graphene.ID(required=True),
        description="Get inventory for a product variant across all branches"
    )
    
    # Get specific branch inventory item
    inventory_item = graphene.Field(
        BranchInventoryType,
        id=graphene.ID(),
        branch_id=graphene.ID(),
        product_variant_id=graphene.ID(),
        description="Get a specific inventory item"
    )
    
    # Get stock movements
    stock_movements = graphene.List(
        StockMovementType,
        branch_id=graphene.ID(),
        product_variant_id=graphene.ID(),
        movement_type=graphene.String(),
        limit=graphene.Int(default_value=50),
        description="Get stock movement history"
    )
    
    # Get stock transfers
    stock_transfers = graphene.List(
        StockTransferType,
        from_branch_id=graphene.ID(),
        to_branch_id=graphene.ID(),
        status=graphene.String(),
        limit=graphene.Int(default_value=50),
        description="Get stock transfer history"
    )
    
    # Get low stock alerts
    low_stock_alerts = graphene.List(
        LowStockAlertType,
        branch_id=graphene.ID(),
        status=graphene.String(),
        description="Get low stock alerts"
    )
    
    def resolve_branch_inventory(self, info, branch_id=None, branchId=None, search=None, low_stock_only=False):
        """Get inventory for a branch"""
        merged_branch_id = branchId or branch_id

        # #region agent log
        _inventory_log(
            "inventory/schema.py:resolve_branch_inventory:entry",
            "Resolve branch inventory called",
            {"hypothesisId": "H5", "branch_id": merged_branch_id, "search": search, "low_stock_only": low_stock_only},
            "H5",
        )
        # #endregion

        queryset = BranchInventory.objects.select_related("branch", "product_variant").all()
        
        if merged_branch_id:
            queryset = queryset.filter(branch_id=merged_branch_id)
        
        if search:
            queryset = queryset.filter(
                Q(product_variant__name__icontains=search)
                | Q(product_variant__sku__icontains=search)
                | Q(branch__name__icontains=search)
            )
        
        if low_stock_only:
            queryset = [item for item in queryset if item.is_low_stock]

        result_count = queryset.count() if hasattr(queryset, "count") else len(queryset)

        # #region agent log
        _inventory_log(
            "inventory/schema.py:resolve_branch_inventory:exit",
            "Resolve branch inventory completed",
            {"hypothesisId": "H5", "count": result_count},
            "H5",
        )
        # #endregion
        
        return queryset
    
    def resolve_product_variant_inventory(self, info, product_variant_id):
        """Get inventory for a product variant across branches"""
        return BranchInventory.objects.select_related(
            'branch', 'product_variant'
        ).filter(product_variant_id=product_variant_id)
    
    def resolve_inventory_item(self, info, id=None, branch_id=None, product_variant_id=None):
        """Get a specific inventory item"""
        try:
            if id:
                return BranchInventory.objects.select_related(
                    'branch', 'product_variant'
                ).get(id=id)
            elif branch_id and product_variant_id:
                return BranchInventory.objects.select_related(
                    'branch', 'product_variant'
                ).get(branch_id=branch_id, product_variant_id=product_variant_id)
            else:
                raise ValidationError("Either id or both branch_id and product_variant_id must be provided")
        except BranchInventory.DoesNotExist:
            return None
    
    def resolve_stock_movements(self, info, branch_id=None, product_variant_id=None, 
                                movement_type=None, limit=50):
        """Get stock movement history"""
        queryset = StockMovement.objects.select_related(
            'branch', 'product_variant'
        ).order_by('-created_at')[:limit]
        
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        if product_variant_id:
            queryset = queryset.filter(product_variant_id=product_variant_id)
        if movement_type:
            queryset = queryset.filter(movement_type=movement_type)
        
        return queryset
    
    def resolve_stock_transfers(self, info, from_branch_id=None, to_branch_id=None,
                                status=None, limit=50):
        """Get stock transfer history"""
        queryset = StockTransfer.objects.select_related(
            'from_branch', 'to_branch', 'product_variant'
        ).order_by('-created_at')[:limit]
        
        if from_branch_id:
            queryset = queryset.filter(from_branch_id=from_branch_id)
        if to_branch_id:
            queryset = queryset.filter(to_branch_id=to_branch_id)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset
    
    def resolve_low_stock_alerts(self, info, branch_id=None, status=None):
        """Get low stock alerts"""
        queryset = LowStockAlert.objects.select_related(
            'branch_inventory__branch', 'branch_inventory__product_variant'
        ).filter(status='ACTIVE')
        
        if branch_id:
            queryset = queryset.filter(branch_inventory__branch_id=branch_id)
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset


# ============================================================================
# Mutations
# ============================================================================

class StockAdjustment(BaseMutation):
    """Adjust stock (increase or decrease)"""
    
    class Meta:
        description = "Adjust stock quantity for a product variant at a branch"
        error_type_class = Error
    
    class Arguments:
        input = StockAdjustmentInput(required=True)
    
    inventory_item = graphene.Field(BranchInventoryType)
    stock_movement = graphene.Field(StockMovementType)
    
    @classmethod
    def perform_mutation(cls, root, info, input):
        """Perform stock adjustment"""
        from saleor.product.models import ProductVariant
        
        branch = Branch.objects.get(id=input['branch_id'])
        product_variant = ProductVariant.objects.get(id=input['product_variant_id'])
        quantity = input['quantity']
        movement_type = input['movement_type']
        
        # Get or create inventory item
        inventory_item, created = BranchInventory.objects.get_or_create(
            branch=branch,
            product_variant=product_variant,
            defaults={
                'quantity': 0,
                'reserved_quantity': 0,
            }
        )
        
        # Calculate new quantity based on movement type
        if movement_type in ['IN', 'TRANSFER_IN', 'RETURN']:
            inventory_item.quantity += quantity
        elif movement_type in ['OUT', 'TRANSFER_OUT']:
            if inventory_item.quantity < quantity:
                raise ValidationError(
                    f"Insufficient stock. Available: {inventory_item.quantity}, Requested: {quantity}"
                )
            inventory_item.quantity -= quantity
        elif movement_type == 'ADJUSTMENT':
            # For adjustments, quantity can be positive or negative
            new_quantity = inventory_item.quantity + quantity
            if new_quantity < 0:
                raise ValidationError("Adjustment would result in negative stock")
            inventory_item.quantity = new_quantity
        
        inventory_item.save()
        
        # Create stock movement record
        stock_movement = StockMovement.objects.create(
            branch=branch,
            product_variant=product_variant,
            movement_type=movement_type,
            quantity=abs(quantity),
            reference_number=input.get('reference_number', ''),
            notes=input.get('notes', ''),
            created_by=info.context.user.username if info.context.user.is_authenticated else '',
        )
        
        result = cls()
        result.inventory_item = inventory_item
        result.stock_movement = stock_movement
        result.errors = []
        return result


class BulkStockAdjustment(BaseMutation):
    """Adjust stock for multiple items at once"""
    
    class Meta:
        description = "Adjust stock quantities for multiple product variants at a branch in a single operation"
        error_type_class = Error
    
    class Arguments:
        branch_id = graphene.ID(required=True)
        adjustments = graphene.List(StockAdjustmentItemInput, required=True)
        reference_number = graphene.String()
        notes = graphene.String()
    
    inventory_items = graphene.List(BranchInventoryType)
    stock_movements = graphene.List(StockMovementType)
    success_count = graphene.Int()
    error_count = graphene.Int()
    
    @classmethod
    def perform_mutation(cls, root, info, branch_id, adjustments, 
                        reference_number=None, notes=None):
        """Perform bulk stock adjustment"""
        from saleor.product.models import ProductVariant
        
        branch = Branch.objects.get(id=branch_id)
        inventory_items = []
        stock_movements = []
        success_count = 0
        error_count = 0
        
        for adjustment in adjustments:
            try:
                product_variant = ProductVariant.objects.get(
                    id=adjustment['product_variant_id']
                )
                quantity = adjustment['quantity']
                movement_type = adjustment['movement_type']
                
                # Get or create inventory item
                inventory_item, created = BranchInventory.objects.get_or_create(
                    branch=branch,
                    product_variant=product_variant,
                    defaults={
                        'quantity': 0,
                        'reserved_quantity': 0,
                    }
                )
                
                # Apply adjustment
                if movement_type in ['IN', 'TRANSFER_IN', 'RETURN']:
                    inventory_item.quantity += quantity
                elif movement_type in ['OUT', 'TRANSFER_OUT']:
                    if inventory_item.quantity < quantity:
                        error_count += 1
                        continue
                    inventory_item.quantity -= quantity
                elif movement_type == 'ADJUSTMENT':
                    new_quantity = inventory_item.quantity + quantity
                    if new_quantity < 0:
                        error_count += 1
                        continue
                    inventory_item.quantity = new_quantity
                
                inventory_item.save()
                inventory_items.append(inventory_item)
                
                # Create stock movement
                stock_movement = StockMovement.objects.create(
                    branch=branch,
                    product_variant=product_variant,
                    movement_type=movement_type,
                    quantity=abs(quantity),
                    reference_number=reference_number or '',
                    notes=notes or adjustment.get('reason', ''),
                    created_by=info.context.user.username if info.context.user.is_authenticated else '',
                )
                stock_movements.append(stock_movement)
                success_count += 1
                
            except Exception as e:
                error_count += 1
                continue
        
        result = cls()
        result.inventory_items = inventory_items
        result.stock_movements = stock_movements
        result.success_count = success_count
        result.error_count = error_count
        result.errors = []
        return result


class StockTransferCreate(BaseMutation):
    """Create a stock transfer request"""
    
    class Meta:
        description = "Create a stock transfer request between two branches"
        error_type_class = Error
    
    class Arguments:
        input = StockTransferInput(required=True)
    
    stock_transfer = graphene.Field(StockTransferType)
    
    @classmethod
    def perform_mutation(cls, root, info, input):
        """Create stock transfer"""
        from saleor.product.models import ProductVariant
        
        from_branch = Branch.objects.get(id=input['from_branch_id'])
        to_branch = Branch.objects.get(id=input['to_branch_id'])
        product_variant = ProductVariant.objects.get(id=input['product_variant_id'])
        quantity = input['quantity']
        
        # Check if source branch has enough stock
        try:
            source_inventory = BranchInventory.objects.get(
                branch=from_branch,
                product_variant=product_variant
            )
            if source_inventory.available_quantity < quantity:
                raise ValidationError(
                    f"Insufficient stock at source branch. Available: {source_inventory.available_quantity}, Requested: {quantity}"
                )
        except BranchInventory.DoesNotExist:
            raise ValidationError("No inventory found at source branch")
        
        # Generate transfer number
        from datetime import datetime
        transfer_number = f"TRF-{datetime.now().strftime('%Y%m%d')}-{StockTransfer.objects.count() + 1:05d}"
        
        # Create transfer (using product_id as CharField for now)
        stock_transfer = StockTransfer.objects.create(
            transfer_number=transfer_number,
            from_branch=from_branch,
            to_branch=to_branch,
            product_id=str(product_variant.id),
            quantity=quantity,
            status='PENDING',
            notes=input.get('notes', ''),
            requested_by=info.context.user.username if info.context.user.is_authenticated else '',
        )
        
        result = cls()
        result.stock_transfer = stock_transfer
        result.errors = []
        return result


class StockTransferProcess(BaseMutation):
    """Process/approve a stock transfer"""
    
    class Meta:
        description = "Process or approve a pending stock transfer between branches"
        error_type_class = Error
    
    class Arguments:
        transfer_id = graphene.ID(required=True)
        approve = graphene.Boolean(default_value=True)
    
    stock_transfer = graphene.Field(StockTransferType)
    
    @classmethod
    def perform_mutation(cls, root, info, transfer_id, approve=True):
        """Process stock transfer"""
        stock_transfer = StockTransfer.objects.select_related(
            'from_branch', 'to_branch', 'product_variant'
        ).get(id=transfer_id)
        
        if stock_transfer.status != 'PENDING':
            raise ValidationError("Transfer is not in PENDING status")
        
        if approve:
            # Deduct from source branch
            source_inventory, _ = BranchInventory.objects.get_or_create(
                branch=stock_transfer.from_branch,
                product_variant=product_variant,
                defaults={'quantity': 0, 'reserved_quantity': 0}
            )
            
            if source_inventory.available_quantity < stock_transfer.quantity:
                raise ValidationError("Insufficient stock at source branch")
            
            source_inventory.quantity -= stock_transfer.quantity
            source_inventory.save()
            
            # Add to destination branch
            dest_inventory, _ = BranchInventory.objects.get_or_create(
                branch=stock_transfer.to_branch,
                product_variant=product_variant,
                defaults={'quantity': 0, 'reserved_quantity': 0}
            )
            dest_inventory.quantity += stock_transfer.quantity
            dest_inventory.save()
            
            # Create stock movements
            StockMovement.objects.create(
                branch=stock_transfer.from_branch,
                product_variant=product_variant,
                movement_type='TRANSFER_OUT',
                quantity=stock_transfer.quantity,
                reference_number=stock_transfer.transfer_number,
                notes=f"Transfer to {stock_transfer.to_branch.name}",
                created_by=info.context.user.username if info.context.user.is_authenticated else '',
            )
            
            StockMovement.objects.create(
                branch=stock_transfer.to_branch,
                product_variant=product_variant,
                movement_type='TRANSFER_IN',
                quantity=stock_transfer.quantity,
                reference_number=stock_transfer.transfer_number,
                notes=f"Transfer from {stock_transfer.from_branch.name}",
                created_by=info.context.user.username if info.context.user.is_authenticated else '',
            )
            
            stock_transfer.status = 'COMPLETED'
        else:
            stock_transfer.status = 'CANCELLED'
        
        stock_transfer.save()
        
        result = cls()
        result.stock_transfer = stock_transfer
        result.errors = []
        return result


class InventoryUpdateLowStockThreshold(BaseMutation):
    """Update low stock threshold for an inventory item"""
    
    class Meta:
        description = "Update the low stock threshold for a specific inventory item"
        error_type_class = Error
    
    class Arguments:
        inventory_id = graphene.ID(required=True)
        threshold = graphene.Int(required=True)
    
    inventory_item = graphene.Field(BranchInventoryType)
    
    @classmethod
    def perform_mutation(cls, root, info, inventory_id, threshold):
        """Update low stock threshold"""
        if threshold < 0:
            raise ValidationError("Threshold cannot be negative")
        
        inventory_item = BranchInventory.objects.get(id=inventory_id)
        inventory_item.low_stock_threshold = threshold
        inventory_item.save()
        
        result = cls()
        result.inventory_item = inventory_item
        result.errors = []
        return result


class InventoryMutations(graphene.ObjectType):
    """Inventory-related mutations"""
    stock_adjustment = StockAdjustment.Field()
    bulk_stock_adjustment = BulkStockAdjustment.Field()
    stock_transfer_create = StockTransferCreate.Field()
    stock_transfer_process = StockTransferProcess.Field()
    inventory_update_threshold = InventoryUpdateLowStockThreshold.Field()


# Export for schema integration
__all__ = ['InventoryQueries', 'InventoryMutations']

