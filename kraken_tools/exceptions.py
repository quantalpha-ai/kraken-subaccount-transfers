"""
Custom exceptions for Kraken API operations

This module defines exception classes for handling various error conditions
when interacting with the Kraken exchange API.
"""


class KrakenAPIError(Exception):
    """Base exception for Kraken API errors"""

    pass


class AuthenticationError(KrakenAPIError):
    """Authentication failed - invalid API key or signature"""

    pass


class RateLimitError(KrakenAPIError):
    """Rate limit exceeded - too many requests"""

    pass


class TransferError(KrakenAPIError):
    """Transfer operation failed"""

    pass


class InsufficientBalanceError(TransferError):
    """Insufficient balance for requested transfer"""

    pass
