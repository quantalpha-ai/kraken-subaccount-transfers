# Kraken Subaccount Transfer Tool

Simple, transparent tool for transferring assets between Kraken subaccounts.

## ⚠️ Security & Legal Disclaimer

**READ THIS CAREFULLY BEFORE USE**

This software is provided **"AS IS"**, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement.

**USE AT YOUR OWN RISK.** This software:
- Interacts directly with your Kraken financial accounts
- Executes real financial transactions
- Requires API keys with **Withdraw** permission
- May contain bugs, errors, or security vulnerabilities

**YOU ARE SOLELY RESPONSIBLE** for:
- Reviewing all code before execution
- Verifying all transaction parameters
- Securing your API keys
- Any financial losses or damages
- Compliance with all applicable laws and regulations

The authors and contributors of this software shall not be liable for any claim, damages, or other liability arising from your use of this software.

**By using this software, you acknowledge that you have read, understood, and accepted these terms.**

---

## What This Tool Does

This tool helps you transfer assets (like USD) between Kraken subaccounts with a simple, transparent workflow:

1. **Check balances** on both accounts
2. **Execute transfer** from one subaccount to another
3. **Verify transfer** by checking updated balances

### Key Features

- ✅ Simple, transparent codebase (easy to audit)
- ✅ Minimal dependencies (reduces attack surface)
- ✅ Direct subaccount-to-subaccount transfers (no master account intermediary needed)
- ✅ Comprehensive error handling and validation
- ✅ Balance verification before and after transfers
- ✅ Clear documentation and security warnings

---

## Prerequisites

### 1. Kraken Account Setup

You need:
- A Kraken master account
- Two or more subaccounts (e.g., staging, production)
- Master account API key with **Withdraw permission** enabled

### 2. Get Your Account IIBANs

IIBANs (Internal Identifiers) are required for transfers. To find them:

1. Log into Kraken web interface
2. Go to **Settings** → **API**
3. Find each account's IIBAN (format: `AAXX XXXX XXXX XXXX`)
4. Copy these for your `.env` configuration

### 3. Create Master API Key

**IMPORTANT:** The API key must be from your **master account** and have **Withdraw** permission.

1. In Kraken, go to **Settings** → **API**
2. Click **Generate New Key**
3. Enable **Query Funds** and **Withdraw** permissions
4. Save the API Key and API Secret securely
5. **NEVER share or commit these credentials**

---

## Installation

### Option 1: Using Miniconda (Recommended)

Miniconda is a lightweight Python environment manager. If you don't have it:

**Download Miniconda:**
- Visit: https://docs.conda.io/en/latest/miniconda.html
- Download the installer for your operating system
- Follow installation instructions

**Setup:**

```bash
# 1. Clone or download this repository
git clone https://github.com/quantalpha-ai/kraken-subaccount-transfers.git
cd kraken-subaccount-transfers

# 2. Create conda environment
conda env create -f environment.yml

# 3. Activate environment
conda activate kraken-tools

# 4. Configure your credentials (see next section)
cp .env.template .env
# Edit .env with your actual API keys and IIBANs
```

### Option 2: Using pip/venv

```bash
# 1. Clone repository
git clone https://github.com/quantalpha-ai/kraken-subaccount-transfers.git
cd kraken-subaccount-transfers

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure credentials
cp .env.template .env
# Edit .env with your actual API keys and IIBANs
```

---

## Configuration

### 1. Copy the template

```bash
cp .env.template .env
```

### 2. Edit `.env` with your credentials

Open `.env` in a text editor and add your actual values:

```bash
# Master Account (required - must have Withdraw permission)
KRAKEN_API_KEY_MASTER=your_actual_api_key_here
KRAKEN_API_SECRET_MASTER=your_actual_api_secret_here
KRAKEN_IIBAN_MASTER=AA01 XXXX XXXX XXXX

# Staging Subaccount
KRAKEN_API_KEY_STAGING=your_staging_api_key_here
KRAKEN_API_SECRET_STAGING=your_staging_api_secret_here
KRAKEN_IIBAN_STAGING=AA02 XXXX XXXX XXXX

# Production Subaccount
KRAKEN_API_KEY_PRODUCTION=your_production_api_key_here
KRAKEN_API_SECRET_PRODUCTION=your_production_api_secret_here
KRAKEN_IIBAN_PRODUCTION=AA03 XXXX XXXX XXXX
```

### 3. Secure your `.env` file

**CRITICAL:** Never commit `.env` to version control!

```bash
# Verify .env is in .gitignore
cat .gitignore | grep .env

# Check git status (should NOT show .env)
git status
```

---

## Usage

### Option 1: Using Jupyter in Browser (Traditional)

```bash
# Make sure environment is activated
conda activate kraken-tools

# Start Jupyter
jupyter notebook
```

This will:
1. Start the Jupyter server
2. Automatically open your browser to http://localhost:8888
3. Show a file browser where you can click on `subaccount_transfer.ipynb`

### Option 2: Using VS Code (Alternative)

If you prefer VS Code:

1. **Install the Jupyter extension** in VS Code (if not already installed)
2. **Open the project folder** in VS Code
3. **Open** `subaccount_transfer.ipynb`
4. **Select the kernel**: Click on "Select Kernel" in the top-right
   - Choose the `kraken-tools` conda environment
