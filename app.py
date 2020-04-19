from flask import Flask, flash, render_template, request, redirect, url_for
from flask_login import current_user, LoginManager
from models import Schema, User
from services import ShoppingService
from config import config
import auth

app = Flask(__name__)
app.config.from_object(config['prod'])
app.register_blueprint(auth.bp)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


@app.before_request
def before_request():
    if not request.is_secure:
        return redirect(request.url.replace('http://', 'https://'))


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']= "POST, GET, PUT, DELETE, OPTIONS"
    return response


@login_manager.user_loader
def load_user(uid):
    user = User.get(uid)
    return user


def is_valid_quantity(quantity):
    is_int = True
    try:
        quantity = int(quantity)
        if quantity < 0:
            is_int = False
    except ValueError:
        is_int = False
    return is_int


@app.route('/', methods = ['GET','POST'])
def index():
    if current_user.is_authenticated:
        if request.method == 'POST':
            name, quantity = request.form['name'], request.form['quantity']
            if not name:
                flash("Please enter an item")
                return redirect(url_for('index'))
            else:
                if  quantity and not is_valid_quantity(quantity):
                    flash("Quantity is not valid. Please enter a number")
                    return redirect(url_for('index'))
                else:
                    if quantity == '':
                        quantity = 1
                    ShoppingService().create(name, quantity,current_user.id)
                    return redirect(url_for('index'))
        else:
            items = ShoppingService().list(current_user.id)
            return render_template('index.html',items=items, uname=current_user.name)
    else:
        return render_template('welcome.html')


@app.route("/delete/<item_id>", methods=["GET","DELETE"])
def delete_item(item_id):
    if current_user.is_authenticated:
        ShoppingService().delete(item_id, current_user.id)
        return redirect(url_for('index'))
    else:
        return render_template('welcome.html')


@app.route("/update/", methods=["GET","POST"])
def update_item():
    if current_user.is_authenticated:
        bought_items = request.form.getlist("bought")
        if not bought_items:
            flash("Please select the items you bought")
        ShoppingService().update(bought_items,current_user.id)
        return redirect(url_for('index'))
    else:
        render_template('welcome.html')


if __name__ == '__main__':
    Schema()
    app.run()
