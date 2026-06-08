import argparse
import os
from dotenv import load_dotenv
from bot.client import BinanceClient
from bot.orders import place_order
from bot.validators import validate_inputs
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger()


def print_order_summary(symbol, side, order_type, quantity, price):
    print("\n========== ORDER REQUEST ==========")
    print(f"  {'symbol':<15}: {symbol.upper()}")
    print(f"  {'side':<15}: {side.upper()}")
    print(f"  {'order_type':<15}: {order_type.upper()}")
    print(f"  {'quantity':<15}: {quantity}")
    print(f"  {'price':<15}: {price if price else 'N/A (MARKET)'}")
    print("===================================\n")


def print_order_response(resp: dict):
    print("\n========== ORDER RESPONSE ==========")
    fields = ["orderId", "symbol", "side", "type", "status",
              "executedQty", "avgPrice", "origQty", "price"]
    for f in fields:
        if f in resp:
            print(f"  {f:<15}: {resp[f]}")
    print("=====================================\n")


def main():
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--symbol", required=True,
                        help="Trading pair symbol (e.g. BTCUSDT)")
    parser.add_argument("--side", required=True,
                        help="Order side: BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type",
                        help="Order type: MARKET, LIMIT, or STOP_MARKET")
    parser.add_argument("--quantity", required=True, type=float,
                        help="Order quantity (e.g. 0.01)")
    parser.add_argument("--price", required=False, type=float, default=None,
                        help="Limit/stop price (required for LIMIT orders)")

    args = parser.parse_args()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("ERROR: BINANCE_API_KEY and BINANCE_API_SECRET must be set in .env")
        logger.error("Missing API credentials in environment variables.")
        exit(1)

    try:
        validate_inputs(
            args.symbol, args.side, args.order_type,
            args.quantity, args.price
        )
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"\n[VALIDATION ERROR] {e}\n")
        exit(1)

    print_order_summary(
        args.symbol, args.side, args.order_type,
        args.quantity, args.price
    )

    client = BinanceClient(api_key, api_secret)

    try:
        response = place_order(
            client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price
        )
        print_order_response(response)
        print("[SUCCESS] Order placed successfully!")
        logger.info(
            f"Order SUCCESS | orderId={response.get('orderId')} "
            f"status={response.get('status')}"
        )
    except Exception as e:
        print(f"\n[FAILURE] Order failed: {e}\n")
        logger.error(f"Order FAILED: {e}")
        exit(1)


if __name__ == "__main__":
    main()
