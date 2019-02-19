def normalize_number(number):
    """Normalize a phone number str to format 18051234567"""
    strip_chars = '()-.+ '
    for char in strip_chars:
        number = number.replace(char, '')
    if len(number) == 10:
        number = "1{}".format(number)
    return number
