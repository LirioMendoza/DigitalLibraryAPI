from marshmallow import fields, validates, ValidationError

class ResourceSchema:
    title = fields.String(required=True)
    author = fields.String(required=True)
    description = fields.String(required=True)

    @validates('title')
    def validateTitle(self, value):
        if len(value) < 5:
            raise ValidationError('Title must be at leat 5 characters long.')
        
    @validates('author')
    def validateAuthor(self, value):
        if len(value) < 5:
            raise ValidationError('Author must be at leat 5 characters long.')

    @validates('description')
    def validateDescription(self, value):
        if len(value) < 5:
            raise ValidationError('Description must be at leat 5 characters long.')
