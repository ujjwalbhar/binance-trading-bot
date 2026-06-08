VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT", "STOP_MARKET"]


def validate_inputs(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None
) -> bool:
    if not symbol or not symbol.isalpha():
        raise ValueError(
            f"Invalid symbol: '{symbol}'. Example: BTCUSDT"
        )
    if side.upper() not in VALID_SIDES:
        raise ValueError(
            f"Invalid side: '{side}'. Must be one of {VALID_SIDES}"
        )
    if order_type.upper() not in VALID_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type: '{order_type}'. Must be one of {VALID_ORDER_TYPES}"
        )
    if quantity <= 0:
        raise ValueError(
            f"Quantity must be a positive number, got: {quantity}"
        )
    if order_type.upper() == "LIMIT":
        if price is None or price <= 0:
            raise ValueError(
                "Price is required and must be positive for LIMIT orders."
            )
    return True
