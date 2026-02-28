from app.extensions import db
from app.models.shift import Shift
from app.models.job import Job

def get_user_shifts(user_id: int):
    """Return all shifts for a user, most recent first."""
    return(
        Shift.query
        .filter_by(user_id=user_id)
        .order_by(Shift.start_time.desc())
        .all()
    )

def create_shift(user_id: int, job_id: int, start_time, end_time, break_duration, notes: str) -> Shift:
    """Create and persist a manual shift."""
    shift = Shift(
        user_id=user_id,
        job_id=job_id,
        start_time=start_time,
        end_time=end_time,
        break_duration=break_duration,
        notes=notes,
        source="manual"
    )
    db.session.add(shift)
    db.session.commit()
    return shift

def update_shift(shift: Shift, job_id: int, start_time, end_time, break_duration, notes: str) -> Shift:
    """Update an existing shift."""
    shift.job_id = job_id
    shift.start_time = start_time
    shift.end_time = end_time
    shift.break_duration = break_duration
    shift.notes = notes
    db.session.commit()
    return shift


def delete_shift(shift: Shift) -> None:
    """Delete a shift."""
    db.session.delete(shift)
    db.session.commit()


def get_shift_or_404(shift_id: int, user_id: int) -> Shift:
    """Fetch shift by id, scoped to user."""
    return Shift.query.filter_by(id=shift_id, user_id=user_id).first_or_404()


def get_active_jobs_for_user(user_id: int):
    """Return active jobs as choices for the shift form."""
    return Job.query.filter_by(user_id=user_id, is_active=True).all()