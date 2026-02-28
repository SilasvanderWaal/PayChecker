from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class TaxResult:
    gross: float
    municipal_tax: float
    state_tax: float
    net: float
    breakdown: float

    @property
    def total_tax(self) -> float:
        return self.municipal_tax + self.state_tax

class TaxStrategy(ABC):
    @classmethod
    @abstractmethod
    def calculate(self, gross: float, metadata: dict) -> TaxResult:
        """metadata can carry tax year, jurisdiction, filling status, etc"""
        ...