"""
Splitroute Payment Service for Nano cryptocurrency payments
Production-level implementation with webhook verification
"""

import os
import requests
import hmac
import hashlib
import json
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class SplitRouteService:
    """Service for handling Splitroute Nano payments"""
    
    def __init__(self):
        self.api_key = os.getenv('SPLITROUTE_API_KEY')
        if not self.api_key:
            raise Exception("SPLITROUTE_API_KEY not configured")
        
        self.base_url = "https://api.splitroute.com"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Minimum payment: 1 XNO = 100 credits
        self.min_payment_nano = 1.0
        self.credits_per_nano = 100
    
    def create_invoice(
        self,
        user_id: str,
        amount_nano: float,
        webhook_url: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        description: str = "NanoTik Video Credits"
    ) -> Dict[str, Any]:
        """
        Create a Splitroute invoice for Nano payment
        
        Args:
            user_id: User ID for tracking
            amount_nano: Amount in Nano (minimum 1.0)
            webhook_url: URL to receive payment notifications
            webhook_secret: Secret for webhook verification
            description: Invoice description
        
        Returns:
            Invoice data with payment address and details
        """
        if amount_nano < self.min_payment_nano:
            raise ValueError(f"Minimum payment is {self.min_payment_nano} XNO")
        
        # Calculate credits
        credits = int(amount_nano * self.credits_per_nano)
        
        # Prepare invoice data
        invoice_data = {
            "currency": "XNO",
            "description": f"{description} - {credits} credits",
            "metadata": {
                "user_id": user_id,
                "credits": credits,
                "platform": "nanotik"
            }
        }
        
        # Add webhook if provided
        if webhook_url and webhook_secret:
            invoice_data["webhook_url"] = webhook_url
            invoice_data["webhook_secret"] = webhook_secret
        
        try:
            response = requests.post(
                f"{self.base_url}/invoices",
                headers=self.headers,
                json=invoice_data,
                timeout=10
            )
            response.raise_for_status()
            
            invoice = response.json()
            
            return {
                'invoice_id': invoice.get('id'),
                'payment_address': invoice.get('account'),
                'amount_nano': amount_nano,
                'credits': credits,
                'status': 'created',
                'expires_at': invoice.get('expires_at'),
                'qr_code': invoice.get('qr_code'),
                'invoice_url': invoice.get('url')
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create Splitroute invoice: {str(e)}")
    
    def check_invoice_status(self, invoice_id: str) -> Dict[str, Any]:
        """
        Check the status of a Splitroute invoice
        
        Args:
            invoice_id: The invoice ID to check
        
        Returns:
            Invoice status data
        """
        try:
            response = requests.get(
                f"{self.base_url}/invoices/{invoice_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            
            invoice = response.json()
            
            return {
                'invoice_id': invoice.get('id'),
                'is_paid': invoice.get('is_paid', False),
                'is_pending': invoice.get('is_pending', False),
                'is_expired': invoice.get('is_expired', False),
                'is_done': invoice.get('is_done', False),
                'amount_received': invoice.get('amount_received'),
                'metadata': invoice.get('metadata', {})
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to check invoice status: {str(e)}")
    
    def verify_webhook_signature(
        self,
        webhook_secret: str,
        signature: str,
        timestamp: str,
        payload: str
    ) -> bool:
        """
        Verify webhook signature from Splitroute
        
        Args:
            webhook_secret: The webhook secret used when creating invoice
            signature: Signature from X-Webhook-Signature header
            timestamp: Timestamp from X-Webhook-Timestamp header
            payload: Raw request body
        
        Returns:
            True if signature is valid, False otherwise
        """
        # Create the expected signature
        message = timestamp + payload
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures securely
        return hmac.compare_digest(expected_signature, signature)
    
    def calculate_credits_for_nano(self, amount_nano: float) -> int:
        """Calculate how many credits for a given Nano amount"""
        return int(amount_nano * self.credits_per_nano)
    
    def calculate_nano_for_credits(self, credits: int) -> float:
        """Calculate Nano amount needed for credits"""
        nano_amount = credits / self.credits_per_nano
        return max(nano_amount, self.min_payment_nano)


# Singleton instance
_splitroute_service = None

def get_splitroute_service() -> SplitRouteService:
    """Get or create SplitRoute service instance"""
    global _splitroute_service
    if _splitroute_service is None:
        _splitroute_service = SplitRouteService()
    return _splitroute_service
