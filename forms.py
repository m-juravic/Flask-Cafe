from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, URL, Email, Length

"""Forms for Flask Cafe."""

class AddCafeForm(FlaskForm):
    """Form for adding cafes."""

    name = StringField("Cafe Name", validators=[InputRequired()])
    description = StringField("Cafe Description", validators=[Optional()])
    url = StringField("Cafe URL", validators=[Optional(), URL()])
    address = StringField("Cafe Address", validators=[InputRequired()])
    city_code = SelectField("City Code")
    image_url = StringField("Cafe Image URL", validators=[Optional(), URL()])


class SignupForm(FlaskForm):
    '''Form to sign up a new user'''

    username = StringField("User Name", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    description = StringField("User Description", validators=[Optional()])
    email = StringField("Email Address", validators=[InputRequired(), Email()])
    password = PasswordField("Password",
                             validators=[InputRequired(), Length(min=6)])
    image_url = StringField("User Image", validators=[Optional(), URL()])


class LoginForm(FlaskForm):
    '''Form for logging a user.'''

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class ProfileEditForm(FlaskForm):
    '''Form to edit user profile'''

    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])
    description = StringField("User Description", validators=[Optional()])
    email = StringField("Email Address", validators=[InputRequired(), Email()])
    image_url = StringField("User Image", validators=[Optional(), URL()])



