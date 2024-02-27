from flask import Flask, render_template

from database import database
from views.homepage import machineoffer
from views.login import register,login
from views.orders import cart,orders,completeOrder,workOrders
from views.reservations import reservations
from views.administration import administration
from views.profile import profile

# Zde budou importy service tříd, které budou sloužit pro komunikaci s DB
from service.reservation_service import ReservationService

app = Flask(__name__)
app.config['DEBUG'] = True
app.config.from_object('config')
database.init_app(app)

app.register_blueprint(machineoffer,url_prefix='/')
app.register_blueprint(login,url_prefix='/login')
app.register_blueprint(register,url_prefix='/register')
app.register_blueprint(orders,url_prefix='/orders')
app.register_blueprint(cart,url_prefix='/cart')
app.register_blueprint(completeOrder,url_prefix='/complete_order')
app.register_blueprint(workOrders,url_prefix='/work_orders')
app.register_blueprint(reservations,url_prefix='/reservations')
app.register_blueprint(administration,url_prefix='/administration')
app.register_blueprint(profile,url_prefix='/profile')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('notFound/index.jinja')

if __name__ == '__main__':
    app.run(debug=True)
