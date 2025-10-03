"""
Google OAuth Authentication Service
"""

import os
import streamlit as st
from streamlit_oauth import OAuth2Component
import requests
from typing import Dict, Any, Optional


class AuthService:
    """Google OAuth authentication handler"""
    
    def __init__(self):
        self.client_id = os.getenv('GOOGLE_CLIENT_ID')
        self.client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        
        if not self.client_id or not self.client_secret:
            raise Exception("Google OAuth credentials not configured in secrets")
        
        # OAuth endpoints
        self.authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
        self.token_url = "https://oauth2.googleapis.com/token"
        self.userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    
    def get_oauth_component(self, redirect_uri: str) -> OAuth2Component:
        """Create OAuth2 component for Google"""
        return OAuth2Component(
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorize_endpoint=self.authorize_url,
            token_endpoint=self.token_url,
            refresh_token_endpoint=self.token_url,
            revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
        )
    
    def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """Get user information from Google"""
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(self.userinfo_url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def login(self, redirect_uri: str) -> Optional[Dict[str, Any]]:
        """Handle Google login flow"""
        oauth_component = self.get_oauth_component(redirect_uri)
        
        # Authorize and get token
        result = oauth_component.authorize_button(
            name="Login with Google",
            icon="https://www.google.com/favicon.ico",
            redirect_uri=redirect_uri,
            scope="openid email profile",
            key="google_oauth",
            pkce='S256',
        )
        
        if result and 'token' in result:
            # Get user info
            user_info = self.get_user_info(result['token']['access_token'])
            
            # Clear anonymous user_id to trigger migration
            if 'user_id' in st.session_state:
                del st.session_state['user_id']
            if 'credits' in st.session_state:
                del st.session_state['credits']
            
            # Store in session
            st.session_state.authenticated = True
            st.session_state.user_email = user_info.get('email')
            st.session_state.user_name = user_info.get('name')
            st.session_state.user_picture = user_info.get('picture')
            st.session_state.google_id = user_info.get('id')
            st.session_state.access_token = result['token']['access_token']
            
            return user_info
        
        return None
    
    def logout(self):
        """Logout user and clear session"""
        keys_to_clear = [
            'authenticated', 'user_email', 'user_name', 'user_picture',
            'google_id', 'access_token', 'user_id', 'credits'
        ]
        
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)


# Singleton instance
_auth_service = None

def get_auth_service() -> AuthService:
    """Get auth service singleton"""
    global _auth_service
    if _auth_service is None:
        _auth_service = AuthService()
    return _auth_service
