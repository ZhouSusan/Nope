from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.controllers import controller_route, controller_inquiries, controller_email

if __name__ == "__main__":
    app.run(debug=True)