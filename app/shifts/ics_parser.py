from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from typing import List

from icalendar import Calendar
import recurring_ical_events


@dataclass
class ShiftCandidate:
    """Intermediate representation of a parsed calendar event."""
    ics_uid: str
    start_time: datetime
    end_time: datetime
    notes: str

    @property
    def unique_key(self) -> str:
        """Compostie key for recurring event deduplication"""
        return f"{self.ics_uid}_{self.start_time.isoformat()}"

def _to_utc(dt) -> datetime:
    """Normalise a date or datetime to a UTC-aware datetime."""
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            # Assume UTC if no timezone info
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    else:
        # All-day event — treat midnight UTC
        return datetime(dt.year, dt.month, dt.day, tzinfo=timezone.utc)


def parse_ics(file_bytes: bytes) -> List[ShiftCandidate]:
    """
    Parse an ICS file and return a list of ShiftCandidates.
    Expands recurring events up to 1 year from today.
    """
    calendar = Calendar.from_ical(file_bytes)

    start_range = datetime.now(timezone.utc)
    end_range = start_range + timedelta(days=365)

    events = recurring_ical_events.of(calendar).between(start_range, end_range)

    candidates = []
    for event in events:
        uid = str(event.get("UID", ""))
        if not uid:
            continue

        start = _to_utc(event.get("DTSTART").dt)
        end = _to_utc(event.get("DTEND").dt) if event.get("DTEND") else start + timedelta(hours=1)
        summary = str(event.get("SUMMARY", ""))

        candidates.append(ShiftCandidate(
            ics_uid=uid,
            start_time=start,
            end_time=end,
            notes=summary
        ))

    return candidates