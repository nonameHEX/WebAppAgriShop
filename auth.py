from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from functools import wraps

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(session)
        if "auth" not in session:
            flash("Musíš být přihlášený, aby jsi sem mohl přistoupit")
            return redirect(url_for("login.view_login_page"))
        return func(*args, **kwargs)
    return decorated_function


def roles_required(*roles):
    def roles_decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if session['role'] not in roles:
                flash('Zde máš zakázaný přístup...')
                return redirect(url_for('login.view_login_page'))
            return func(*args, **kwargs)
        return decorated_function
    return roles_decorator

def cart_items_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "cart" not in session:
            return redirect(url_for('machineoffer.view_machine_offer_page'))
        elif len(session['cart']) == 0:
            return redirect(url_for('machineoffer.view_machine_offer_page'))
        return func(*args, **kwargs)
    return decorated_function