import os

from flask import request, render_template, Blueprint, redirect, url_for, session, flash

import auth
import forms
from service.machine_service import MachineService
from service.user_service import UserService

administration = Blueprint("administration", __name__)


@administration.route('', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required("Správce")
def view_add_machine_page():
    form = forms.AddMachineForm(request.form)
    types = MachineService.get_machine_types()
    # add machine types to SelectField
    form.type.choices = [[type['id'], type['name']] for type in types]
    valid_image_formats = ['JPG', 'JPEG', 'PNG']

    if request.method == 'POST' and form.validate():
        if request.files['image'].filename == '':
            flash('Chybí obrázek')
            return render_template('administration/add_machine.jinja', form=form)

        file_name, file_extension = os.path.splitext(request.files['image'].filename)
        file_extension = file_extension[1:]
        if file_extension.upper() in valid_image_formats:
            MachineService.add_machine(name=request.form['machineName'], price_per_day=request.form['price'],
                                       type=request.form['type'], description=request.form['description'], image=request.files['image'])
            flash('Stroj přidán')
            session.pop('_flashes', None) #todo maybe smazat
            return redirect(url_for('machineoffer.view_machine_offer_page'))
        else:
            flash('Podporované formáty jsou:')
            flash(', '.join(valid_image_formats))
            return render_template('administration/add_machine.jinja', form=form)

    return render_template('administration/add_machine.jinja', form=form)


@administration.route('/manage_employee', methods=['GET', 'POST'])
@auth.login_required
@auth.roles_required("Správce")
def view_manage_employee_page():
    form = forms.ManageEmployeeForm(request.form)
    roles = UserService.get_roles()
    form.type.choices = [[type['id'], type['name']] for type in roles]
    if request.method == 'POST' and form.validate():
        UserService.alter_user_role_by_id(id=request.form["userId"], username=request.form["username"],
                                          phone_number=request.form["phone_number"], salary=request.form["salary"],
                                          role=request.form["type"])
        flash("Role změněna")
    return render_template('administration/manage_employee.jinja', form=form)
