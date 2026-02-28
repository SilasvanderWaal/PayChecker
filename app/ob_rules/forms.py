from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange


PERIOD_CHOICES = [
    ("weekday_evening", "Weekday Evening"),
    ("weekday_night", "Weekday Night"),
    ("saturday", "Saturday"),
    ("sunday", "Sunday"),
    ("public_holiday", "Public Holiday"),
]

HOUR_CHOICES = [(h, f"{h:02d}") for h in range(24)]
MINUTE_CHOICES = [(0, "00"), (15, "15"), (30, "30"), (45, "45")]


class OBRuleForm(FlaskForm):
    period = SelectField("Period", choices=PERIOD_CHOICES, validators=[DataRequired()])
    start_hour = SelectField("Start Hour", coerce=int, choices=HOUR_CHOICES)
    start_minute = SelectField("Start Minute", coerce=int, choices=MINUTE_CHOICES)
    end_hour = SelectField("End Hour", coerce=int, choices=HOUR_CHOICES)
    end_minute = SelectField("End Minute", coerce=int, choices=MINUTE_CHOICES)
    percentage = DecimalField(
        "OB Supplement (%)",
        validators=[DataRequired(), NumberRange(min=0.01)],
        places=2
    )
    submit = SubmitField("Save Rule")