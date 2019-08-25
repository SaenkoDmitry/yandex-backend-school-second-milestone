import datetime

from jsonschema import FormatChecker, ValidationError

format_checker = FormatChecker()


@format_checker.checks('simple_date')
def simple_date(date_text):
    try:
        return datetime.datetime.strptime(date_text, '%d.%m.%Y')
    except ValueError:
        raise ValidationError("Incorrect data format, should be DD-MM-YYYY")
