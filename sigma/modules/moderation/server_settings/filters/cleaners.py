def clean_content(text):
    symbols = ['`', '"', '\'', '_', '-', '*', '~']
    out = text
    for symbol in symbols:
        out = out.replace(symbol, '')
    return out
