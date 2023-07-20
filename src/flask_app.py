from flask import Flask, request

app = Flask(__name__)

@app.route("/hello_flask/")
def hello_flask() -> str:
    """A flask route."""
    name = request.args.get("name", "World!")
    return f"Hello, {name} from Flask!"
