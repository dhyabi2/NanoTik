"""
Payment Service for Nano cryptocurrency transactions
Integrates with Splitroute for payment processing
"""

import os
import requests
import qrcode
import io
import base64
from typing import Dict, Any
from datetime import datetime
from decimal import Decimal


class PaymentService:
    """Service for handling Nano cryptocurrency payments via Splitroute"""

    def __init__(self):
        # Use the provided Splitroute API key
        self.splitroute_api_key = "SR_SECRET_a9a981a4a6173ad7da9fa7d557e37de6"

        self.base_url = "https://api.splitroute.com/api/v1"
        self.headers = {
            'X-API-Key': self.splitroute_api_key,
            'Content-Type': 'application/json'
        }

        # Video payment: 0.01 XNO per video
        self.video_payment_nano = 0.01
        # Destination Nano address - app wallet
        self.destination_address = os.getenv('NANO_DESTINATION_ADDRESS', 'nano_3qya5xpjfsbk3ndfebo9dsrj6iy6f6idmogqtn1mtzdtwnxu6rw3dz18i6xf')
    
    def create_video_payment_invoice(self, user_id: str = None) -> Dict[str, Any]:
        """
        Create a Splitroute payment invoice for video generation (0.01 XNO)

        Args:
            user_id: User ID for transaction tracking (optional)

        Returns:
            Payment request details including QR code and payment address
        """
        try:
            # Create Splitroute invoice for 0.01 XNO
            amount_decimal = Decimal(str(self.video_payment_nano))
            # Convert XNO to raw units (1 XNO = 10^30 raw)
            amount_raw = int(amount_decimal * Decimal(10 ** 30))

            invoice_data = {
                "nominal_amount": self.video_payment_nano,
                "nominal_currency": "XNO",
                "destinations": [
                    {
                        "account": self.destination_address,
                        "primary": True
                    }
                ]
            }

            response = requests.post(
                f"{self.base_url}/invoices",
                headers=self.headers,
                json=invoice_data,
                timeout=10
            )
            response.raise_for_status()

            invoice = response.json()

            # Get invoice ID from response
            invoice_id = (invoice.get('invoice_id') or
                         invoice.get('uuid') or
                         invoice.get('id') or
                         invoice.get('reference'))

            if not invoice_id:
                # If still no ID, return error with response details
                return {
                    'success': False,
                    'error': f'No invoice ID in response. Fields: {list(invoice.keys())}'
                }

            # Use Splitroute's temporary account for payment tracking
            # Users pay to this address, Splitroute tracks it and forwards to your wallet
            splitroute_account = invoice.get('account_address') or invoice.get('account')

            if not splitroute_account:
                return {
                    'success': False,
                    'error': f'No payment account in response. Fields: {list(invoice.keys())}'
                }

            # Generate QR code pointing to SPLITROUTE's temporary address
            # They track the payment and forward it to your destination address
            payment_string = f"nano:{splitroute_account}?amount={amount_raw}"
            qr_code_base64 = self._generate_qr_code(payment_string)

            # Save to database
            if user_id and invoice_id:
                from app.database import get_database
                db = get_database()

                # Save Splitroute invoice record
                db.create_splitroute_invoice({
                    'user_id': user_id,
                    'invoice_id': invoice_id,
                    'amount_nano': self.video_payment_nano,
                    'amount_usd': 0,
                    'credits': 0,  # For video payment, not credit purchase
                    'payment_address': splitroute_account,
                    'status': 'created',
                    'expires_at': invoice.get('expires_at')
                })

            return {
                'success': True,
                'invoice_id': invoice_id,
                'amount': self.video_payment_nano,
                'amount_raw': amount_raw,
                'currency': 'XNO',
                'payment_address': splitroute_account,  # Splitroute tracking address
                'destination_address': self.destination_address,  # Your final wallet
                'qr_code': qr_code_base64,
                'payment_string': payment_string,
                'created_at': datetime.utcnow().isoformat(),
                'status': 'pending',
                'expires_at': invoice.get('expires_at'),
                'user_id': user_id
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _generate_qr_code(self, data: str) -> str:
        """
        Generate QR code and return as base64 encoded image

        Args:
            data: Data to encode in QR code

        Returns:
            Base64 encoded PNG image
        """
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode()

        return f"data:image/png;base64,{img_base64}"

    def create_payment_request(self, amount: float, credits: int, user_id: str = None) -> Dict[str, Any]:
        """
        Create a Splitroute payment invoice for credit purchase

        Args:
            amount: Amount in NANO
            credits: Number of credits to purchase
            user_id: User ID for transaction tracking (optional)

        Returns:
            Payment request details including QR code and payment address
        """
        try:
            # Create Splitroute invoice
            invoice_data = {
                "nominal_amount": amount,
                "nominal_currency": "XNO",
                "destinations": [
                    {
                        "account": self.destination_address,
                        "primary": True
                    }
                ]
            }

            response = requests.post(
                f"{self.base_url}/invoices",
                headers=self.headers,
                json=invoice_data,
                timeout=10
            )
            response.raise_for_status()

            invoice = response.json()

            # Get invoice ID from response
            invoice_id = (invoice.get('invoice_id') or
                         invoice.get('uuid') or
                         invoice.get('id') or
                         invoice.get('reference'))

            if not invoice_id:
                return {
                    'success': False,
                    'error': f'No invoice ID in response. Fields: {list(invoice.keys())}'
                }

            splitroute_account = invoice.get('account_address') or invoice.get('account')

            # Convert XNO to raw units for QR code
            amount_decimal = Decimal(str(amount))
            amount_raw = int(amount_decimal * Decimal(10 ** 30))

            # Generate QR code pointing to SPLITROUTE's temporary address
            payment_string = f"nano:{splitroute_account}?amount={amount_raw}"
            qr_code_base64 = self._generate_qr_code(payment_string)

            # Save to database
            if user_id and invoice_id:
                from app.database import get_database
                db = get_database()

                # Save Splitroute invoice record
                db.create_splitroute_invoice({
                    'user_id': user_id,
                    'invoice_id': invoice_id,
                    'amount_nano': amount,
                    'amount_usd': 0,  # Calculate if needed
                    'credits': credits,
                    'payment_address': splitroute_account,
                    'status': 'created',
                    'expires_at': invoice.get('expires_at')
                })

            return {
                'success': True,
                'payment_id': invoice_id,
                'invoice_id': invoice_id,
                'amount': amount,
                'amount_raw': amount_raw,
                'credits': credits,
                'currency': 'XNO',
                'payment_address': splitroute_account,  # Splitroute tracking address
                'destination_address': self.destination_address,  # Your final wallet
                'qr_code': qr_code_base64,
                'payment_string': payment_string,
                'created_at': datetime.utcnow().isoformat(),
                'status': 'pending',
                'expires_at': invoice.get('expires_at'),
                'user_id': user_id
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_payment(self, invoice_id: str) -> Dict[str, Any]:
        """
        Check Splitroute invoice status and credit user if paid

        Args:
            invoice_id: The Splitroute invoice ID

        Returns:
            Payment verification status
        """
        try:
            # Check invoice status from Splitroute
            response = requests.get(
                f"{self.base_url}/invoices/{invoice_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()

            invoice = response.json()

            # Check invoice payment status using boolean fields
            is_paid = invoice.get('is_paid', False) or invoice.get('is_done', False)
            is_expired = invoice.get('is_expired', False)

            # Update database and credit user if paid
            if is_paid:
                from app.database import get_database
                db = get_database()

                # Get invoice record
                invoice_record = db.get_splitroute_invoice_by_id(invoice_id)
                if invoice_record and not invoice_record.get('is_paid'):
                    # Credit the user if this was a credit purchase
                    user_id = invoice_record['user_id']
                    credits = invoice_record.get('credits', 0)

                    if credits > 0:
                        new_balance = db.add_credits(user_id, credits)
                    else:
                        new_balance = None

                    db.update_splitroute_invoice_status(invoice_id, 'paid', is_paid=True)

                    return {
                        'success': True,
                        'invoice_id': invoice_id,
                        'status': 'paid',
                        'credits_added': credits,
                        'new_balance': new_balance,
                        'verified_at': datetime.utcnow().isoformat()
                    }

            status = 'expired' if is_expired else 'pending'
            return {
                'success': True,
                'invoice_id': invoice_id,
                'status': status,
                'is_paid': is_paid,
                'is_expired': is_expired
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_payment_status(self, invoice_id: str) -> str:
        """
        Get current status of a Splitroute invoice

        Returns: 'pending', 'paid', 'expired'
        """
        try:
            response = requests.get(
                f"{self.base_url}/invoices/{invoice_id}",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()

            invoice = response.json()

            if invoice.get('is_paid') or invoice.get('is_done'):
                return 'paid'
            elif invoice.get('is_expired'):
                return 'expired'
            else:
                return 'pending'

        except:
            return 'unknown'
    
    def get_transaction_history(self, user_id: str) -> list:
        """
        Get payment transaction history for a user
        
        Args:
            user_id: User identifier
        
        Returns:
            List of transaction records
        """
        # In real implementation, fetch from database
        return []
