"""
Pricing calculation services for jewellery products
"""
from decimal import Decimal
from django.utils import timezone
from saleor_extensions.pricing.models import (
    GoldRate, MakingChargeRule, BranchPricingOverride, PricingOverride
)


class PricingCalculator:
    """Calculate prices for jewellery products"""
    
    @staticmethod
    def get_gold_rate(region, date=None):
        """Get the latest gold rate for a region"""
        if date is None:
            date = timezone.now()
        
        try:
            gold_rate = GoldRate.objects.filter(
                region=region,
                effective_date__lte=date
            ).order_by('-effective_date').first()
            return gold_rate
        except GoldRate.DoesNotExist:
            return None
    
    @staticmethod
    def calculate_making_charge(region, gold_value, weight_grams=None):
        """
        Calculate making charge based on region rules
        
        Args:
            region: Region instance
            gold_value: Decimal value of gold
            weight_grams: Optional weight in grams for weight-based rules
        
        Returns:
            Decimal making charge amount
        """
        rules = MakingChargeRule.objects.filter(
            region=region,
            is_active=True
        ).order_by('priority')
        
        # Apply weight constraints if provided
        if weight_grams is not None:
            from django.db import models as db_models
            rules = rules.filter(
                db_models.Q(min_weight_grams__isnull=True) | db_models.Q(min_weight_grams__lte=weight_grams),
                db_models.Q(max_weight_grams__isnull=True) | db_models.Q(max_weight_grams__gte=weight_grams)
            )
        
        if not rules.exists():
            return Decimal('0')
        
        rule = rules.first()
        
        if rule.charge_type == 'PERCENTAGE':
            return (gold_value * rule.value) / Decimal('100')
        elif rule.charge_type == 'FIXED_PER_GRAM':
            if weight_grams:
                return rule.value * weight_grams
            return rule.value
        elif rule.charge_type == 'FIXED_TOTAL':
            return rule.value
        
        return Decimal('0')
    
    @staticmethod
    def get_product_price(product_id, branch=None, region=None):
        """
        Get price for a product, considering branch and region overrides
        
        Args:
            product_id: Product ID
            branch: Optional Branch instance
            region: Optional Region instance (required if branch not provided)
        
        Returns:
            Dict with 'price', 'currency', 'making_charge' if applicable
        """
        # Priority: Branch override > Default pricing
        if branch:
            try:
                override = BranchPricingOverride.objects.get(
                    branch=branch,
                    product_id=product_id,
                    is_active=True
                )
                # Check validity dates
                now = timezone.now()
                if override.valid_from and override.valid_from > now:
                    pass  # Not yet valid
                elif override.valid_until and override.valid_until < now:
                    pass  # Expired
                else:
                    return {
                        'price': override.override_price,
                        'currency': override.currency.code,
                        'making_charge': override.override_making_charge,
                    }
            except BranchPricingOverride.DoesNotExist:
                pass
        
        return None
    
    @staticmethod
    def calculate_total_price(gold_rate_per_gram, weight_grams, making_charge_percentage=None):
        """
        Calculate total price for gold jewellery
        
        Args:
            gold_rate_per_gram: Gold rate per gram
            weight_grams: Weight in grams
            making_charge_percentage: Optional making charge percentage
            region: Optional Region for making charge calculation
        
        Returns:
            Dict with 'gold_value', 'making_charge', 'total_price'
        """
        gold_value = gold_rate_per_gram * Decimal(str(weight_grams))
        
        if making_charge_percentage:
            making_charge = (gold_value * Decimal(str(making_charge_percentage))) / Decimal('100')
        elif region:
            making_charge = PricingCalculator.calculate_making_charge(
                region, gold_value, weight_grams
            )
        else:
            making_charge = Decimal('0')
        
        total_price = gold_value + making_charge
        
        return {
            'gold_value': gold_value,
            'making_charge': making_charge,
            'total_price': total_price,
        }

