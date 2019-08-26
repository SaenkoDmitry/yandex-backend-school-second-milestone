import datetime

from jsonschema import FormatChecker, ValidationError

format_checker = FormatChecker()


@format_checker.checks('simple_date')
def simple_date(date_text):
    try:
        from_json_date = datetime.datetime.strptime(date_text, '%d.%m.%Y')
        now = datetime.datetime.now()
        if from_json_date > now:
            raise ValueError
        return from_json_date
    except ValueError:
        raise ValidationError("Incorrect date, should be DD-MM-YYYY and go before current date")
