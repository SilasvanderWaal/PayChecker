import requests
from datetime import datetime
from functools import lru_cache

from app.payslips.tax.base import TaxStrategy, TaxResult

_SKATTEVERKET_API = (
    "https://skatteverket.entryscape.net/rowstore/dataset/"
    "88320397-5c32-4c16-ae79-d36d95b17b95/json"
)


@lru_cache(maxsize=20)
def _fetch_tax_table(year: int, tabellnr: int) -> tuple:
    """Fetch and cache Skatteverket's monthly withholding table (30B) for a given year and table number."""
    results = []
    url = (
        f"{_SKATTEVERKET_API}"
        f"?%C3%A5r={year}&tabellnr={tabellnr}&antal+dgr=30B&_limit=1000"
    )
    while url:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results.extend(data["results"])
        url = data.get("next")
    return tuple(results)


def _lookup_withholding(rows: tuple, gross: float) -> float | None:
    """Return the kolumn 1 withholding amount for the bracket containing gross, or None."""
    for row in rows:
        try:
            low = float(row["inkomst fr.o.m."])
            high = float(row["inkomst t.o.m."])
            if low <= gross <= high:
                return float(row["kolumn 1"])
        except (ValueError, KeyError):
            continue
    return None


class SwedishTaxStrategy(TaxStrategy):
    """
    Swedish income tax using Skatteverket's official withholding table (skattetabell).

    The table (kolumn 1) gives the total monthly tax to withhold for a given gross income,
    with grundavdrag already built in. Falls back to a manual approximation if the API
    is unavailable.

    - tabellnr: municipality-specific table number (default 35, national average)
    - State tax: 20% on monthly gross above 49,875 SEK (separated from the table total)
    - Municipal rate: 32% (used to back-derive grundavdrag for the breakdown display)
    """

    MUNICIPAL_RATE = 0.32
    STATE_TAX_RATE = 0.20
    STATE_TAX_MONTHLY_THRESHOLD = 49_875  # 598,500 SEK/year

    def __init__(self, tabellnr: int = 35):
        self.tabellnr = tabellnr

    def _grundavdrag_fallback(self, gross: float) -> float:
        """Fallback grundavdrag approximation used when the API is unavailable."""
        if gross <= 14_000:
            return gross * 0.423
        elif gross <= 21_400:
            return 13_900 + (gross - 14_000) * 0.20
        elif gross <= 35_900:
            return 15_380
        elif gross <= 51_000:
            return 15_380 - (gross - 35_900) * 0.10
        else:
            return 13_870

    def calculate(self, gross: float) -> TaxResult:
        year = datetime.now().year
        api_withholding = None

        try:
            rows = _fetch_tax_table(year, self.tabellnr)
            api_withholding = _lookup_withholding(rows, gross)
        except Exception:
            pass

        if api_withholding is not None:
            # kolumn 1 is the total monthly withholding (municipal + state, grundavdrag applied).
            # Separate out state tax for the breakdown; the remainder is municipal.
            state_taxable = max(gross - self.STATE_TAX_MONTHLY_THRESHOLD, 0)
            state_tax = state_taxable * self.STATE_TAX_RATE
            municipal_tax = max(api_withholding - state_tax, 0)
            # Back-derive grundavdrag for display: taxable = municipal_tax / rate
            taxable_income = municipal_tax / self.MUNICIPAL_RATE if municipal_tax > 0 else 0
            grundavdrag = max(gross - taxable_income, 0)
            tax_source = f"Skatteverket tabell {self.tabellnr} ({year})"
        else:
            # Fallback: manual approximation
            grundavdrag = self._grundavdrag_fallback(gross)
            taxable_income = max(gross - grundavdrag, 0)
            municipal_tax = taxable_income * self.MUNICIPAL_RATE
            state_taxable = max(gross - self.STATE_TAX_MONTHLY_THRESHOLD, 0)
            state_tax = state_taxable * self.STATE_TAX_RATE
            tax_source = "approximation (API unavailable)"

        net = gross - municipal_tax - state_tax

        return TaxResult(
            gross=round(gross, 2),
            municipal_tax=round(municipal_tax, 2),
            state_tax=round(state_tax, 2),
            net=round(net, 2),
            breakdown={
                "grundavdrag": round(grundavdrag, 2),
                "taxable_income": round(taxable_income, 2),
                "municipal_rate": f"{self.MUNICIPAL_RATE * 100:.0f}%",
                "state_threshold": self.STATE_TAX_MONTHLY_THRESHOLD,
                "tax_table": self.tabellnr,
                "tax_source": tax_source,
            },
        )
