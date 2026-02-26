from app.extensions import db
from app.models.job import Job


def get_user_jobs(user_id: int):
    """Return all jobs for a user, active ones first."""
    return (
        Job.query
        .filter_by(user_id=user_id)
        .order_by(Job.is_active.desc(), Job.name)
        .all()
    )


def create_job(user_id: int, name: str, hourly_rate, currency: str) -> Job:
    """Create and persist a new job for the user."""
    job = Job(
        user_id=user_id,
        name=name,
        hourly_rate=hourly_rate,
        currency=currency
    )
    db.session.add(job)
    db.session.commit()
    return job


def update_job(job: Job, name: str, hourly_rate, currency: str, is_active: bool) -> Job:
    """Update an existing job."""
    job.name = name
    job.hourly_rate = hourly_rate
    job.currency = currency
    job.is_active = is_active
    db.session.commit()
    return job


def get_job_or_404(job_id: int, user_id: int) -> Job:
    """Fetch job by id, ensuring it belongs to the requesting user."""
    return Job.query.filter_by(id=job_id, user_id=user_id).first_or_404()