5. **Run cells** by clicking the play button or using Shift+Enter

**Tip:** VS Code provides better autocomplete and debugging than browser Jupyter.

### Follow the Notebook Steps

The notebook guides you through:

1. **Import libraries** and initialize
2. **Load credentials** from `.env`
3. **Initialize Kraken client** (tests your API credentials)
4. **Check current balances** on both accounts
5. **Configure transfer** (asset, amount, direction)
6. **Execute transfer** (with confirmation prompt)
7. **Verify transfer** (check updated balances)

### Transfer Flow

**Kraken API supports direct transfers:**
- Master ↔ Subaccount
- Subaccount ↔ Subaccount (direct, no intermediary)

All transfers require the **master account API key** with **Withdraw** permission.

---

## Security Best Practices

### API Key Security

1. **Minimal Permissions:** Only enable required permissions (Query Funds, Withdraw)
2. **Key Rotation:** Rotate API keys periodically (monthly or quarterly)
3. **Separate Keys:** Use different API keys for different purposes
4. **Secure Storage:** Never store keys in code, screenshots, or version control
5. **Access Control:** Limit who has access to API credentials

### Environment Security

1. **Verify .gitignore:** Ensure `.env` is ignored by git
2. **Private Repository:** Keep this repository private if it contains any account-specific information
3. **Code Review:** Review all code changes before running
4. **Audit Logs:** Regularly check Kraken's API activity logs

### Transfer Verification

1. **Check Balances:** Always verify balances before and after transfers
2. **Start Small:** Test with small amounts first
3. **Confirm Parameters:** Double-check asset names, amounts, and account IIBANs
4. **Monitor Transfers:** Check Kraken web interface to verify transfers completed

---

## Troubleshooting

### Authentication Errors

**Error:** `AuthenticationError: Invalid API credentials`

**Solutions:**
- Verify API key and secret are correct in `.env`
- Ensure master account API key has **Withdraw** permission
- Check for extra spaces or quotes in `.env` file
- Try regenerating API key in Kraken

### Transfer Errors

**Error:** `TransferError: Transfer failed`

**Common causes:**
- Insufficient balance in source account
- Incorrect IIBAN format (should be: `AAXX XXXX XXXX XXXX`)
- Wrong asset name (use `ZUSD` not `USD`, `XXBT` not `BTC`)
- API key lacks Withdraw permission
- Rate limiting (wait a few seconds and retry)

### Balance Not Updating

**Issue:** Balances don't reflect transfer immediately

**Solutions:**
- Wait 5-10 seconds and re-run balance check cell
- Check Kraken web interface for transfer status
- Verify transfer ID in Kraken's transaction history

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'kraken_tools'`

**Solutions:**
- Ensure you're in the correct directory (`kraken-subaccount-transfers/`)
- Activate the conda environment: `conda activate kraken-tools`
- Reinstall dependencies: `pip install -r requirements.txt`

---

## Understanding Kraken Asset Names

Kraken uses specific asset codes:

| Common Name | Kraken Code |
|-------------|-------------|
| US Dollar   | `ZUSD`      |
| Bitcoin     | `XXBT`      |
| Ethereum    | `XETH`      |
| Euro        | `ZEUR`      |

**Tip:** Check your account balance in the notebook to see the exact asset names.

---

## Project Structure

```
kraken-subaccount-transfers/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── environment.yml              # Conda environment specification
├── .env.template                # Template for credentials
├── .gitignore                   # Git ignore rules
├── subaccount_transfer.ipynb    # Main transfer notebook
└── kraken_tools/                # Python package
    ├── __init__.py              # Package initialization
    ├── auth.py                  # Kraken API authentication
    ├── client.py                # Kraken API client
    ├── env_loader.py            # Environment variable loader
    └── exceptions.py            # Custom exception classes
```

---

## Technical Details

### Kraken API Endpoints Used

- **Balance:** `/0/private/Balance` - Get account balances
- **AccountTransfer:** `/0/private/AccountTransfer` - Transfer between accounts

### Authentication

Uses Kraken's signature-based authentication:
1. Generates nonce (timestamp-based unique ID)
2. Creates HMAC-SHA512 signature with API secret
3. Includes signature in request headers

### Rate Limiting

Default: 2 requests per second (configurable in `KrakenClient`)

---

## Contributing

This is a simple utility tool. If you find bugs or have suggestions:

1. Review the code thoroughly
2. Test changes extensively with small amounts
3. Create a pull request with detailed description

**Remember:** Any changes to this code will handle real financial transactions. Test carefully!

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

**Summary:** You can use, modify, and distribute this software, but it comes with NO WARRANTY. Use at your own risk.

---

## Support

### Official Kraken Resources

- **Kraken Support:** https://support.kraken.com
- **Kraken API Docs:** https://docs.kraken.com/api/
- **Kraken API Status:** https://status.kraken.com

### This Repository

For issues with this tool:
- Review the **Troubleshooting** section above
- Check Kraken's API documentation
- Verify your setup against the **Configuration** section

**Important:** This is an independent tool, not officially supported by Kraken.

---

## Acknowledgments

This tool is built using:
- **Kraken REST API** - https://www.kraken.com
- **Python** - https://www.python.org
- **Jupyter** - https://jupyter.org
- **requests** - HTTP library for Python

---

**Remember:** Always review code that handles your financial accounts. Stay safe! 🔒
