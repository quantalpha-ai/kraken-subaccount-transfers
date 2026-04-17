"""
Environment variable loader for Kraken API credentials

This module provides utilities for loading Kraken API credentials from
environment variables using suffixes to distinguish between different accounts.
"""

import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def load_kraken_credentials(suffix: str) -> Dict[str, str]:
    """
    Load Kraken API credentials for a specific account by suffix.

    Args:
        suffix (str): The account suffix (e.g., "MASTER", "STAGING", "PRODUCTION")

    Returns:
        Dict[str, str]: Dictionary containing api_key, api_secret, and iiban

    Raises:
        ValueError: If any required credential is missing

    Example:
        >>> creds = load_kraken_credentials("MASTER")
        >>> print(creds['api_key'])
        >>> print(creds['iiban'])
    """
    api_key_key = f"KRAKEN_API_KEY_{suffix}"
    api_secret_key = f"KRAKEN_API_SECRET_{suffix}"
    iiban_key = f"KRAKEN_IIBAN_{suffix}"

    api_key = os.getenv(api_key_key)
    api_secret = os.getenv(api_secret_key)
    iiban = os.getenv(iiban_key)

    # Validate all credentials are present
    missing = []
    if not api_key:
        missing.append(api_key_key)
    if not api_secret:
        missing.append(api_secret_key)
    if not iiban:
        missing.append(iiban_key)

    if missing:
        raise ValueError(
            f"Missing required environment variables for suffix '{suffix}': "
            f"{', '.join(missing)}"
        )

    return {
        "api_key": api_key,
        "api_secret": api_secret,
        "iiban": iiban,
    }
