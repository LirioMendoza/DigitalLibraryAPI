from marshmallow import fields, validates, ValidationError
import re
class CommentSchema:
    user_id = fields.Integer(required=True)
    user_name = fields.String(required=True)
    fist_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email =  fields.Email(required=True)

    @validates('user_id')
    def validateUserId(self, value):
        if value< 0:
            raise ValidationError('User ID must be a non-negative integer.')
        
    @validates('user_name')
    def validateUser_name(self, value):
        if len(value) < 5:
            raise ValidationError('Comments must be at leat 5 characters long.')

    @validates('first_name')
    def validateFirst_name(self, value):
        if len(value) < 3:
            raise ValidationError('First name must be at leat 3 characters long.')
        if not re.match("^[a-zA-Z]+$", value):
            raise ValidationError('First name must contain only letters (no numbers or special characters).')

    @validates('last_name')
    def validateLast_name(self, value):
        if len(value) < 3:
            raise ValidationError('Last name must be at leat 3 characters long.')
        if not re.match("^[a-zA-Z]+$", value):
            raise ValidationError('Last name must contain only letters (no numbers or special characters).')

    @validates('email')
    def validateEmail(self, value):
        if len(value)<7:
             raise ValidationError('Email must be at leat 7 characters long.')
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValidationError('Invalid email format.')
        
    @validates('password')
    def validatePassword(self, value):
        if len(value)<6:
             raise ValidationError('Password must be at leat 6 characters long.')
        