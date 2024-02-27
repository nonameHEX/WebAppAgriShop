import datetime

from flask import request, render_template, Blueprint, redirect, url_for, session, flash, jsonify

import auth
import forms
from service.machine_service import MachineService
from service.reservation_service import ReservationService
from service.order_service import OrderService
from service.user_service import UserService

completeOrder = Blueprint("completeOrder", __name__)
cart = Blueprint("cart", __name__)
orders = Blueprint("orders", __name__)
workOrders = Blueprint("workOrders", __name__)


@cart.route('')
def view_cart_page():
    items = []
    # session.pop("cart")

    if 'cart' in session:
        for product in session['cart']:
            machine = MachineService.get_machine(product['id'])

            # add machine info to cart item list
            if machine is not None:
                for m in machine:
                    # calculate days between
                    formattedDateFrom = datetime.datetime.strptime(product['from'], "%Y-%m-%d").date()
                    formattedDateTo = datetime.datetime.strptime(product['to'], "%Y-%m-%d").date()

                    daysBetween = formattedDateTo - formattedDateFrom
                    daysBetween = daysBetween.days

                    items.append(
                        {"image": m['image'], "name": m['name'], "days": daysBetween, "service": product['service'],
                         "price": m['price_per_day'],
                         "index": product['index']})

    return render_template('orders/cart.jinja', products=items)


@cart.route('/add/<int:machine_id>', methods=['GET', 'POST'])
def add_product_to_cart(machine_id):
    machine = MachineService.get_machine(machine_id)
    form = forms.MachineFilterForm(request.form)

    if session['dateFrom'] == "" or session['dateTo'] == "":
        flash("Vyberte datum od a datum do")
        return redirect(url_for('machineoffer.show_machine_detail', machine_id=machine_id, form=form))

    for m in machine:
        if 'cart' not in session:
            session['cart'] = []
            session.permanent = True

        # check if dates are same as cart items dates
        if len(session['cart']) > 0:
            if session['cart'][0]['from'] != session['dateFrom'] or session['cart'][0]['to'] != session['dateTo']:
                session['dateFrom'] = session['cart'][0]['from']
                session['dateTo'] = session['cart'][0]['to']

                flash("V jedné objednávce musí být stejná data !")
                flash("Filtr byl nastaven na správné hodnoty")
                return redirect(url_for('machineoffer.view_machine_offer_page'))

        session['cart'].append(
            {"id": m['id'], "index": len(session['cart']), "from": session['dateFrom'], "to": session['dateTo'],
             "service": 1 if session['withService'] == "true" else 0})  # index for item deleting

        if 'auth' in session:
            OrderService.add_item(m['id'], session['uid'], session['dateFrom'], session['dateTo'],
                                  1 if session['withService'] == "true" else 0)

    return redirect(url_for('machineoffer.view_machine_offer_page'))


@cart.route('/add/service', methods=['POST'])
def add_service_to_cart():
    if request.method == 'POST':
        session['withService'] = request.form['with_service']

        if session['withService'] == "true" or session['withService'] == "false":
            return jsonify({'Success': 'Service option set'}), 200
        else:
            return jsonify({'error': 'Error with service option'}), 401


@cart.route('/update/service', methods=['POST'])
def update_cart_service():
    if request.method == 'POST':
        index = int(request.form['index'])
        session['withService'] = request.form['with_service']

        if session['withService'] == "true" or session['withService'] == "false":
            session['cart'][index].update({"service": 1 if session['withService'] == "true" else 0})
            if 'auth' in session:
                OrderService.update_item_service_by_index(session['uid'], index,
                                                          1 if session['withService'] == "true" else 0)
            session['withService'] = ""
            return jsonify({'Success': 'Service option set'}), 200
        else:
            return jsonify({'error': 'Error with service option'}), 401


@cart.route('/delete/<int:product_index>')
def delete_product(product_index):
    del session['cart'][product_index]
    # OrderService.delete_items(session['uid'])
    if 'auth' in session:
        OrderService.delete_item_by_index(session['uid'], product_index)

    # update item indexes
    for i in range(len(session['cart'])):
        session['cart'][i].update({"index": i})

    # for product in session['cart']:
    #     machine = MachineService.get_machine(product['id'])
    #     for m in machine:
    #         OrderService.add_item(m['id'], session['uid'])

    return redirect(url_for('cart.view_cart_page'))


