from flask_forms import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class DepartmentForm(Flaskform):
	"""
	Form for admin to add or edit a department
	"""
	name = StringField("Name", validators=[DataRequired()])
	description = StringField("Description", validators=[DataRequired()])
	submit = SubmitField("Submit")
