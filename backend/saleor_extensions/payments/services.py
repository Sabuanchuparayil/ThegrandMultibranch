"""
Payment gateway integration services
"""
from decimal import Decimal
from typing import Dict, Optional
from saleor_extensions.payments.models import PaymentGateway, PaymentTransaction


class PaymentGatewayInterface:
    """Base interface for payment gateway integrations"""
    
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway
    
    def create_payment(self, amount: Decimal, currency: str, order_id: str, **kwargs) -> Dict:
        """Create a payment transaction"""
        raise NotImplementedError
    
    def verify_payment(self, transaction_id: str) -> Dict:
        """Verify payment status"""
        raise NotImplementedError
    
    def process_refund(self, transaction_id: str, amount: Decimal, reason: str = "") -> Dict:
        """Process refund"""
        raise NotImplementedError
    
    def get_payment_status(self, transaction_id: str) -> Dict:
        """Get payment status"""
        raise NotImplementedError


class StripeGateway(PaymentGatewayInterface):
    """Stripe payment gateway implementation"""
    
    def create_payment(self, amount: Decimal, currency: str, order_id: str, **kwargs) -> Dict:
        """Create Stripe payment intent"""
        # Implementation will use Stripe SDK
        # import stripe
        # stripe.api_key = self.gateway.api_key
        # intent = stripe.PaymentIntent.create(...)
        return {
            'transaction_id': '',
            'client_secret': '',
            'status': 'pending',
        }
    
    def verify_payment(self, transaction_id: str) -> Dict:
        """Verify Stripe payment"""
        return {'status': 'success'}
    
    def process_refund(self, transaction_id: str, amount: Decimal, reason: str = "") -> Dict:
        """Process Stripe refund"""
        return {'refund_id': '', 'status': 'success'}
    
    def get_payment_status(self, transaction_id: str) -> Dict:
        """Get Stripe payment status"""
        return {'status': 'success'}


class RazorpayGateway(PaymentGatewayInterface):
    """Razorpay payment gateway implementation"""
    
    def create_payment(self, amount: Decimal, currency: str, order_id: str, **kwargs) -> Dict:
        """Create Razorpay order"""
        # Implementation will use Razorpay SDK
        return {
            'transaction_id': '',
            'order_id': '',
            'status': 'created',
        }
    
    def verify_payment(self, transaction_id: str) -> Dict:
        """Verify Razorpay payment"""
        return {'status': 'success'}
    
    def process_refund(self, transaction_id: str, amount: Decimal, reason: str = "") -> Dict:
        """Process Razorpay refund"""
        return {'refund_id': '', 'status': 'success'}
    
    def get_payment_status(self, transaction_id: str) -> Dict:
        """Get Razorpay payment status"""
        return {'status': 'success'}


class PayTabsGateway(PaymentGatewayInterface):
    """PayTabs payment gateway implementation (UAE)"""
    
    def create_payment(self, amount: Decimal, currency: str, order_id: str, **kwargs) -> Dict:
        """Create PayTabs payment"""
        return {
            'transaction_id': '',
            'payment_url': '',
            'status': 'pending',
        }
    
    def verify_payment(self, transaction_id: str) -> Dict:
        """Verify PayTabs payment"""
        return {'status': 'success'}
    
    def process_refund(self, transaction_id: str, amount: Decimal, reason: str = "") -> Dict:
        """Process PayTabs refund"""
        return {'refund_id': '', 'status': 'success'}
    
    def get_payment_status(self, transaction_id: str) -> Dict:
        """Get PayTabs payment status"""
        return {'status': 'success'}


class PaymentGatewayFactory:
    """Factory for creating payment gateway instances"""
    
    GATEWAY_CLASSES = {
        'STRIPE': StripeGateway,
        'RAZORPAY': RazorpayGateway,
        'PAYTABS': PayTabsGateway,
        # Add more gateways as needed
    }
    
    @classmethod
    def get_gateway(cls, gateway: PaymentGateway) -> PaymentGatewayInterface:
        """Get payment gateway instance"""
        gateway_class = cls.GATEWAY_CLASSES.get(gateway.gateway_type)
        if not gateway_class:
            raise ValueError(f"Unsupported gateway type: {gateway.gateway_type}")
        return gateway_class(gateway)
    
    @classmethod
    def get_gateway_for_region(cls, region_code: str, currency_code: str) -> Optional[PaymentGateway]:
        """Get active payment gateway for region and currency"""
        from saleor_extensions.payments.models import PaymentGateway
        from saleor_extensions.currency.models import Currency
        
        try:
            currency = Currency.objects.get(code=currency_code, is_active=True)
            gateway = PaymentGateway.objects.filter(
                region__code=region_code,
                is_active=True,
                supported_currencies=currency
            ).first()
            return gateway
        except Currency.DoesNotExist:
            return None

