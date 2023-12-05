from marshmallow import fields, validates, ValidationError

class CommentSchema:
    title = fields.String(required=True)
    comment = fields.String(required=True)
    rating = fields.Integer(required=True)

    @validates('title')
    def validateTitle(self, value):
        if len(value) < 5:
            raise ValidationError('Title must be at leat 5 characters long.')
        
    @validates('comment')
    def validateComment(self, value):
        if len(value) < 5:
            raise ValidationError('Comments must be at leat 5 characters long.')

    @validates('rating')
    def validateRating(self, value):
        if value < 0 or value > 5:
            raise ValidationError('Rating must be between 1 to 5.')