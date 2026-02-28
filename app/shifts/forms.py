from flask_wtf import FlaskForm
from wtforms import SelectField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Optional, NumberRange
from wtforms.fields import DateTimeLocalField
from flask_wtf.file import FileField, FileRequired, FileAllowed

class ShiftForm(FlaskForm):
    job_id = SelectField("Job", coerce=int, validators=[DataRequired()])
    start_time = DateTimeLocalField(
        "Start Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    end_time = DateTimeLocalField(
        "End Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    break_duration = IntegerField(
        "Break duration (minutes)", 
        validators=[Optional(), NumberRange(min=0)], 
        default=0
    )
    notes = TextAreaField("Notes")
    submit = SubmitField("Save Shift")

    def validate_end_time(self, field):
        if self.start_time and field.data:
            if field.data <= self.start_time.data:
                raise ValidationError("End must be after start time.")
            
class ICSImportForm(FlaskForm):
    job_id = SelectField("Assign to Job", coerce=int, validators=[DataRequired()])
    ics_file = FileField(
        "ICS File",
        validators=[
            FileRequired(),
            FileAllowed(["ics"], "ICS files only.")
        ]
    )

    submit = SubmitField("Import")