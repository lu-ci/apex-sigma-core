import string


def clean_content(text):
    symbols = string.punctuation + string.whitespace
    out = ''
    for char in text:
        if char not in symbols:
            out += char
    return out
