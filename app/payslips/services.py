from datetime import datetime
from dataclasses import dataclass, field
from typing import List

from app.models.shift import Shift
from app.models.job import Job
from app.payslips.tax import get_tax_strategy

from sqlalchemy import extract as db_extract

@dataclass
class JobSummary:
    job_name: str
    currency: str
    hourly_rate: float
    hours_worked: float
    gross: float


@dataclass
class PayslipResult:
    year: int
    month: int
    job_summaries: List[JobSummary]
    total_gross: float
    municipal_tax: float
    state_tax: float
    total_tax: float
    net: float
    breakdown: dict = field(default_factory=dict)

    @property
    def month_name(self) -> str:
        return datetime(self.year, self.month, 1).strftime("%B %Y")


def calculate_payslip(user_id: int, year: int, month: int) -> PayslipResult:
    """
    Calculate a combined payslip for a user across all jobs for a given month.
    """
    # Fetch all shifts for the user in the given month
    shifts = (
        Shift.query
        .filter(
            Shift.user_id == user_id,
            db_extract("year", Shift.start_time) == year,
            db_extract("month", Shift.start_time) == month
        )
        .all()
    )

    # Group shifts by job
    job_data = {}
    for shift in shifts:
        job = shift.job
        if job.id not in job_data:
            job_data[job.id] = {
                "job": job,
                "hours": 0.0
            }
        job_data[job.id]["hours"] += shift.duration_hours

    # Build per-job summaries
    job_summaries = []
    total_gross = 0.0

    for entry in job_data.values():
        job = entry["job"]
        hours = entry["hours"]
        gross = hours * float(job.hourly_rate)
        total_gross += gross
        job_summaries.append(JobSummary(
            job_name=job.name,
            currency=job.currency,
            hourly_rate=float(job.hourly_rate),
            hours_worked=round(hours, 2),
            gross=round(gross, 2)
        ))

    # Apply tax strategy
    strategy = get_tax_strategy("swedish")
    tax_result = strategy.calculate(total_gross)

    return PayslipResult(
        year=year,
        month=month,
        job_summaries=job_summaries,
        total_gross=tax_result.gross,
        municipal_tax=tax_result.municipal_tax,
        state_tax=tax_result.state_tax,
        total_tax=tax_result.total_tax,
        net=tax_result.net,
        breakdown=tax_result.breakdown
    )