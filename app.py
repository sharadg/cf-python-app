from flask import Flask, jsonify, render_template, url_for
import os
from rpc_client import FibonacciRPCClient

app = Flask(__name__)

fibonacci_rpc = FibonacciRPCClient()

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", title="Title Passed", text=["apple", "orange", "lemon"])


@app.route("/fib/<number>")
def fibonacci(number):
    resp = fibonacci_rpc.call(int(number))
    return jsonify(resp)

@app.route("/info")
def env_info():
    dict_env = {k:v for k,v in os.environ.items()}
    return jsonify(dict_env)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
