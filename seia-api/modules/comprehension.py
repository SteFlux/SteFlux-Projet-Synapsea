def analyser(message):
    message = message.lower()
    if "bonjour" in message:
        return "salutation"
    elif "crée une page" in message:
        return "creation_page"
    else:
        return "inconnu"
