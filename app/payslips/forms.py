from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime


def year_choices():
    current_year = datetime.now().year
    return [(y, str(y)) for y in range(current_year - 2, current_year + 1)]


def month_choices():
    return [
        (1, "January"), (2, "February"), (3, "March"),
        (4, "April"), (5, "May"), (6, "June"),
        (7, "July"), (8, "August"), (9, "September"),
        (10, "October"), (11, "November"), (12, "December")
    ]


class PayslipForm(FlaskForm):
    year = SelectField("Year", coerce=int, validators=[DataRequired()])
    month = SelectField("Month", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Calculate")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.year.choices = year_choices()
        self.month.choices = month_choices()