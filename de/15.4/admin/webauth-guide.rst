==================
Web-Authentifizierung
==================

Übersicht
=========

Hier wird die Konfigurationsmethode erläutert, wenn Web-Authentifizierung für das Crawlen von Webs erforderlich ist.
|Fess| unterstützt das Crawlen mit BASIC-, DIGEST- und NTLM-Authentifizierung.

Verwaltung
==========

Anzeige
-------

Um die Web-Authentifizierungs-Konfigurationsübersichtsseite zu öffnen, klicken Sie im linken Menü auf [Crawler > Web-Authentifizierung].

|image0|

Klicken Sie auf den Konfigurationsnamen, um ihn zu bearbeiten.

Konfiguration erstellen
-----------------------

Um die Web-Authentifizierungskonfigurationsseite zu öffnen, klicken Sie auf die Schaltfläche „Neu erstellen".

|image1|

Konfigurationsparameter
-----------------------

Hostname
::::::::

Geben Sie den Hostnamen der Site an, die Authentifizierung erfordert.
Wenn weggelassen, wird dies auf jeden Hostnamen in der angegebenen Web-Crawl-Konfiguration angewendet.

Port
::::

Geben Sie den Port der Site an, die Authentifizierung erfordert.
Um dies auf alle Ports anzuwenden, geben Sie -1 an.
In diesem Fall wird dies auf jeden Port in der angegebenen Web-Crawl-Konfiguration angewendet.

Realm
:::::

Geben Sie den Realm-Namen der Site an, die Authentifizierung erfordert.
Wenn weggelassen, wird dies auf jeden Realm-Namen in der angegebenen Web-Crawl-Konfiguration angewendet.

Schema
::::::

Wählen Sie die Authentifizierungsmethode aus.
Sie können BASIC-, DIGEST-, NTLM- oder FORM-Authentifizierung verwenden.

Benutzername
::::::::::::

Geben Sie den Benutzernamen für die Anmeldung bei der Authentifizierungssite an.

Passwort
::::::::

Geben Sie das Passwort für die Anmeldung bei der Authentifizierungssite an.

Parameter
:::::::::

Konfigurieren Sie dies, wenn Konfigurationswerte für die Anmeldung bei der Authentifizierungssite erforderlich sind.
Für NTLM-Authentifizierung können Sie die Werte für Workstation und Domäne konfigurieren.
Geben Sie sie wie folgt an:

::

    workstation=HOGE
    domain=FUGA

Web-Konfiguration
:::::::::::::::::

Wählen Sie den Web-Konfigurationsnamen aus, auf den die oben genannte Authentifizierungskonfiguration angewendet werden soll.
Sie müssen die Web-Crawl-Konfiguration im Voraus registrieren.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

.. |image0| image:: ../../../resources/images/en/15.4/admin/webauth-1.png
.. |image1| image:: ../../../resources/images/en/15.4/admin/webauth-2.png
