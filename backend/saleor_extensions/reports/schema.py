"""
GraphQL Schema for Dashboard and Reporting Data
Provides queries for executive and branch dashboards
"""
import graphene
from django.db.models import Sum, Count, Avg, Q, F
from datetime import datetime, timedelta
from decimal import Decimal as PythonDecimal

# Try to import Decimal from Saleor to avoid duplicate type errors
try:
    from saleor.graphql.core.scalars import Decimal
except ImportError:
    # Fallback to graphene.Decimal if Saleor's Decimal is not available
    Decimal = graphene.Decimal

# Import models
from saleor_extensions.orders.models import OrderBranchAssignment, ManualOrder
from saleor_extensions.inventory.models import BranchInventory, StockMovement
from saleor_extensions.branches.models import Branch
from saleor_extensions.regions.models import Region
from saleor_extensions.currency.models import Currency


# ============================================================================
# Dashboard Data Types
# ============================================================================

class KPIType(graphene.ObjectType):
    """Key Performance Indicator"""
    label = graphene.String()
    value = graphene.String()
    change = graphene.Float(description="Percentage change")
    trend = graphene.String(description="up, down, or stable")
    currency = graphene.String()


class SalesDataPoint(graphene.ObjectType):
    """Sales data point for charts"""
    date = graphene.String()
    value = Decimal()
    orders = graphene.Int()
    currency = graphene.String()


class BranchPerformanceType(graphene.ObjectType):
    """Branch performance metrics"""
    branch_id = graphene.ID()
    branch_name = graphene.String()
    sales = Decimal()
    orders = graphene.Int()
    growth = graphene.Float()
    currency = graphene.String()


class ProductPerformanceType(graphene.ObjectType):
    """Top performing products"""
    product_id = graphene.ID()
    product_name = graphene.String()
    sales = Decimal()
    quantity = graphene.Int()
    currency = graphene.String()


class InventoryStatusType(graphene.ObjectType):
    """Inventory status summary"""
    total_items = graphene.Int()
    low_stock_items = graphene.Int()
    out_of_stock_items = graphene.Int()
    total_value = Decimal()
    currency = graphene.String()


# ============================================================================
# Dashboard Queries
# ============================================================================

