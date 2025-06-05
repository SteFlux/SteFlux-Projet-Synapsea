def executer(intention, etat):
    if intention == "salutation":
        return "👋 Bonjour, je suis SEIA !", etat

    if intention == "creation_page":
        try:
            with open("/var/www/seia.synapsea.dev/test_auto.html", "w") as f:
                f.write("<html><body><h1>Page générée par SEIA</h1></body></html>")
            return "✅ Page HTML créée avec succès.", etat
        except Exception as e:
            return f"❌ Erreur de création : {e}", etat

    return "🤖 SEIA n’a pas compris la demande.", etat
