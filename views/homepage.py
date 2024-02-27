from datetime import datetime, date

from flask import Blueprint, render_template, request, session, redirect, url_for, flash

import forms
from service.machine_service import MachineService

machineoffer = Blueprint("machineoffer", __name__)


@machineoffer.route('', methods=['GET', 'POST'])
def view_machine_offer_page():
    machines = MachineService.get_all()
    form = forms.MachineFilterForm(request.form)

    if 'dateFrom' not in session:
        session['dateFrom'] = ""

    if 'dateTo' not in session:
        session['dateTo'] = ""

    session['withService'] = ""  # clear on page load

    if request.method == 'GET' and form.validate():
        machineName = request.args.get('machineName')
        dateFrom = request.args.get('dateFrom')
        dateTo = request.args.get('dateTo')
        priceFrom = request.args.get('priceFrom')
        priceTo = request.args.get('priceTo')

        # prevent session value delete on page load
        if dateFrom is not None or dateTo is not None:
            if dateFrom != "" or dateTo != "":
                session['dateFrom'] = dateFrom
                session['dateTo'] = dateTo

        machines = MachineService.get_filterMachines(priceFrom, priceTo, machineName, session['dateTo'],
                                                     session['dateFrom'])

    # fill form with saved data for better user orientation or print validation error
    if session['dateFrom'] != "" and session['dateTo'] != "":
        formattedDateFrom = datetime.strptime(session['dateFrom'], "%Y-%m-%d").date()
        formattedDateTo = datetime.strptime(session['dateTo'], "%Y-%m-%d").date()
        today = datetime.today().date()

        if formattedDateFrom < today or formattedDateTo < today or formattedDateTo < formattedDateFrom:
            if 'cart' in session:
                if len(session['cart']) > 0:
                    if session['cart'][0]['from'] != session['dateFrom'] or session['cart'][0]['to'] != session['dateTo']:
                        session['dateFrom'] = session['cart'][0]['from']
                        session['dateTo'] = session['cart'][0]['to']

                        flash("V jedné objednávce musí být stejná data !")
                        flash("Filtr byl nastaven na správné hodnoty")
                        return redirect(url_for('machineoffer.view_machine_offer_page'))

            session['dateFrom'] = ""
            session['dateTo'] = ""

            flash("Neplatné datum")
            # overwrite filter with empty dates and render default page
            machines = MachineService.get_filterMachines(priceFrom, priceTo, machineName, session['dateTo'],
                                                         session['dateFrom'])
            return render_template('homepage/machine_offer.jinja', machines=machines, form=form)

        form.dateFrom.process_data(formattedDateFrom)
        form.dateTo.process_data(formattedDateTo)

    return render_template('homepage/machine_offer.jinja', machines=machines, form=form)


@machineoffer.route('/reset', methods=['GET', 'POST'])
def reset_offer_filter():
    if 'dateFrom' in session:
        session['dateFrom'] = ""

    if 'dateTo' in session:
        session['dateTo'] = ""

    return redirect(url_for('machineoffer.view_machine_offer_page'))


@machineoffer.route('/detail/<int:machine_id>', methods=['GET', 'POST'])
def show_machine_detail(machine_id):
    machine = MachineService.get_machine(machine_id)
    form = forms.MachineFilterForm(request.form)

    if request.method == 'GET' and form.validate():
        dateFrom = request.args.get('dateFrom')
        dateTo = request.args.get('dateTo')

        # prevent session value delete on page load
        if dateFrom is not None or dateTo is not None:
            if dateFrom != "" or dateTo != "":
                session['dateFrom'] = dateFrom
                session['dateTo'] = dateTo

                formattedDateFrom = datetime.strptime(session['dateFrom'], "%Y-%m-%d").date()
                formattedDateTo = datetime.strptime(session['dateTo'], "%Y-%m-%d").date()
                today = datetime.today().date()

                if formattedDateFrom < today or formattedDateTo < today or formattedDateTo < formattedDateFrom:

                    return redirect(url_for('machineoffer.view_machine_offer_page'))

            return redirect(url_for('cart.add_product_to_cart', machine_id=machine_id))

    # fill form with saved data for better user orientation
    if session['dateFrom'] != "" and session['dateTo'] != "":
        form.dateFrom.process_data(datetime.strptime(str(session['dateFrom']), "%Y-%m-%d"))
        form.dateTo.process_data(datetime.strptime(str(session['dateTo']), "%Y-%m-%d"))

    if len(machine) == 0:
        return render_template('notFound/index.jinja')
    return render_template('homepage/machine_detail.jinja', machine=machine, form=form)