class DashboardQueries(graphene.ObjectType):
    """Dashboard-related queries for executive and branch views"""
    
    # Executive Dashboard KPIs
    executive_kpis = graphene.List(
        KPIType,
        region_code=graphene.String(),
        start_date=graphene.String(),
        end_date=graphene.String(),
        description="Get executive dashboard KPIs"
    )
    
    # Branch Dashboard KPIs
    branch_kpis = graphene.List(
        KPIType,
        branch_id=graphene.ID(required=True),
        start_date=graphene.String(),
        end_date=graphene.String(),
        description="Get branch-specific KPIs"
    )
    
    # Sales data for charts
    sales_chart_data = graphene.List(
        SalesDataPoint,
        branch_id=graphene.ID(),
        region_code=graphene.String(),
        period=graphene.String(default_value="30d"),  # 7d, 30d, 90d, 1y
        description="Get sales data for chart visualization"
    )
    
    # Branch performance comparison
    branch_performance = graphene.List(
        BranchPerformanceType,
        region_code=graphene.String(),
        start_date=graphene.String(),
        end_date=graphene.String(),
        description="Get performance metrics for all branches"
    )
    
    # Top products
    top_products = graphene.List(
        ProductPerformanceType,
        branch_id=graphene.ID(),
        region_code=graphene.String(),
        limit=graphene.Int(default_value=10),
        start_date=graphene.String(),
        end_date=graphene.String(),
        description="Get top performing products"
    )
    
    # Inventory status
    inventory_status = graphene.Field(
        InventoryStatusType,
        branch_id=graphene.ID(),
        region_code=graphene.String(),
        description="Get inventory status summary"
    )
    
    # Revenue by region
    revenue_by_region = graphene.List(
        BranchPerformanceType,
        start_date=graphene.String(),
        end_date=graphene.String(),
        description="Get revenue breakdown by region"
    )
    
    def resolve_executive_kpis(self, info, region_code=None, start_date=None, end_date=None):
        """Get executive dashboard KPIs"""
        # Parse dates
        if end_date:
            end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        else:
            end_date_obj = datetime.now()
        
        if start_date:
            start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        else:
            start_date_obj = end_date_obj - timedelta(days=30)
        
        # Previous period for comparison
        period_days = (end_date_obj - start_date_obj).days
        prev_start = start_date_obj - timedelta(days=period_days)
        prev_end = start_date_obj
        
        kpis = []
        
        # Build base queryset
        orders_qs = OrderBranchAssignment.objects.filter(
            created_at__gte=start_date_obj,
            created_at__lte=end_date_obj
        )
        prev_orders_qs = OrderBranchAssignment.objects.filter(
            created_at__gte=prev_start,
            created_at__lte=prev_end
        )
        
        if region_code:
            orders_qs = orders_qs.filter(region__code=region_code)
            prev_orders_qs = prev_orders_qs.filter(region__code=region_code)
        
        # Total Revenue
        try:
            total_revenue = orders_qs.aggregate(
                total=Sum('order__total_gross_amount')
            )['total'] or Decimal('0')
            
            prev_total_revenue = prev_orders_qs.aggregate(
                total=Sum('order__total_gross_amount')
            )['total'] or Decimal('0')
            
            change = 0.0
            if prev_total_revenue > 0:
                change = ((total_revenue - prev_total_revenue) / prev_total_revenue) * 100
            
            kpis.append(KPIType(
                label="Total Revenue",
                value=str(total_revenue),
                change=float(change),
                trend="up" if change > 0 else "down" if change < 0 else "stable",
                currency="GBP"  # Default, should get from orders
            ))
        except Exception as e:
            # Fallback if Saleor Order fields don't exist
            kpis.append(KPIType(
                label="Total Revenue",
                value="0",
                change=0.0,
                trend="stable",
                currency="GBP"
            ))
        
        # Total Orders
        total_orders = orders_qs.count()
        prev_total_orders = prev_orders_qs.count()
        
        change = 0.0
        if prev_total_orders > 0:
            change = ((total_orders - prev_total_orders) / prev_total_orders) * 100
        
        kpis.append(KPIType(
            label="Total Orders",
            value=str(total_orders),
            change=float(change),
            trend="up" if change > 0 else "down" if change < 0 else "stable",
            currency=None
        ))
        
        # Average Order Value
        try:
            avg_order_value = orders_qs.aggregate(
                avg=Avg('order__total_gross_amount')
            )['avg'] or Decimal('0')
            
            prev_avg_order_value = prev_orders_qs.aggregate(
                avg=Avg('order__total_gross_amount')
            )['avg'] or Decimal('0')
            
            change = 0.0
            if prev_avg_order_value > 0:
                change = ((avg_order_value - prev_avg_order_value) / prev_avg_order_value) * 100
            
            kpis.append(KPIType(
                label="Average Order Value",
                value=str(avg_order_value),
                change=float(change),
                trend="up" if change > 0 else "down" if change < 0 else "stable",
                currency="GBP"
            ))
        except Exception:
            kpis.append(KPIType(
                label="Average Order Value",
                value="0",
                change=0.0,
                trend="stable",
                currency="GBP"
            ))
        
        # Active Branches
        active_branches = Branch.objects.filter(is_active=True).count()
        kpis.append(KPIType(
            label="Active Branches",
            value=str(active_branches),
            change=0.0,
            trend="stable",
            currency=None
        ))
        
        return kpis
    
    def resolve_branch_kpis(self, info, branch_id, start_date=None, end_date=None):
        """Get branch-specific KPIs"""
        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return []
        
        # Parse dates
        if end_date:
            end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        else:
            end_date_obj = datetime.now()
        
        if start_date:
            start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        else:
            start_date_obj = end_date_obj - timedelta(days=30)
        
        # Previous period
        period_days = (end_date_obj - start_date_obj).days
        prev_start = start_date_obj - timedelta(days=period_days)
        prev_end = start_date_obj
        
        kpis = []
        
        # Branch orders
        orders_qs = OrderBranchAssignment.objects.filter(
            branch_id=branch_id,
            created_at__gte=start_date_obj,
            created_at__lte=end_date_obj
        )
        prev_orders_qs = OrderBranchAssignment.objects.filter(
            branch_id=branch_id,
            created_at__gte=prev_start,
            created_at__lte=prev_end
        )
        
        # Branch Revenue
        try:
            revenue = orders_qs.aggregate(
                total=Sum('order__total_gross_amount')
            )['total'] or Decimal('0')
            
            prev_revenue = prev_orders_qs.aggregate(
                total=Sum('order__total_gross_amount')
            )['total'] or Decimal('0')
            
            change = 0.0
            if prev_revenue > 0:
                change = ((revenue - prev_revenue) / prev_revenue) * 100
            
            kpis.append(KPIType(
                label="Branch Revenue",
                value=str(revenue),
                change=float(change),
                trend="up" if change > 0 else "down" if change < 0 else "stable",
                currency=branch.region.default_currency
            ))
        except Exception:
            kpis.append(KPIType(
                label="Branch Revenue",
                value="0",
                change=0.0,
                trend="stable",
                currency=branch.region.default_currency
            ))
        
        # Branch Orders
        orders_count = orders_qs.count()
        prev_orders_count = prev_orders_qs.count()
        
        change = 0.0
        if prev_orders_count > 0:
            change = ((orders_count - prev_orders_count) / prev_orders_count) * 100
        
        kpis.append(KPIType(
            label="Orders",
            value=str(orders_count),
            change=float(change),
            trend="up" if change > 0 else "down" if change < 0 else "stable",
            currency=None
        ))
        
        # Inventory Items
        inventory_count = BranchInventory.objects.filter(branch_id=branch_id).count()
        low_stock_count = BranchInventory.objects.filter(
            branch_id=branch_id,
            quantity__lte=F('low_stock_threshold')
        ).count()
        
        kpis.append(KPIType(
            label="Inventory Items",
            value=str(inventory_count),
            change=0.0,
            trend="stable",
            currency=None
        ))
        
        kpis.append(KPIType(
            label="Low Stock Items",
            value=str(low_stock_count),
            change=0.0,
            trend="stable" if low_stock_count == 0 else "down",
            currency=None
        ))
        
        return kpis
    
    def resolve_sales_chart_data(self, info, branch_id=None, region_code=None, period="30d", **kwargs):
        """Get sales data for chart visualization"""
        # Parse period
        period_map = {
            "7d": 7,
            "30d": 30,
            "90d": 90,
            "1y": 365
        }
        days = period_map.get(period, 30)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Build queryset
        orders_qs = OrderBranchAssignment.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        )
        
        if branch_id:
            orders_qs = orders_qs.filter(branch_id=branch_id)
        if region_code:
            orders_qs = orders_qs.filter(region__code=region_code)
        
        # Group by date
        data_points = []
        current_date = start_date.date()
        
        while current_date <= end_date.date():
            day_start = datetime.combine(current_date, datetime.min.time())
            day_end = day_start + timedelta(days=1)
            
            day_orders = orders_qs.filter(
                created_at__gte=day_start,
                created_at__lt=day_end
            )
            
            try:
                day_revenue = day_orders.aggregate(
                    total=Sum('order__total_gross_amount')
                )['total'] or Decimal('0')
            except Exception:
                day_revenue = Decimal('0')
            
            data_points.append(SalesDataPoint(
                date=current_date.isoformat(),
                value=day_revenue,
                orders=day_orders.count(),
                currency="GBP"  # Default
            ))
            
            current_date += timedelta(days=1)
        
        return data_points
    
    def resolve_branch_performance(self, info, region_code=None, start_date=None, end_date=None, **kwargs):
        """Get performance metrics for all branches"""
        # Parse dates
        if end_date:
            end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        else:
            end_date_obj = datetime.now()
        
        if start_date:
            start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        else:
            start_date_obj = end_date_obj - timedelta(days=30)
        
        branches_qs = Branch.objects.filter(is_active=True)
        if region_code:
            branches_qs = branches_qs.filter(region__code=region_code)
        
        performance = []
        
        for branch in branches_qs:
            orders_qs = OrderBranchAssignment.objects.filter(
                branch_id=branch.id,
                created_at__gte=start_date_obj,
                created_at__lte=end_date_obj
            )
            
            try:
                sales = orders_qs.aggregate(
                    total=Sum('order__total_gross_amount')
                )['total'] or Decimal('0')
            except Exception:
                sales = Decimal('0')
            
            orders_count = orders_qs.count()
            
            # Calculate growth (simplified - compare with previous period)
            period_days = (end_date_obj - start_date_obj).days
            prev_start = start_date_obj - timedelta(days=period_days)
            prev_end = start_date_obj
            
            prev_orders_qs = OrderBranchAssignment.objects.filter(
                branch_id=branch.id,
                created_at__gte=prev_start,
                created_at__lte=prev_end
            )
            
            try:
                prev_sales = prev_orders_qs.aggregate(
                    total=Sum('order__total_gross_amount')
                )['total'] or Decimal('0')
            except Exception:
                prev_sales = Decimal('0')
            
            growth = 0.0
            if prev_sales > 0:
                growth = ((sales - prev_sales) / prev_sales) * 100
            
            performance.append(BranchPerformanceType(
                branch_id=str(branch.id),
                branch_name=branch.name,
                sales=sales,
                orders=orders_count,
                growth=float(growth),
                currency=branch.region.default_currency
            ))
        
        return performance
    
    def resolve_top_products(self, info, branch_id=None, region_code=None, limit=10, 
                            start_date=None, end_date=None, **kwargs):
        """Get top performing products"""
        # This would require OrderLineItem data from Saleor
        # For now, return empty list as placeholder
        # In real implementation, would aggregate from order items
        return []
    
    def resolve_inventory_status(self, info, branch_id=None, region_code=None, **kwargs):
        """Get inventory status summary"""
        inventory_qs = BranchInventory.objects.all()
        
        if branch_id:
            inventory_qs = inventory_qs.filter(branch_id=branch_id)
        elif region_code:
            inventory_qs = inventory_qs.filter(branch__region__code=region_code)
        
        total_items = inventory_qs.count()
        low_stock_items = inventory_qs.filter(quantity__lte=F('low_stock_threshold')).count()
        out_of_stock_items = inventory_qs.filter(quantity=0).count()
        
        # Total value would require product prices - placeholder for now
        total_value = Decimal('0')
        
        return InventoryStatusType(
            total_items=total_items,
            low_stock_items=low_stock_items,
            out_of_stock_items=out_of_stock_items,
            total_value=total_value,
            currency="GBP"  # Default
        )
    
    def resolve_revenue_by_region(self, info, start_date=None, end_date=None, **kwargs):
        """Get revenue breakdown by region"""
        # Parse dates
        if end_date:
            end_date_obj = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        else:
            end_date_obj = datetime.now()
        
        if start_date:
            start_date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        else:
            start_date_obj = end_date_obj - timedelta(days=30)
        
        regions = Region.objects.filter(is_active=True)
        revenue_data = []
        
        for region in regions:
            orders_qs = OrderBranchAssignment.objects.filter(
                region_id=region.id,
                created_at__gte=start_date_obj,
                created_at__lte=end_date_obj
            )
            
            try:
                sales = orders_qs.aggregate(
                    total=Sum('order__total_gross_amount')
                )['total'] or Decimal('0')
            except Exception:
                sales = Decimal('0')
            
            orders_count = orders_qs.count()
            
            revenue_data.append(BranchPerformanceType(
                branch_id=str(region.id),
                branch_name=region.name,
                sales=sales,
                orders=orders_count,
                growth=0.0,  # Would calculate if needed
                currency=region.default_currency
            ))
        
        return revenue_data

