from app.payslips.tax.swedish import SwedishTaxStrategy
from app.payslips.tax.base import TaxStrategy


def get_tax_strategy(name: str = "swedish") -> TaxStrategy:
    strategies = {
        "swedish": SwedishTaxStrategy,
    }
    cls = strategies.get(name)
    if not cls:
        raise ValueError(f"Unknown tax strategy: {name}")
    return cls()