import string


def clean_content(text):
    symbols = string.punctuation
    out = ''
    for char in text:
        if char not in symbols:
            out += char
    return out
