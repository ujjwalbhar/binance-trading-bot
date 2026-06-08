# Binance Futures Testnet Trading Bot

A Python CLI application to place **Market**, **Limit**, and **Stop-Market** orders on [Binance Futures Demo/Testnet](https://demo-fapi.binance.com) (USDT-M).

---

## Project Structure

```
binance-trading-bot/
├── bot/
│   ├── __init__.py          # Package init
│   ├── client.py            # Binance API client wrapper (HMAC signing)
│   ├── orders.py            # Order placement logic
│   ├── validators.py        # CLI input validation
│   └── logging_config.py    # Structured logging setup
├── cli.py                   # CLI entry point (argparse)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/ujjwalbhar/binance-trading-bot.git
cd binance-trading-bot
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API credentials
Create a `.env` file in the root directory:
```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```
> Get your keys from [Binance Demo Trading](https://demo.binance.com) → Account → API Management

---

## How to Run

### Place a MARKET BUY order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a LIMIT SELL order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 95000
```

### Place a MARKET SELL order
```bash
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.1
```

### Place a STOP_MARKET order (Bonus)
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.01 --price 90000
```

### Get help
```bash
python cli.py --help
```

---

## CLI Arguments

| Argument | Required | Description |
|-----------|----------|-------------|
| `--symbol` | Yes | Trading pair (e.g. `BTCUSDT`, `ETHUSDT`) |
| `--side` | Yes | `BUY` or `SELL` |
| `--type` | Yes | `MARKET`, `LIMIT`, or `STOP_MARKET` |
| `--quantity` | Yes | Order quantity (e.g. `0.01`) |
| `--price` | No* | Limit/stop price (*required for LIMIT) |

---

## Output Example

```
========== ORDER REQUEST ==========
  symbol         : BTCUSDT
  side           : BUY
  order_type     : MARKET
  quantity       : 0.01
  price          : N/A (MARKET)
===================================

========== ORDER RESPONSE ==========
  orderId        : 3492837
  symbol         : BTCUSDT
  side           : BUY
  type           : MARKET
  status         : FILLED
  executedQty    : 0.01
  avgPrice       : 104523.50
=====================================

[SUCCESS] Order placed successfully!
```

---

## Logging

All API requests, responses, and errors are logged to `trading_bot.log` in the root directory.

Log format:
```
2026-06-08 18:00:00 | INFO | trading_bot | Placing MARKET BUY order | symbol=BTCUSDT qty=0.01
2026-06-08 18:00:01 | DEBUG | trading_bot | Response [200]: {...}
2026-06-08 18:00:01 | INFO | trading_bot | Order SUCCESS | orderId=3492837 status=FILLED
```

---

## Assumptions

- All orders are placed on **Binance Demo Futures** (`https://demo-fapi.binance.com`), not mainnet.
- LIMIT orders require the `--price` argument.
- Quantity precision follows Binance testnet defaults.
- API credentials are stored in `.env` (never committed to version control).
- The `trading_bot.log` file is excluded from git via `.gitignore`.

---

## Bonus Feature

`STOP_MARKET` order type is supported as a bonus, in addition to MARKET and LIMIT.

---

## Requirements

- Python 3.8+
- `requests` — HTTP client for REST API calls
- `python-dotenv` — loads `.env` file for API credentials
