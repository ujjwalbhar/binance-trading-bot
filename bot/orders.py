from bot.client import BinanceClient
from bot.logging_config import setup_logger

logger = setup_logger()


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None
) -> dict:
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
    }

    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    if order_type.upper() == "STOP_MARKET":
        if price:
            params["stopPrice"] = price

    price_info = f" price={price}" if price else ""
    logger.info(
        f"Placing {order_type.upper()} {side.upper()} order | "
        f"symbol={symbol.upper()} qty={quantity}{price_info}"
    )

    response = client.post("/fapi/v1/order", params)
    return response
