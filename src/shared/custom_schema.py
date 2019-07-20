from marshmallow import Schema, validates_schema, ValidationError

class CustomSchema(Schema):
    @validates_schema(pass_original=True)
    def check_unknown_fields(self, data, original_data):
        validate_data = original_data if data == {} else data
        unknown = set(validate_data) - set(self.fields)
        if unknown:
            raise ValidationError('Unknown field', unknown)