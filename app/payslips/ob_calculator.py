from datetime import datetime, date, timedelta, timezone
from typing import List
from workalendar.europe import Sweden

from app.models.ob_rule import OBRule
from app.models.shift import Shift

_calendar = Sweden()


def _is_public_holiday(d: date) -> bool:
    return _calendar.is_working_day(d) is False and d.weekday() < 5


def _rule_applies_to_day(rule: OBRule, d: date) -> bool:
    """Check if an OB rule is relevant for a given calendar day."""
    weekday = d.weekday()  # 0=Monday, 6=Sunday

    if rule.period == "public_holiday":
        return _is_public_holiday(d)
    if rule.period == "sunday":
        return weekday == 6
    if rule.period == "saturday":
        return weekday == 5
    if rule.period in ("weekday_evening", "weekday_night"):
        return weekday < 5 and not _is_public_holiday(d)
    return False


def _overlap_minutes(
    shift_start: datetime,
    shift_end: datetime,
    window_start: datetime,
    window_end: datetime
) -> float:
    """Return overlapping minutes between two datetime ranges."""
    latest_start = max(shift_start, window_start)
    earliest_end = min(shift_end, window_end)
    delta = (earliest_end - latest_start).total_seconds()
    return max(delta / 60, 0)


def calculate_ob_supplement(shift: Shift, ob_rules: List[OBRule]) -> float:
    """
    Calculate total OB supplement in SEK for a single shift.
    Iterates day by day to handle shifts crossing midnight.
    """
    if not ob_rules:
        return 0.0

    hourly_rate = float(shift.job.hourly_rate)
    rate_per_minute = hourly_rate / 60
    total_supplement = 0.0

    # Iterate through each calendar day the shift touches
    current_day = shift.start_time.date()
    end_day = shift.end_time.date()

    while current_day <= end_day:
        for rule in ob_rules:
            if not _rule_applies_to_day(rule, current_day):
                continue

            # Build the rule window for this specific day
            window_start = datetime(
                current_day.year, current_day.month, current_day.day,
                rule.start_hour, rule.start_minute
            )
            window_end = datetime(
                current_day.year, current_day.month, current_day.day,
                rule.end_hour, rule.end_minute
            )

            # Handle windows crossing midnight (e.g. 23:00-06:00)
            if window_end <= window_start:
                window_end += timedelta(days=1)

            overlap = _overlap_minutes(
                shift.start_time, shift.end_time,
                window_start, window_end
            )

            if overlap > 0:
                supplement = overlap * rate_per_minute * (float(rule.percentage) / 100)
                total_supplement += supplement

        current_day += timedelta(days=1)

    return round(total_supplement, 2)