@completeOrder.route('', methods=['POST', 'GET'])
@auth.login_required
@auth.cart_items_required
def view_complete_order_page():
    form = forms.CompleteOrderForm(request.form)

    if request.method == 'POST' and form.validate():
        address = form.street.data + " " + form.descriptive_number.data + ", " + form.zip_code.data[
                                                                                 0:3] + " " + form.zip_code.data[
                                                                                              3::] + " " + form.city.data
        ReservationService.create_order(session['cart'][0]['from'], session['cart'][0]['to'], address, session['uid'])
        order_id = ReservationService.get_user_last_order(session['uid'])
        for product in session['cart']:
            for o in order_id:
                ReservationService.add_machine_to_order(product['id'], o['id'], product["service"])

        OrderService.delete_cart_by_user(session['uid'])
        session['cart'] = []
        flash("Objednávka vytvořena")
        return redirect(url_for('machineoffer.view_machine_offer_page'))

    return render_template('orders/complete_order.jinja', form=form)


@orders.route('')
@auth.login_required
@auth.roles_required("Uživatel")
def view_orders_page():
    user_id = request.args.get('usid', None, int)
    if user_id == session["uid"]:
        my_orders = ReservationService.get_by_user_all(user_id)
        return render_template('orders/my_orders.jinja', my_orders=my_orders)
    else:
        flash("Nesprávný uživatel")
        return redirect(url_for('login.view_login_page'))


@workOrders.route('')
@auth.login_required
@auth.roles_required("Technik")
def view_work_orders_page():
    employee_id = request.args.get('emid', None, int)
    if employee_id == session["uid"]:
        work_orders = ReservationService.get_by_employee_all(employee_id)
        return render_template('orders/my_work_orders.jinja', work_orders=work_orders)
    else:
        flash("Nesprávný uživatel")
        return redirect(url_for('login.view_login_page'))


@orders.route('/order_details', methods=['POST', 'GET'])
@auth.login_required
def view_order_details_page():
    order_id = request.args.get('oid', None, int)
    user_id = request.args.get('usid', None, int)
    form = forms.AddEmployeeToOrderForm(request.form)
    employees = UserService.get_all_employees_by_role_id(3)
    form.employee_select.choices = [[type['id'], (type['name'] + "  " + type["last_name"])] for type in employees]

    if user_id == session["uid"]:
        order = ReservationService.get_by_order_id(order_id)
        order_machines = ReservationService.get_by_order_machine_id(order_id)
        if order is None:
            flash("Neexistující objednávka")
            return redirect(url_for('machineoffer.view_machine_offer_page'))
        if order["creator"] == session["uid"] or order["given_employee"] == session["uid"] or session["role"] == "Správce" or session["role"] == "Dispečer":
            sum_price = 0
            for mach in order_machines:
                sum_price = sum_price + mach["price_per_all_day"]
                if mach["salary_for_worker"] is not None:
                    sum_price = sum_price + mach["salary_for_worker"]
            if request.method == 'POST':
                if 'assign_technician' in request.form:
                    technician_id = int(form.employee_select.data)
                    OrderService.update_given_employee_on_order(technician_id, order_id)
                    flash('Technik byl přidělen k objednávce.')
                elif 'remove_technician' in request.form:
                    OrderService.update_given_employee_on_order(None, order_id)
                    flash('Technik byl odebrán z objednávky.')
                return redirect(url_for('orders.view_order_details_page', oid=order_id, usid=user_id))

            return render_template('orders/order_detail.jinja', order=order, order_machines=order_machines, form=form, sum_price=sum_price)
        else:
            flash("Nesprávný uživatel")
            return redirect(url_for('login.view_login_page'))
    else:
        flash("Nesprávný uživatel")
        return redirect(url_for('login.view_login_page'))

@orders.route("/update")
@auth.login_required
@auth.roles_required("Správce", "Dispečer")
def update_order_state():
    order_id = request.args.get('oid', None, int)
    state = request.args.get('st', None, int)
    ReservationService.update_order_state(order_id, state)
    return redirect(url_for('reservations.view_reservations_page'))