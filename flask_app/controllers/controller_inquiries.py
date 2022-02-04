from flask_app import app, bcrypt
from flask import render_template,redirect,request,session,flash,url_for
from flask_app.models.model_inquiries import Inquiry
from flask_app.models.model_email import Email
from flask_app.config.mysqlconnection import connectToMySQL
import smtplib
import os
from email.message import EmailMessage 


@app.route('/inquiries/new',  methods=['POST'])
def new():
    if not Inquiry.validate_form(request.form):
        return redirect('/contact')
    if not Inquiry.validate_email(request.form):
        return redirect('/contact')
    id = Inquiry.save(request.form)
    session['first_name'] = request.form['first_name']
    name = session['first_name']
    USER_NAME = app.config['DB_USER']
    PASSWORD = app.config['DB_PASS']

    msg = EmailMessage()
    msg['subject'] = "We have recieve your message"
    msg['From'] = USER_NAME
    msg['To'] = request.form['email']
    msg.set_content('Thank you for contacting us. Your inquiry is very important to us. Some will contact you with in 48 hours. ') 
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        
        smtp.login(USER_NAME,PASSWORD)
        smtp.send_message(msg)
    return redirect(url_for('.success', name=name))

@app.route('/success')
def success():
    name = request.args['name']  # counterpart for url_for()
    return render_template("thank_you.html", name=name)
