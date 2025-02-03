from flask import Flask, render_template
from jinja2 import ChoiceLoader, FileSystemLoader
import json

app = Flask(__name__)

app.jinja_env.loader = ChoiceLoader([
    FileSystemLoader("Landing-Page"),
    FileSystemLoader("Web-App"),
])


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/', methods=['GET', 'POST'])
def login_page():
    return render_template('Templates/dashboard.html')


@app.route('/login', methods=['GET', 'POST'])
def test_page():
    return render_template('Templates/login.html')


@app.route('/index', methods=['GET', 'POST'])
def index_page():
    return render_template('Templates/index.html')


@app.route('/demo', methods=['GET', 'POST'])
def demo_page():
    return render_template('Templates/demo.html')


@app.route('/create', methods=['GET', 'POST'])
def create_page():
    return render_template('Templates/create.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard_page():
    return render_template('Templates/dashboard.html')


@app.route('/invoices', methods=['GET', 'POST'])
def invoices_page():
    return render_template('Templates/invoices.html')


@app.route('/transactions', methods=['GET', 'POST'])
def transaction_page():
    return render_template('Templates/transactions.html')


@app.route('/customers', methods=['GET', 'POST'])
def customers_page():
    return render_template('Templates/customers.html')


@app.route('/products')
def products_page():
    return render_template('Templates/products.html')


@app.route('/accounts')
def accounts_page():
    return render_template('Templates/accounts.html')


@app.route('/reports')
def reports_page():
    return render_template('Templates/reports.html')


@app.route('/settings')
def settings_page():
    return render_template('Templates/settings.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5003, debug=True)
