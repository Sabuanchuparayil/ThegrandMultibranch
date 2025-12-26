"""
Currency conversion services
"""
from decimal import Decimal
from django.utils import timezone
from saleor_extensions.currency.models import Currency, ExchangeRate


class CurrencyConverter:
    """Handle currency conversion operations"""
    
    @staticmethod
    def get_exchange_rate(from_currency_code, to_currency_code, date=None):
        """
        Get exchange rate between two currencies
        
        Args:
            from_currency_code: Source currency code (e.g., 'GBP')
            to_currency_code: Target currency code (e.g., 'AED')
            date: Optional date for historical rates (defaults to now)
        
        Returns:
            Decimal exchange rate or None
        """
        if date is None:
            date = timezone.now()
        
        if from_currency_code == to_currency_code:
            return Decimal('1.0')
        
        try:
            from_currency = Currency.objects.get(code=from_currency_code, is_active=True)
            to_currency = Currency.objects.get(code=to_currency_code, is_active=True)
            
            exchange_rate = ExchangeRate.objects.filter(
                from_currency=from_currency,
                to_currency=to_currency,
                effective_date__lte=date
            ).order_by('-effective_date').first()
            
            if exchange_rate:
                return exchange_rate.rate
            
            # Try reverse rate
            reverse_rate = ExchangeRate.objects.filter(
                from_currency=to_currency,
                to_currency=from_currency,
                effective_date__lte=date
            ).order_by('-effective_date').first()
            
            if reverse_rate:
                return Decimal('1') / reverse_rate.rate
            
        except Currency.DoesNotExist:
            pass
        
        return None
    
    @staticmethod
    def convert_amount(amount, from_currency_code, to_currency_code, date=None):
        """
        Convert amount from one currency to another
        
        Args:
            amount: Decimal amount to convert
            from_currency_code: Source currency code
            to_currency_code: Target currency code
            date: Optional date for historical conversion
        
        Returns:
            Decimal converted amount or None
        """
        if from_currency_code == to_currency_code:
            return amount
        
        rate = CurrencyConverter.get_exchange_rate(
            from_currency_code,
            to_currency_code,
            date
        )
        
        if rate is None:
            return None
        
        return amount * rate
    
    @staticmethod
    def format_currency(amount, currency_code):
        """
        Format amount as currency string
        
        Args:
            amount: Decimal amount
            currency_code: Currency code
        
        Returns:
            Formatted string (e.g., "£100.00" or "AED 367.50")
        """
        try:
            currency = Currency.objects.get(code=currency_code, is_active=True)
            symbol = currency.symbol
            
            # Format with symbol based on currency
            if currency_code == 'GBP':
                return f"£{amount:,.2f}"
            elif currency_code == 'AED':
                return f"AED {amount:,.2f}"
            elif currency_code == 'INR':
                return f"₹{amount:,.2f}"
            else:
                return f"{symbol} {amount:,.2f}"
        except Currency.DoesNotExist:
            return f"{amount:,.2f}"


