import secrets


def scramble(text):
    separated_text = text.split()
    chunks = []
    for word in separated_text:
        chunk = ''
        charlist = list(word)
        while charlist:
            chunk += charlist.pop(secrets.randbelow(len(charlist)))
        chunks.append(chunk)
    end_text = ' '.join(chunks)
    return end_text
