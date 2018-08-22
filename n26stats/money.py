from decimal import ROUND_HALF_DOWN, Decimal

TWOPLACES = Decimal('10') ** -2


def quantize(value: Decimal) -> Decimal:
    return value.quantize(TWOPLACES, rounding=ROUND_HALF_DOWN)


def format(value: Decimal) -> str:
    return str(quantize(value))
