from flask_app import app, bcrypt
from flask import render_template,redirect,request,session,flash
from flask_app.models.model_inquiries import Inquiry
from flask_app.models.model_email import Email
from flask_app.config.mysqlconnection import connectToMySQL

import smtplib
import os
from email.message import EmailMessage 

@app.route('/email/update')
def update_request():
    return render_template("update_email.html")

@app.route('/email/update/request', methods=['POST'])
def update_email():
    if not Email.validate_new_email(request.form):
        return redirect('/email/update')
    if not Email.validate_old_email(request.form):
        return redirect('/email/update')
    data = {**request.form}
    id = Email.update(data)
    session['id'] = id
    session['email'] = request.form['new_email']
    return redirect ('/update/confirm')

@app.route('/update/confirm')
def update_confirm():
    return render_template("update_email_confirm.html")

@app.route('/register/email', methods=['POST'])
def register_email():
    if not Email.validate_email(request.form):
        return redirect('/')
    data = {**request.form}
    id = Email.save(data)
    session['id'] = id
    session['email'] = request.form['email']

    USER_NAME = app.config['DB_USER']
    PASSWORD = app.config['DB_PASS']

    msg = EmailMessage()
    msg['subject'] = "Welcome to our Mailing List"
    msg['From'] = USER_NAME
    msg['To'] = data['email']
    msg.set_content('This is an email confirming that you have sucessfully join our mailing list.') 
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        
        smtp.login(USER_NAME,PASSWORD)
        smtp.send_message(msg)
    return redirect('/success/email')

@app.route('/success/email')
def success_email():
    return render_template("success.html")

@app.route('/email/delete/request')
def delete_request():
    return render_template("delete_email.html")

@app.route('/email/delete', methods=['POST'])
def delete_email():
    if not Email.validate_delete_email(request.form):
        return redirect('/email/delete/request')
    data = {
        **request.form
    }
    data['email'] = request.form['email']
    Email.destroy(data)

    USER_NAME = app.config['DB_USER']
    PASSWORD = app.config['DB_PASS']

    msg = EmailMessage()
    msg['subject'] = "Unsubscribe From Our Mailing List"
    msg['From'] = USER_NAME
    msg['To'] = data['email']
    msg.set_content('This is an email confirming that you have unsucessfully unsubscribed from our mailing list.') 
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        
        smtp.login(USER_NAME,PASSWORD)
        smtp.send_message(msg)
    return redirect('/unsubscribe')

@app.route('/unsubscribe')
def unsubscribe():
    return render_template("unsubscribe.html")