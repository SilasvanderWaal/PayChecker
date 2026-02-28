from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from sqlalchemy import extract as db_extract

from app.models.shift import Shift
from app.models.ob_rule import OBRule
from app.payslips.tax import get_tax_strategy
from app.payslips.ob_calculator import calculate_ob_supplement


@dataclass
class JobSummary:
    job_name: str
    currency: str
    hourly_rate: float
    hours_worked: float
    gross: float
    ob_supplement: float

    @property
    def total(self) -> float:
        return round(self.gross + self.ob_supplement, 2)


@dataclass
class PayslipResult:
    year: int
    month: int
    job_summaries: List[JobSummary]
    total_gross: float
    ob_supplement: float
    municipal_tax: float
    state_tax: float
    total_tax: float
    net: float
    breakdown: dict = field(default_factory=dict)

    @property
    def month_name(self) -> str:
        return datetime(self.year, self.month, 1).strftime("%B %Y")


def calculate_payslip(user_id: int, year: int, month: int) -> PayslipResult:
    shifts = (
        Shift.query
        .filter(
            Shift.user_id == user_id,
            db_extract("year", Shift.start_time) == year,
            db_extract("month", Shift.start_time) == month
        )
        .all()
    )

    job_data = {}
    for shift in shifts:
        job = shift.job
        if job.id not in job_data:
            job_data[job.id] = {"job": job, "hours": 0.0, "ob_supplement": 0.0}

        job_data[job.id]["hours"] += shift.duration_hours

        ob_rules = OBRule.query.filter_by(job_id=job.id).all()
        job_data[job.id]["ob_supplement"] += calculate_ob_supplement(shift, ob_rules)

    job_summaries = []
    total_gross = 0.0
    total_ob = 0.0

    for entry in job_data.values():
        job = entry["job"]
        hours = entry["hours"]
        gross = hours * float(job.hourly_rate)
        ob = entry["ob_supplement"]
        total_gross += gross
        total_ob += ob

        job_summaries.append(JobSummary(
            job_name=job.name,
            currency=job.currency,
            hourly_rate=float(job.hourly_rate),
            hours_worked=round(hours, 2),
            gross=round(gross, 2),
            ob_supplement=round(ob, 2)
        ))

    taxable_gross = total_gross + total_ob
    strategy = get_tax_strategy("swedish")
    tax_result = strategy.calculate(taxable_gross)

    return PayslipResult(
        year=year,
        month=month,
        job_summaries=job_summaries,
        total_gross=tax_result.gross,
        ob_supplement=round(total_ob, 2),
        municipal_tax=tax_result.municipal_tax,
        state_tax=tax_result.state_tax,
        total_tax=tax_result.total_tax,
        net=tax_result.net,
        breakdown=tax_result.breakdown
    )