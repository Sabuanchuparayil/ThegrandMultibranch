"""
Tax calculation services
"""
from decimal import Decimal
from django.utils import timezone
from saleor_extensions.taxes.models import TaxRule, TaxExemption


class TaxCalculator:
    """Calculate taxes for orders and products"""
    
    @staticmethod
    def get_tax_rate(region, state=None, product_type='ALL'):
        """
        Get tax rate for a region/state and product type
        
        Args:
            region: Region instance
            state: Optional state (for India GST)
            product_type: Product type/category (e.g., 'GOLD', 'DIAMOND', 'ALL')
        
        Returns:
            Decimal tax rate percentage
        """
        now = timezone.now()
        
        from django.db import models
        
        # Build query
        query = TaxRule.objects.filter(
            region=region,
            is_active=True
        ).filter(
            models.Q(applies_to='ALL') | models.Q(applies_to=product_type)
        ).filter(
            models.Q(effective_from__isnull=True) | models.Q(effective_from__lte=now),
            models.Q(effective_until__isnull=True) | models.Q(effective_until__gte=now)
        )
        
        # Add state filter if provided
        if state:
            query = query.filter(
                models.Q(state='') | models.Q(state=state)
            )
        else:
            query = query.filter(state='')
        
        tax_rule = query.first()
        
        if tax_rule:
            return tax_rule.rate
        else:
            # Fallback to region default tax rate
            return region.tax_rate
    
    @staticmethod
    def calculate_tax(amount, region, state=None, product_type='ALL', order_value=None):
        """
        Calculate tax amount for a given amount
        
        Args:
            amount: Decimal amount to calculate tax on
            region: Region instance
            state: Optional state (for India GST)
            product_type: Product type/category
            order_value: Optional order value for exemption checks
        
        Returns:
            Dict with 'tax_rate', 'tax_amount', 'total_amount'
        """
        from django.db import models
        
        # Check for exemptions first
        exemption_amount = Decimal('0')
        if order_value is not None:
            exemptions = TaxExemption.objects.filter(
                region=region,
                is_active=True,
                exemption_type__in=['ORDER_VALUE', 'PRODUCT']
            ).filter(
                models.Q(valid_from__isnull=True) | models.Q(valid_from__lte=timezone.now()),
                models.Q(valid_until__isnull=True) | models.Q(valid_until__gte=timezone.now())
            )
            
            for exemption in exemptions:
                if exemption.exemption_type == 'ORDER_VALUE':
                    if exemption.min_order_value and order_value >= exemption.min_order_value:
                        exemption_amount = (amount * exemption.exemption_percentage) / Decimal('100')
                        break
                elif exemption.exemption_type == 'PRODUCT':
                    if exemption.identifier == product_type or exemption.identifier == 'ALL':
                        exemption_amount = (amount * exemption.exemption_percentage) / Decimal('100')
                        break
        
        # Get tax rate
        tax_rate = TaxCalculator.get_tax_rate(region, state, product_type)
        
        # Calculate tax on amount after exemption
        taxable_amount = amount - exemption_amount
        tax_amount = (taxable_amount * tax_rate) / Decimal('100')
        total_amount = amount + tax_amount
        
        return {
            'tax_rate': tax_rate,
            'tax_amount': tax_amount,
            'exemption_amount': exemption_amount,
            'taxable_amount': taxable_amount,
            'total_amount': total_amount,
        }
    
    @staticmethod
    def is_exempt(region, product_id=None, customer_id=None, order_value=None):
        """
        Check if a product/customer/order is tax exempt
        
        Returns:
            Tuple (is_exempt: bool, exemption_percentage: Decimal)
        """
        from django.db import models
        
        exemptions = TaxExemption.objects.filter(
            region=region,
            is_active=True
        ).filter(
            models.Q(valid_from__isnull=True) | models.Q(valid_from__lte=timezone.now()),
            models.Q(valid_until__isnull=True) | models.Q(valid_until__gte=timezone.now())
        )
        
        for exemption in exemptions:
            if exemption.exemption_type == 'PRODUCT' and product_id:
                if exemption.identifier == product_id or exemption.identifier == 'ALL':
                    return True, exemption.exemption_percentage
            elif exemption.exemption_type == 'CUSTOMER' and customer_id:
                if exemption.identifier == customer_id:
                    return True, exemption.exemption_percentage
            elif exemption.exemption_type == 'ORDER_VALUE' and order_value:
                if exemption.min_order_value and order_value >= exemption.min_order_value:
                    return True, exemption.exemption_percentage
        
        return False, Decimal('0')

