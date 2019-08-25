from jsonschema import ValidationError


def construct_dict(citizens):
    citizens_dict = dict()
    for citizen in citizens:
        citizens_dict[citizen['citizen_id']] = citizen['relatives']
    return citizens_dict


def check(citizens):
    citizens_dict = construct_dict(citizens)
    for citizen_id, relatives in citizens_dict.items():
        for relative_id in relatives:
            if citizen_id not in citizens_dict[relative_id] or citizen_id == relative_id:
                raise ValidationError("inconsistent data")
    return True
