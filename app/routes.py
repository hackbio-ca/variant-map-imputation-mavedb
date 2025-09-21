from flask import Blueprint

# Create a blueprint named 'main'
main = Blueprint("main", __name__)

@main.route("/")
def home():
    return "Hello, Flask is working with a blueprint!"

@main.route("/test")
def test():
    return "Test route works!"
    