from flask import request, flash, redirect, url_for, render_template, Blueprint, session

import auth
import forms
from service.user_service import UserService

profile = Blueprint("profile", __name__)


@profile.route("", methods=['GET', 'POST'])
@auth.login_required
def view_profile_page():
    user_id = request.args.get('usid', None, int)
    form = forms.ProfileForm(request.form)
    user = UserService.get_user_by_id(user_id)
    if request.method == "POST" and form.validate():
        name = request.form["name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        # password = request.form["password"] TODO použít pro změnu hesla, nutnost zkontrolovat zda není stejný jak původní
        if (name != user["name"] or last_name != user["last_name"] or
                email != user["email"] or phone_number != user["phone_number"]):
            UserService.alter_profile_by_id(user_id, name, last_name, email, phone_number)
            user = UserService.get_user_by_id(user_id)  # Refresh user data after update

    if user and session["uid"] == user_id:
        return render_template("profile/profile.jinja", user=user, form=form)
    else:
        print("Pokus o přistup na špatný profil")
        flash("Pokus o přístup na špatný nebo neexistující profil.")
        return render_template("profile/profile.jinja", user=None)