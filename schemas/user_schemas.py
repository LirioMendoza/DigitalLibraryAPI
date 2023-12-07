from marshmallow import fields, validates, ValidationError
import re
class UserSchema:
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email =  fields.Email(required=True)
    password = fields.String(required=True)

    #validation for minimum username characters   
    @validates('username')
    def validateUsername(self, value):
        if len(value) < 5:
            raise ValidationError('User name must be at leat 5 characters long.')
    
    #validation for minimum first_name characters and special characters are not accepted
    @validates('first_name')
    def validateFirstName(self, value):
        if len(value) < 3:
            raise ValidationError('First name must be at leat 3 characters long.')
        if not re.match("^[a-zA-Z]+$", value):
            raise ValidationError('First name must contain only letters (no numbers or special characters).')
    
    #validation for minimum last_name characters and special characters are not accepted
    @validates('last_name')
    def validateLastName(self, value):
        if len(value) < 3:
            raise ValidationError('Last name must be at leat 3 characters long.')
        if not re.match("^[a-zA-Z]+$", value):
            raise ValidationError('Last name must contain only letters (no numbers or special characters).')
    
    #validation for minimum email characters
    @validates('email')
    def validateEmail(self, value):
        if len(value)<7:
             raise ValidationError('Email must be at leat 7 characters long.')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValidationError('Invalid email format.')
    
    #validation for minimum password characters   
    @validates('password')
    def validatePassword(self, value):
        if len(value)<6:
             raise ValidationError('Password must be at leat 6 characters long.')
        