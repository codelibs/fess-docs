=====================================
HTTP-Sitzungen zwischen Knoten teilen
=====================================

Überblick
=========

Standardmäßig hält jeder |Fess|-Knoten seine HTTP-Sitzungen im eigenen Arbeitsspeicher. Wenn Sie mehrere |Fess|-Knoten hinter einem Load Balancer betreiben, setzen Sie auf jedem Knoten die Umgebungsvariable ``FESS_SESSION_STORE=opensearch``. Die Sitzungen werden dann im Index ``fess_config.session`` der Suchmaschine gespeichert, und ein Knoten kann eine Sitzung lesen, die ein anderer Knoten angelegt hat. Das umfasst den Anmeldestatus sowie das, was ein Passkey-Vorgang oder eine SSO-Anmeldung zwischen zwei Anfragen in der Sitzung hält (siehe :doc:`security-passkey` und :doc:`sso-saml`). Ohne Wert, mit leerem Wert oder mit ``memory`` bleiben die Sitzungen im Arbeitsspeicher des jeweiligen Knotens. Ein unbekannter Wert wird auf der Standardfehlerausgabe gemeldet und wie ``memory`` behandelt.

Zum Hinzufügen oder Entfernen eines SSO-Plugins, wodurch alle gespeicherten Sitzungen ungültig werden, siehe den Hinweis in :doc:`sso-saml`.

Voraussetzung bei mehreren Knoten
=================================

Richten Sie am Load Balancer auch bei geteilten Sitzungen Sticky Sessions (Client-Affinität) ein, sodass ein Client immer demselben Knoten zugewiesen wird.

Ein Knoten speichert eine Sitzung in der Suchmaschine, bevor er die Antwort sendet; im Normalbetrieb kann daher ein anderer Knoten die Sitzung lesen, sobald der Client die Antwort erhalten hat. Garantiert ist das jedoch nicht. Kann eine Sitzung nicht gespeichert werden, wird nur eine Warnung in das Log des Knotens geschrieben, und die Anfrage selbst wird weiterhin normal beantwortet. Außerdem findet eine Anfrage, die kurz nach dem Start eines Knotens zu einem anderen Knoten wechselt, die Sitzung möglicherweise nicht. In beiden Fällen kann ein Client, der seine nächste Anfrage sofort an einen anderen Knoten sendet, zum Beispiel direkt nach der Anmeldung, als nicht angemeldet behandelt werden und ``401`` erhalten. In Tests trat das gelegentlich bei Anfragen auf, die unmittelbar nach dem Start eines Knotens gesendet wurden, und nach dem Warmlaufen nicht mehr. Mit Sticky Sessions erreicht der Client stets den Knoten, der die Sitzung angelegt hat; die geteilten Sitzungen werden dann nur benötigt, um die Sitzung zu übernehmen, wenn dieser Knoten nicht mehr verfügbar ist.
