from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, URL


class CalendarFeedForm(FlaskForm):
    name = StringField("Feed Name", validators=[DataRequired(), Length(max=150)])
    url = StringField("ICS URL", validators=[DataRequired(), URL(), Length(max=2048)])
    job_id = SelectField("Assign to Job", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Save Feed")