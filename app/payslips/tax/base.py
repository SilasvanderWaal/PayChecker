from dataclasses import dataclass

@dataclass
class TaxResult:
    gross: float
    tax: float
    net: float
    breakdown: float

class TaxStrategy(ABC):
    @abstractmethod
    def calculate(self, gross: float, metadata: dict) -> TaxResult:
        """metadata can carry tax year, jurisdiction, filling status, etc"""