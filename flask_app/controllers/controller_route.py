from flask_app import app, bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.model_inquiries import Inquiry
from flask_app.models.model_email import Email
from flask_app.config.mysqlconnection import connectToMySQL


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/berserker')
def display_berzerker():
    return render_template("berzerker.html")

@app.route('/bombmancer')
def display_bombmancer():
    return render_template("bombmancer.html")

@app.route('/mage')
def display_mage():
    return render_template("mage.html")

@app.route('/nature')
def display_nature():
    return render_template("nature.html")

@app.route('/paladin')
def display_paladin():
    return render_template("paladin.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

    