import pytest
from income_tax import taxable_income, tax_due, refund_status


def test_taxable_income_new_regime():
    assert taxable_income(1000000, "new", 0) == 925000


def test_taxable_income_old_regime():
    assert taxable_income(1000000, "old", 100000) == 850000


def test_old_regime_investment_cap():
    assert taxable_income(1000000, "old", 200000) == 800000


def test_negative_gross_income():
    with pytest.raises(ValueError):
        taxable_income(-1, "new", 0)


def test_invalid_regime():
    with pytest.raises(ValueError):
        taxable_income(100000, "invalid", 0)


def test_taxable_income_below_zero():
    assert taxable_income(50000, "new", 0) == 0


def test_negative_taxable_amount():
    with pytest.raises(ValueError):
        tax_due(-1, 30)


def test_tax_due_senior_citizen_below_exemption():
    assert tax_due(200000, 65) == 0


def test_tax_due_super_senior_below_exemption():
    assert tax_due(400000, 80) == 0


def test_tax_due_five_percent_slab():
    assert tax_due(400000, 30) == 7500


def test_tax_due_twenty_percent_slab():
    assert tax_due(700000, 30) == 52500


def test_refund_on_time():
    assert refund_status(10000, 5000, True) == "refund"


def test_refund_late():
    assert refund_status(10000, 5000, False) == "refund delayed"


def test_balance_due_on_time():
    assert refund_status(5000, 10000, True) == "pay balance"


def test_balance_due_late():
    assert refund_status(5000, 10000, False) == "pay balance with penalty"


def test_settled():
    assert refund_status(5000, 5000, True) == "settled"