import pytest
from income_tax import taxable_income, tax_due, refund_status


# taxable_income() branch tests

def test_negative_gross():
    with pytest.raises(ValueError):
        taxable_income(-1, "new", 0)


def test_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000


def test_old_regime_investments_below_cap():
    assert taxable_income(1000000, "old", 100000) == 850000


def test_old_regime_investments_above_cap():
    assert taxable_income(1000000, "old", 200000) == 800000


def test_invalid_regime():
    with pytest.raises(ValueError):
        taxable_income(100000, "invalid", 0)


def test_taxable_income_negative_after_deduction():
    assert taxable_income(50000, "new", 0) == 0


def test_taxable_income_positive_after_deduction():
    assert taxable_income(100000, "new", 0) == 25000


# tax_due() branch tests

def test_negative_taxable_amount():
    with pytest.raises(ValueError):
        tax_due(-1, 30)


def test_age_below_60():
    assert tax_due(400000, 30) == 7500


def test_age_60_to_79():
    assert tax_due(400000, 65) == 5000


def test_age_80_or_above():
    assert tax_due(400000, 80) == 0


def test_taxable_income_below_exemption():
    assert tax_due(200000, 30) == 0


def test_taxable_income_at_exemption():
    assert tax_due(250000, 30) == 0


def test_slab_at_or_below_250000():
    assert tax_due(500000, 30) == 12500


def test_slab_above_250000():
    assert tax_due(750000, 30) == 62500


# refund_status() branch tests

def test_refund_filed_on_time():
    assert refund_status(10000, 5000, True) == "refund"


def test_refund_filed_late():
    assert refund_status(10000, 5000, False) == "refund delayed"


def test_balance_filed_on_time():
    assert refund_status(5000, 10000, True) == "pay balance"


def test_balance_filed_late():
    assert refund_status(5000, 10000, False) == "pay balance with penalty"


def test_equal_tax_paid_and_due():
    assert refund_status(5000, 5000, True) == "settled"