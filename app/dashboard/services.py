from datetime import datetime, timedelta
from sqlalchemy import extract as db_extract

from app.models.shift import Shift
from app.models.ob_rule import OBRule
from app.payslips.services import calculate_payslip
from app.payslips.ob_calculator import calculate_ob_supplement


def get_dashboard_data(user_id: int) -> dict:
    now = datetime.now()
    year, month = now.year, now.month

    # Hours worked this month
    shifts_this_month = (
        Shift.query
        .filter(
            Shift.user_id == user_id,
            db_extract("year", Shift.start_time) == year,
            db_extract("month", Shift.start_time) == month
        )
        .all()
    )
    hours_this_month = sum(s.duration_hours for s in shifts_this_month)

    # Current month earnings estimate
    payslip = calculate_payslip(user_id, year, month)

    # Upcoming shifts (next 14 days)
    upcoming = (
        Shift.query
        .filter(
            Shift.user_id == user_id,
            Shift.start_time >= now,
            Shift.start_time <= now + timedelta(days=14)
        )
        .order_by(Shift.start_time)
        .limit(5)
        .all()
    )

    return {
        "hours_this_month": round(hours_this_month, 2),
        "payslip": payslip,
        "upcoming_shifts": upcoming,
        "current_month": now.strftime("%B %Y")
    }