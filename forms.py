from flask_wtf.file import FileRequired, FileAllowed
from wtforms import Form, StringField, validators, PasswordField, EmailField, DateField, IntegerField, FileField, \
    SelectField, TextAreaField
from service.machine_service import MachineService


class LoginForm(Form):
    username = StringField(name='username', label='Přihlašovací jméno',
                           validators=[validators.Length(min=1, max=30), validators.InputRequired()])
    password = PasswordField(name='password', label='Heslo', validators=[validators.DataRequired()])


class RegisterForm(Form):
    username = StringField(name='username', label='Přihlašovací jméno',
                           validators=[validators.Length(min=1, max=30), validators.InputRequired()])
    name = StringField(name='name', label='Jméno',
                       validators=[validators.Length(min=1, max=30), validators.InputRequired()])
    last_name = StringField(name='last_name', label='Přijmení',
                            validators=[validators.Length(min=2, max=30), validators.InputRequired()])
    password = PasswordField(name='password', label='Heslo', validators=[validators.Length(min=8, max=30),
                                                                         validators.EqualTo('confirm_password',
                                                                                            'Hesla se neshodují'),
                                                                         validators.DataRequired()])
    confirm_password = PasswordField(label='Potvrzení hesla')
    email = EmailField(name='email', label='Email', validators=[validators.DataRequired()])


class CompleteOrderForm(Form):
    name = StringField(name='name', label='Jméno', validators=[validators.Length(min=1), validators.InputRequired()])
    last_name = StringField(name='last_name', label='Přijmení',
                            validators=[validators.Length(min=1, max=30), validators.InputRequired()])
    phone_number = StringField(name='phone_number', label='Telefonní číslo',
                               validators=[validators.Length(min=9, max=9), validators.InputRequired(),
                                           validators.regexp(r'^\d*$')])
    email = EmailField(name='email', label='Email', validators=[validators.DataRequired()])
    city = StringField(name='city', label='Město', validators=[validators.Length(min=2), validators.InputRequired()])
    street = StringField(name='street', label='Ulice',
                         validators=[validators.Length(min=2), validators.InputRequired()])
    descriptive_number = StringField(name='descriptive_number', label='Číslo popisné',
                                     validators=[validators.Length(min=1), validators.InputRequired(),
                                                 validators.regexp(r'^\d*$')])
    zip_code = StringField(name='zip_code', label='PSČ',
                           validators=[validators.Length(min=5, max=5), validators.InputRequired(),
                                       validators.regexp(r'^\d*$')])


class MachineFilterForm(Form):
    machineName = StringField(name='machineName', label='Název')
    dateFrom = DateField(name='dateFrom', label='Datum od')
    dateTo = DateField(name='dateTo', label='Datum do')
    priceFrom = IntegerField(name='priceFrom', label='cena od')
    priceTo = IntegerField(name='priceTo', label='cena do')


class AddMachineForm(Form):
    machineName = StringField(name='machineName', label='Název', validators=[validators.InputRequired()])
    price = IntegerField(name='price', label='Cena za den', validators=[validators.InputRequired()])
    type = SelectField(name='type', label='Typ', validators=[validators.InputRequired()])
    description = TextAreaField(name='description', label='Popis')
    image = FileField(name='image', label='Obrázek')


class ManageEmployeeForm(Form):
    userId = IntegerField(name='userId', label='ID Uživatele', validators=[validators.InputRequired()])
    username = StringField(name='username', label='Přihlašovací jméno',
                           validators=[validators.Length(min=1, max=30), validators.InputRequired()])
    phone_number = StringField(name='phone_number', label='Telefonní číslo:',
                               validators=[validators.Length(min=9, max=9), validators.InputRequired(),
                                           validators.regexp(r"^[0-9]{9}$")])
    salary = IntegerField(name='salary', label='Plat na hodinu', validators=[validators.InputRequired()])
    type = SelectField(name='type', label='Typ role', validators=[validators.InputRequired()])


class ProfileForm(Form):
    name = StringField(name='name', label='Jméno:', validators=[validators.Length(min=1), validators.InputRequired()])
    last_name = StringField(name='last_name', label='Přijmení:',
                            validators=[validators.Length(min=1, max=30), validators.InputRequired()])
    email = EmailField(name='email', label='Email:', validators=[validators.DataRequired()])
    phone_number = StringField(name='phone_number', label='Telefonní číslo:',
                               validators=[validators.Length(min=9, max=9), validators.InputRequired(),
                                           validators.regexp(
                                               r"^[0-9]{9}$")])  # password = PasswordField(name='password', label='Nové heslo:', validators=[validators.DataRequired()])

class AddEmployeeToOrderForm(Form):
    employee_select = SelectField(name='employee', label='Technici', validators=[validators.InputRequired()])