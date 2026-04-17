"""
Authentication utilities for Kraken exchange API

This module provides functions for generating authentication signatures
and headers required for Kraken's private API endpoints.
"""

import base64
import hashlib
import hmac
import urllib.parse
from typing import Dict, Any


def get_kraken_signature(urlpath: str, data: Dict[str, Any], secret: str) -> str:
    """
    Generate a Kraken API signature.

    This creates the cryptographic signature required to authenticate
    private API requests to Kraken.

    Args:
        urlpath (str): The API endpoint path (e.g., "/0/private/Balance")
        data (Dict[str, Any]): The API request parameters (must include nonce)
        secret (str): The API secret key (base64 encoded)

    Returns:
        str: The generated signature (base64 encoded)

    Example:
        >>> signature = get_kraken_signature(
        ...     "/0/private/Balance",
        ...     {"nonce": 1234567890},
        ...     "your_secret_key"
        ... )
    """
    # Convert data to URL encoded string
    postdata = urllib.parse.urlencode(data)

    # Create the message: nonce + postdata, then hash with sha256
    encoded = (str(data["nonce"]) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    # Decode the secret (it's base64 encoded)
    secret_decoded = base64.b64decode(secret)

    # Generate the signature using HMAC-SHA512
    mac = hmac.new(secret_decoded, message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())

    return sigdigest.decode()


def create_auth_headers(
    api_key: str, api_secret: str, urlpath: str, data: Dict[str, Any]
) -> Dict[str, str]:
    """
    Create authentication headers for Kraken API requests.

    Args:
        api_key (str): The API key
        api_secret (str): The API secret
        urlpath (str): The API endpoint path
        data (Dict[str, Any]): The request data (must include nonce)

    Returns:
        Dict[str, str]: Authentication headers for the request

    Example:
        >>> headers = create_auth_headers(
        ...     "your_api_key",
        ...     "your_api_secret",
        ...     "/0/private/Balance",
        ...     {"nonce": 1234567890}
        ... )
    """
    signature = get_kraken_signature(urlpath, data, api_secret)

    return {
        "API-Key": api_key,
        "API-Sign": signature,
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
    }
