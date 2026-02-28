from app.extensions import db
from app.models.ob_rule import OBRule
from app.models.job import Job


def get_rules_for_job(job_id: int):
    return OBRule.query.filter_by(job_id=job_id).all()


def create_rule(job_id: int, period: str, start_hour: int, start_minute: int,
                end_hour: int, end_minute: int, percentage: float) -> OBRule:
    rule = OBRule(
        job_id=job_id,
        period=period,
        start_hour=start_hour,
        start_minute=start_minute,
        end_hour=end_hour,
        end_minute=end_minute,
        percentage=percentage
    )
    db.session.add(rule)
    db.session.commit()
    return rule


def delete_rule(rule: OBRule) -> None:
    db.session.delete(rule)
    db.session.commit()


def get_rule_or_404(rule_id: int, job_id: int) -> OBRule:
    return OBRule.query.filter_by(id=rule_id, job_id=job_id).first_or_404()


def get_job_or_404_scoped(job_id: int, user_id: int) -> Job:
    return Job.query.filter_by(id=job_id, user_id=user_id).first_or_404()