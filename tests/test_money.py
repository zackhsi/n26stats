from decimal import Decimal

from n26stats import money


def test_quantize():
    assert money.quantize(Decimal('1.005')) == Decimal('1.00')
    assert money.quantize(Decimal('1.0051')) == Decimal('1.01')
