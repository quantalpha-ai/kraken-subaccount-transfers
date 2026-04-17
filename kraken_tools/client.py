"""
Kraken API Client for Subaccount Transfers

This module provides a simplified Kraken API client focused solely on:
- Checking account balances
- Transferring assets between master and subaccounts

Security Note:
This code interacts with real financial accounts. Review all operations carefully
before execution. All transfers require a master account API key with Withdraw permission.
"""

import time
import logging
from typing import Dict, Optional, Any

import requests

from .auth import create_auth_headers
from .exceptions import (
    KrakenAPIError,
    AuthenticationError,
    RateLimitError,
    TransferError,
)

logger = logging.getLogger(__name__)


class KrakenClient:
    """
    Kraken API client for account management and transfers.

    This client provides simplified access to Kraken's private API endpoints
    for checking balances and transferring assets between master and subaccounts.

    Security Notes:
    - All transfers require master account API credentials
    - Master API key must have "Withdraw" permission enabled
    - Always verify transfer parameters before execution
    """

    def __init__(self, api_key: str, api_secret: str, rate_limit: int = 2):
        """
        Initialize the Kraken client.

        Args:
            api_key (str): Kraken API key
            api_secret (str): Kraken API secret
            rate_limit (int): Maximum requests per second (default: 2)

        Raises:
            AuthenticationError: If credentials are invalid
        """
        self.api_url = "https://api.kraken.com"
        self.api_key = api_key
        self.api_secret = api_secret
        self.rate_limit = rate_limit
        self.last_request_time = 0

        logger.info("Initializing Kraken client")

        # Test credentials
        if not self.test_connection():
            raise AuthenticationError("Failed to authenticate with Kraken API")

        logger.info("✅ Kraken client initialized successfully")

    def _ensure_rate_limit(self):
        """Ensure we don't exceed the rate limit."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < (1 / self.rate_limit):
            sleep_time = (1 / self.rate_limit) - time_since_last
            time.sleep(sleep_time)

    def _make_request(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make a request to the Kraken API with proper error handling.

        Args:
            path (str): API endpoint path
            params (Optional[Dict[str, Any]]): Request parameters

        Returns:
            Dict[str, Any]: API response

        Raises:
            AuthenticationError: If authentication fails
            RateLimitError: If rate limit is exceeded
            KrakenAPIError: For other API errors
        """
        self._ensure_rate_limit()

        url = f"{self.api_url}{path}"

        if params is None:
            params = {}
        params["nonce"] = int(time.time() * 1000000)  # Microsecond nonce

        headers = create_auth_headers(self.api_key, self.api_secret, path, params)

        try:
            logger.debug(f"Making request to {path}")
            response = requests.post(url, headers=headers, data=params, timeout=30)
            response.raise_for_status()

            result = response.json()

            # Check for API errors
            if "error" in result and result["error"]:
                error_messages = result["error"]
                if any("EAPI:Invalid key" in err for err in error_messages):
                    raise AuthenticationError(
                        f"Invalid API credentials: {error_messages}"
                    )
                elif any("EGeneral:Permission denied" in err for err in error_messages):
                    raise AuthenticationError(f"Permission denied: {error_messages}")
                elif any("EGeneral:Too many requests" in err for err in error_messages):
                    raise RateLimitError("Rate limit exceeded")
                else:
                    raise KrakenAPIError(f"Kraken API error: {error_messages[0]}")

            self.last_request_time = time.time()
            return result

        except requests.exceptions.Timeout:
            raise KrakenAPIError("Request timeout")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                raise RateLimitError("HTTP 429: Rate limit exceeded")
            else:
                raise KrakenAPIError(
                    f"HTTP error {e.response.status_code}: {e.response.text}"
                )
        except requests.exceptions.RequestException as e:
            raise KrakenAPIError(f"Request failed: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test API connection and authentication.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            response = self._make_request("/0/private/Balance")
            return "result" in response
        except Exception as e:
            logger.error(f"Connection test failed: {str(e)}")
            return False

    def get_account_balance(self) -> Dict[str, float]:
        """
        Get account balance for all assets.

        Returns:
            Dict[str, float]: Dictionary mapping asset names to balances

        Example:
            >>> client = KrakenClient(api_key, api_secret)
            >>> balance = client.get_account_balance()
            >>> print(balance)
            {'ZUSD': 1000.0, 'XETH': 2.5}
        """
        logger.info("Fetching account balance")
        response = self._make_request("/0/private/Balance")

        if "result" not in response:
            raise KrakenAPIError("Invalid response from balance endpoint")

        # Convert string values to float
        balance = {asset: float(amount) for asset, amount in response["result"].items()}

        logger.info(f"Retrieved balance for {len(balance)} assets")
        return balance

    def transfer_between_accounts(
        self, asset: str, amount: float, from_iiban: str, to_iiban: str
    ) -> Dict[str, Any]:
        """
        Transfer assets between any two accounts (master or subaccounts).

        This is the universal transfer method that can handle:
        - Master → Subaccount
        - Subaccount → Master
        - Subaccount → Subaccount (direct transfer)

        Args:
            asset (str): Asset to transfer (e.g., "USD", "ETH")
            amount (float): Amount to transfer
            from_iiban (str): Source account IIBAN (Public ID)
            to_iiban (str): Destination account IIBAN (Public ID)

        Returns:
            Dict[str, Any]: Transfer result with transfer_id and status

        Raises:
            TransferError: If transfer fails

        Security Warning:
            This executes a real financial transaction. Verify all parameters
            before calling this method.

        Example:
            >>> # Transfer from staging to production subaccount
            >>> result = client.transfer_between_accounts(
            ...     "USD", 100.0,
            ...     "AA02 N84G AHGV XD4A",  # staging
            ...     "AA03 N84G AHGV XD4B"   # production
            ... )

        Note:
            - Must use master account API key with Withdraw permission
            - IIBAN format: "AAXX XXXX XXXX XXXX" (with spaces)
            - IIBANs can be found in Kraken web interface under account settings
        """
        logger.info(
            f"Transferring {amount} {asset} from {from_iiban} to {to_iiban}"
        )

        params = {
            "asset": asset,
            "amount": str(amount),
            "from": from_iiban,
            "to": to_iiban,
        }

        logger.debug(f"Transfer params: {params}")

        try:
            response = self._make_request("/0/private/AccountTransfer", params)

            if "result" not in response:
                raise TransferError("Transfer failed: Invalid response")

            logger.info(f"✅ Transfer completed: {response['result']}")
            return response["result"]

        except KrakenAPIError as e:
            raise TransferError(f"Transfer failed: {str(e)}")
