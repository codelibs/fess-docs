=====================================
HTTP-Sitzungen zwischen Knoten teilen
=====================================

Überblick
=========

Standardmäßig hält jeder |Fess|-Knoten seine HTTP-Sitzungen im eigenen Arbeitsspeicher. Wenn Sie mehrere |Fess|-Knoten hinter einem Load Balancer betreiben, setzen Sie auf jedem Knoten die Umgebungsvariable ``FESS_SESSION_STORE=opensearch``. Die Sitzungen werden dann im Index ``fess_config.session`` der Suchmaschine gespeichert, und ein Knoten kann eine Sitzung lesen, die ein anderer Knoten angelegt hat. Das umfasst den Anmeldestatus sowie das, was ein Passkey-Vorgang oder eine SSO-Anmeldung zwischen zwei Anfragen in der Sitzung hält (siehe :doc:`security-passkey` und :doc:`sso-saml`). Ohne Wert, mit leerem Wert oder mit ``memory`` bleiben die Sitzungen im Arbeitsspeicher des jeweiligen Knotens. Ein unbekannter Wert wird auf der Standardfehlerausgabe gemeldet und wie ``memory`` behandelt.

Zum Hinzufügen oder Entfernen eines SSO-Plugins, wodurch alle gespeicherten Sitzungen ungültig werden, siehe den Hinweis in :doc:`sso-saml`.

Speichern und Fehlerfälle
=========================

Ein Knoten speichert die Sitzungen, die eine Anfrage berührt hat, in der Suchmaschine, bevor er die Antwort sendet. Ein Client, der seine nächste Anfrage direkt nach der Antwort an einen anderen Knoten sendet, zum Beispiel direkt nach der Anmeldung, findet die Sitzung dort daher. Änderungen, die nach dem Beginn der Antwort erfolgen, werden am Ende der Anfrage gespeichert.

Kann die Suchmaschine nicht gelesen oder beschrieben werden, wird die Anfrage dennoch beantwortet, und im Log erscheint eine Warnung wie „Failed to save the session to the session store.“ oder „Failed to load the session from the session store. The session is kept in memory only.“ (höchstens einmal pro Minute). Der Knoten hält die Sitzung dann nur in seinem eigenen Arbeitsspeicher, und die anderen Knoten sehen sie nicht, bis sie wieder gespeichert werden kann. Kann eine Abmeldung die gespeicherte Sitzung nicht löschen, lehnt der Knoten diese Sitzung fortan ab, die anderen Knoten akzeptieren sie jedoch, bis sie abläuft.

Ohne ``FESS_SESSION_STORE`` hält jeder Knoten seine Sitzungen nur im eigenen Arbeitsspeicher, und ein Client, der an einen anderen Knoten geleitet wird, ist dort nicht angemeldet. Teilen Sie die Sitzungen wie oben beschrieben, oder lassen Sie den Load Balancer jeden Client immer demselben Knoten zuweisen.
