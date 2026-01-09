DEFAULT_CURRENCY = "USD"
TAX_RATE = 0.21

COUPON_SAVE10 = "SAVE10"
COUPON_SAVE20 = "SAVE20"
COUPON_VIP = "VIP"

DISCOUNT_RATE_10 = 0.10
DISCOUNT_RATE_20 = 0.20
DISCOUNT_RATE_MIN_SAVE20 = 0.05
MIN_SUBTOTAL_FOR_SAVE20 = 200
VIP_DISCOUNT_HIGH = 50
VIP_DISCOUNT_LOW = 10
VIP_THRESHOLD = 100


def validate_request(request: dict):
    user_id = request.get("user_id")
    items = request.get("items")
    currency = request.get("currency", DEFAULT_CURRENCY)
    coupon = request.get("coupon")

    if user_id is None:
        raise ValueError("user_id is required")
    if items is None:
        raise ValueError("items is required")
    if not isinstance(items, list):
        raise ValueError("items must be a list")
    if len(items) == 0:
        raise ValueError("items must not be empty")

    for item in items:
        if "price" not in item or "qty" not in item:
            raise ValueError("item must have price and qty")
        if item["price"] <= 0:
            raise ValueError("price must be positive")
        if item["qty"] <= 0:
            raise ValueError("qty must be positive")

    return user_id, items, coupon, currency


def calculate_subtotal(items):
    return sum(item["price"] * item["qty"] for item in items)


def calculate_discount(subtotal: int, coupon: str) -> int:
    if not coupon or coupon == "":
        return 0

    if coupon == COUPON_SAVE10:
        return int(subtotal * DISCOUNT_RATE_10)

    if coupon == COUPON_SAVE20:
        if subtotal >= MIN_SUBTOTAL_FOR_SAVE20:
            return int(subtotal * DISCOUNT_RATE_20)
        else:
            return int(subtotal * DISCOUNT_RATE_MIN_SAVE20)

    if coupon == COUPON_VIP:
        return VIP_DISCOUNT_HIGH if subtotal >= VIP_THRESHOLD else VIP_DISCOUNT_LOW

    raise ValueError("unknown coupon")


def generate_order_id(user_id, items_count: int) -> str:
    return f"{user_id}-{items_count}-X"


def process_checkout(request: dict) -> dict:
    user_id, items, coupon, currency = validate_request(request)

    subtotal = calculate_subtotal(items)
    discount = calculate_discount(subtotal, coupon)

    total_after_discount = max(0, subtotal - discount)
    tax = int(total_after_discount * TAX_RATE)
    total = total_after_discount + tax

    order_id = generate_order_id(user_id, len(items))

    return {
        "order_id": order_id,
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }