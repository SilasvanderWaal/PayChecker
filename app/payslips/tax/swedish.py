from app.payslips.tax.base import TaxStrategy, TaxResult


class SwedishTaxStrategy(TaxStrategy):
    """
    Swedish income tax calculation based on 2024/2025 rates.

    - Municipal tax: 32% flat (national average)
    - State tax: 20% on monthly income above 49,875 SEK
    - Basic deduction (grundavdrag) applied before municipal tax
    """

    MUNICIPAL_RATE = 0.32
    STATE_TAX_RATE = 0.20
    STATE_TAX_MONTHLY_THRESHOLD = 49_875  # 598,500 SEK/year

    def _grundavdrag(self, gross: float) -> float:
        """
        Approximate basic deduction (grundavdrag).
        Simplified linear approximation of Skatteverket's table.
        """
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
        deduction = self._grundavdrag(gross)
        taxable_income = max(gross - deduction, 0)

        municipal_tax = taxable_income * self.MUNICIPAL_RATE

        # State tax only on income above threshold
        state_taxable = max(gross - self.STATE_TAX_MONTHLY_THRESHOLD, 0)
        state_tax = state_taxable * self.STATE_TAX_RATE

        total_tax = municipal_tax + state_tax
        net = gross - total_tax

        return TaxResult(
            gross=round(gross, 2),
            municipal_tax=round(municipal_tax, 2),
            state_tax=round(state_tax, 2),
            net=round(net, 2),
            breakdown={
                "grundavdrag": round(deduction, 2),
                "taxable_income": round(taxable_income, 2),
                "municipal_rate": f"{self.MUNICIPAL_RATE * 100:.0f}%",
                "state_threshold": self.STATE_TAX_MONTHLY_THRESHOLD,
            }
        )