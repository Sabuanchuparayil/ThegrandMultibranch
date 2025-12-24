"""
Integration services for external systems
"""
import requests
import json
from typing import Dict, Optional
from django.utils import timezone
from saleor_extensions.integrations.models import IntegrationConfig, APILog


class LogisticsIntegration:
    """Base class for logistics/courier integrations"""
    
    def __init__(self, integration: IntegrationConfig):
        self.integration = integration
    
    def create_shipment(self, order_data: Dict) -> Dict:
        """Create shipment with courier"""
        raise NotImplementedError
    
    def track_shipment(self, tracking_number: str) -> Dict:
        """Track shipment"""
        raise NotImplementedError
    
    def cancel_shipment(self, tracking_number: str) -> Dict:
        """Cancel shipment"""
        raise NotImplementedError


class ShiprocketIntegration(LogisticsIntegration):
    """Shiprocket integration (India)"""
    
    def create_shipment(self, order_data: Dict) -> Dict:
        """Create Shiprocket shipment"""
        # Implementation will use Shiprocket API
        return {
            'shipment_id': '',
            'tracking_number': '',
            'awb_code': '',
            'status': 'created',
        }
    
    def track_shipment(self, tracking_number: str) -> Dict:
        """Track Shiprocket shipment"""
        return {'status': 'in_transit', 'updates': []}
    
    def cancel_shipment(self, tracking_number: str) -> Dict:
        """Cancel Shiprocket shipment"""
        return {'status': 'cancelled'}


class RoyalMailIntegration(LogisticsIntegration):
    """Royal Mail integration (UK)"""
    
    def create_shipment(self, order_data: Dict) -> Dict:
        """Create Royal Mail shipment"""
        return {
            'shipment_id': '',
            'tracking_number': '',
            'status': 'created',
        }
    
    def track_shipment(self, tracking_number: str) -> Dict:
        """Track Royal Mail shipment"""
        return {'status': 'in_transit', 'updates': []}
    
    def cancel_shipment(self, tracking_number: str) -> Dict:
        """Cancel Royal Mail shipment"""
        return {'status': 'cancelled'}


class AramexIntegration(LogisticsIntegration):
    """Aramex integration (UAE)"""
    
    def create_shipment(self, order_data: Dict) -> Dict:
        """Create Aramex shipment"""
        return {
            'shipment_id': '',
            'tracking_number': '',
            'status': 'created',
        }
    
    def track_shipment(self, tracking_number: str) -> Dict:
        """Track Aramex shipment"""
        return {'status': 'in_transit', 'updates': []}
    
    def cancel_shipment(self, tracking_number: str) -> Dict:
        """Cancel Aramex shipment"""
        return {'status': 'cancelled'}


class IntegrationService:
    """Service for managing API calls to integrations"""
    
    @staticmethod
    def make_api_request(
        integration: IntegrationConfig,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict:
        """Make API request and log it"""
        import time
        
        start_time = time.time()
        
        # Prepare headers
        request_headers = headers or {}
        if integration.api_key:
            request_headers['Authorization'] = f'Bearer {integration.api_key}'
        
        # Prepare URL
        url = f"{integration.api_endpoint.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=request_headers, params=data)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=request_headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=request_headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=request_headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Log API call
            APILog.objects.create(
                integration=integration,
                request_method=method.upper(),
                endpoint=endpoint,
                request_data=data or {},
                response_status=response.status_code,
                response_data=response.json() if response.content else {},
                duration_ms=duration_ms,
                is_success=response.status_code < 400,
                error_message='' if response.status_code < 400 else response.text
            )
            
            response.raise_for_status()
            return {
                'success': True,
                'status_code': response.status_code,
                'data': response.json() if response.content else {}
            }
            
        except requests.RequestException as e:
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Log failed API call
            APILog.objects.create(
                integration=integration,
                request_method=method.upper(),
                endpoint=endpoint,
                request_data=data or {},
                response_status=getattr(e.response, 'status_code', None),
                response_data={},
                duration_ms=duration_ms,
                is_success=False,
                error_message=str(e)
            )
            
            return {
                'success': False,
                'error': str(e)
            }

