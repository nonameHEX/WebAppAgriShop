from flask import request, flash, redirect, url_for, render_template, Blueprint, session

import forms
from service.machine_service import MachineService
from service.order_service import OrderService
from service.user_service import UserService

login = Blueprint("login", __name__)
register = Blueprint("register", __name__)


@login.route('', methods=['GET', 'POST'])
def view_login_page():
    form = forms.LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = UserService.verify(request.form['username'], request.form['password'])
        if not user:
            print("Failed login")
            pass
        else:
            session['auth'] = 1
            session['uid'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session.permanent = True
            if 'cart' not in session:
                session['cart'] = []

            if 'dateFrom' not in session:
                session['dateFrom'] = ""

            if 'dateTo' not in session:
                session['dateTo'] = ""
            if 'withService' not in session:
                session['withService'] = ""

            # add new items to db
            for i in range(0, len(session['cart'])):
                OrderService.add_item(session['cart'][i]['id'], session['uid'], session['dateFrom'], session['dateTo'],
                                      1 if session['withService'] == "true" else 0)

            session['cart'] = []  # prevent wrong item order or item duplication

            user_items = OrderService.get_items_for_user(session['uid'])  # get updated items from db

            # get machine with item id
            for i in user_items:
                machine = MachineService.get_machine(i['item_id'])

                # add machine info to cart item list
                if machine is not None:
                    for m in machine:
                        session['cart'].append(
                            {"id": m['id'], "index": len(session['cart']), "from": i['date_to_delivery'],
                             "to": i['date_to_pickup'],
                             "service": i['with_service']})  # index for item deleting
            print(user['role'] + " Success login")
            return redirect(url_for('machineoffer.view_machine_offer_page'))

    return render_template('login/login.jinja', form=form)


@login.route('/signout')
def signout():
    session.pop("auth")
    session.pop("uid")
    session.pop("username")
    session.pop("role")
    session.pop("cart")
    session.pop("dateFrom")
    session.pop("dateTo")

    return redirect(url_for('machineoffer.view_machine_offer_page'))


@register.route('', methods=['GET', 'POST'])
def view_register_page():
    form = forms.RegisterForm(request.form)
    users = UserService.get_all()
    usernames = [user['username'] for user in users]
    emails = [user['email'] for user in users]

    session.pop('_flashes', None)  # clear flash messages (for redirect on low role)

    if request.method == 'POST' and form.validate():
        if request.form['username'] not in usernames and request.form['email'] not in emails:
            UserService.insert_user(username=request.form['username'], name=request.form['name'],
                                    last_name=request.form['last_name'], password=request.form['password'],
                                    email=request.form['email'])
            flash('Registrace úspěšná')
            return redirect(url_for('login.view_login_page'))
        else:
            if request.form['username'] in usernames:
                flash("Uživatelské jméno není dostupné")
            elif request.form['email'] in emails:
                flash("Email je používán")

    return render_template('login/register.jinja', form=form)
