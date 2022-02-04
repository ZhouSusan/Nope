from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt, DATABASE
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Inquiry:
    def __init__( self , data ):
        self.id = data['id']
        self.email = data['email']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM inquiries WHERE email = %(email)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query= "SELECT * FROM inquiries;"
        results = connectToMySQL(DATABASE).query_db(query)
        emails = []
        for row in results:
            emails.append( cls(row) )
        return emails

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM inquiries WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO inquiries ( first_name, email, message ) VALUES ( %(first_name)s, %(email)s, %(message)s );"
        return connectToMySQL(DATABASE).query_db( query, data )

    @staticmethod
    def validate_form(inquiry):
        is_valid = True
        if len(inquiry['first_name']) < 3:
            flash("Name must be at least 3 characters.", "name_error")
            is_valid = False
        if len(inquiry['message']) < 3:
            flash("Message must be at least 5 characters.", "msg_error")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_email(email):
        is_valid = True
        if not EMAIL_REGEX.match(email['email']):
            flash("Invalid email!", 'email_error') 
            return False      
        return is_valid