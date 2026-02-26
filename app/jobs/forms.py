from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from app.constants.job_constatns import JobConstants as const

class JobForm(FlaskForm):
    name = StringField("Job Name", validators=[DataRequired(), Length(max=const.MAX_NAME_LENGTH)])
    hourly_rate = DecimalField(
        "Hourly Rate",
        validators=[DataRequired(), NumberRange(min=const.MIN_HOURLY_RATE)],
        places=2
    )
    currency = SelectField("Currency",
                           choices=[("SEK","SEK"), ("EUR", "EUR"), ("USD", "USD")],
                           default="SEK"
    )
    is_active = BooleanField("Active", default=True)
    submit = SubmitField("Save Job")
