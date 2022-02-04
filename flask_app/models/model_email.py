from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt, DATABASE
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Email:
    def __init__( self , data ):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM emails WHERE email = %(email)s"
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query= "SELECT * FROM emails;"
        results = connectToMySQL(DATABASE).query_db(query)
        emails = []
        for row in results:
            emails.append( cls(row) )
        return emails

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM emails WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0])

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO emails ( email ) VALUES ( %(email)s );"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def update(cls, data):
        query = "Update emails SET email = %(new_email)s WHERE email = %(email)s;"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM emails WHERE email = %(email)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod
    def validate_email(email):
        is_valid = True
        if not EMAIL_REGEX.match(email['email']):
            flash("Invalid email!", 'invalid_email_error') 
            return False      
        query = "SELECT * FROM emails WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,email)
        if results != False and len(results) != 0:
            flash("Emails already taken.", 'duplicate_email_error')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_new_email(email):
        is_valid = True
        if not EMAIL_REGEX.match(email['new_email']):
            flash("Invalid email!", 'invalid_new_email_error') 
            return False      
        query = "SELECT * FROM emails WHERE email = %(new_email)s;"
        results = connectToMySQL(DATABASE).query_db(query,email)
        if results != False and len(results) != 0:
            flash("Emails already taken.", 'duplicate_new_email_error')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_old_email(email):
        is_valid = True
        if not EMAIL_REGEX.match(email['email']):
            flash("Invalid email!", 'invalid_old_email_error') 
            return False
        return is_valid

    @staticmethod
    def validate_delete_email(email):
        is_valid = True
        if not EMAIL_REGEX.match(email['email']):
            flash("Invalid email!", 'invalid_delete_email_error') 
            return False
        return is_valid
    