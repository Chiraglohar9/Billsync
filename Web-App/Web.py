import socket

from flask import Flask, render_template
from jinja2 import ChoiceLoader, FileSystemLoader

app = Flask(__name__)

app.jinja_env.loader = ChoiceLoader([
    FileSystemLoader("../Web-App")
])


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # Bind to any available port
        return s.getsockname()[1]


@app.route('/')
def login_page():
    return render_template('Templates/dashboard.html')


if __name__ == "__main__":
    free_port = find_free_port()
    app.run(host="127.0.0.1", port=free_port, debug=True)
