==================
Web-Authentifizierung
==================

Übersicht
=========

Hier wird die Konfigurationsmethode erläutert, wenn Web-Authentifizierung für das Crawlen von Webs erforderlich ist.
|Fess| unterstützt das Crawlen mit BASIC-, DIGEST-, NTLM- und FORM-Authentifizierung.

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

.. warning::

   Wird der Hostname weggelassen, werden Benutzername und Passwort auch an andere Hosts gesendet, die der Crawl über Links oder Weiterleitungen erreicht.
   Geben Sie den Hostnamen an, damit die Zugangsdaten nicht an unbeabsichtigte Hosts gesendet werden.

Port
::::

Geben Sie den Port der Site an, die Authentifizierung erfordert.
Um dies auf alle Ports anzuwenden, lassen Sie das Feld leer. ``-1`` kann nicht angegeben werden; zulässig sind nur Werte ab 0.
In diesem Fall wird dies auf jeden Port in der angegebenen Web-Crawl-Konfiguration angewendet.

Realm
:::::

Geben Sie den Realm-Namen der Site an, die Authentifizierung erfordert.
Wenn weggelassen, wird dies auf jeden Realm-Namen in der angegebenen Web-Crawl-Konfiguration angewendet.
Bei der BASIC- und DIGEST-Authentifizierung wird der Realm unter Beachtung der Groß-/Kleinschreibung mit dem vom Server zurückgegebenen Realm verglichen. Stimmen sie nicht überein, werden die Zugangsdaten nicht gesendet.
Eine NTLM-Challenge enthält keinen Realm, daher wird diese Angabe bei der NTLM-Authentifizierung nicht verwendet (die Authentifizierung gelingt auch mit einem falschen Realm).

Schema
::::::

Wählen Sie die Authentifizierungsmethode aus.
Sie können BASIC-, DIGEST-, NTLM- oder FORM-Authentifizierung verwenden.

.. note::

   Das Schema BASIC, DIGEST oder NTLM schränkt nicht ein, welches Verfahren der Server anfordern darf.
   |Fess| sendet die Zugangsdaten mit dem Verfahren, das der Server anfordert.
   Ein als DIGEST gespeicherter Eintrag wird beispielsweise per BASIC gesendet, wenn der Server nur BASIC anfordert (über HTTP liegen die Zugangsdaten dann praktisch im Klartext vor).
   Ein als BASIC gespeicherter Eintrag antwortet mit DIGEST, wenn der Server DIGEST anfordert.
   NTLM und BASIC/DIGEST sind nicht gegeneinander austauschbar.
   Wählen Sie ein Schema, das der Server nicht verwendet, werden keine Zugangsdaten gesendet und die Dokumente der Site nicht indexiert.
   Wählen Sie das vom Server verwendete Verfahren und verwenden Sie nach Möglichkeit HTTPS.

Benutzername
::::::::::::

Geben Sie den Benutzernamen für die Anmeldung bei der Authentifizierungssite an.
Wenn die NTLM-Authentifizierung eine Domäne erfordert, schreiben Sie den Benutzernamen nicht als ``DOMAIN\Benutzer``, sondern geben Sie die Domäne im unten beschriebenen Parameter ``domain`` an.
Ein Wert wie ``DOMAIN\Benutzer`` wird nicht aufgeteilt: Die gesamte Zeichenfolge wird als Benutzername mit leerer Domäne gesendet.

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

``domain``
    Die Domäne, in der authentifiziert wird. Geben Sie sie an, wenn Sie sich mit einem Domänenkonto authentifizieren.
    Ohne Angabe wird die Domäne leer gesendet, und die Authentifizierung eines Domänenkontos schlägt fehl.
    Eine in Kleinbuchstaben angegebene Domäne wird vor dem Senden in Großbuchstaben umgewandelt.

``workstation``
    Der Workstation-Name, der in den NTLM-Nachrichten gesendet wird.
    Ohne Angabe wird der Hostname des Rechners gesendet, auf dem |Fess| läuft.

Web-Konfiguration
:::::::::::::::::

Wählen Sie den Web-Konfigurationsnamen aus, auf den die oben genannte Authentifizierungskonfiguration angewendet werden soll.
Sie müssen die Web-Crawl-Konfiguration im Voraus registrieren.

Wenn die Authentifizierung fehlschlägt
--------------------------------------

Sind die Zugangsdaten falsch, oder stimmen Hostname, Port oder Realm nicht mit der Site überein, sodass keine Zugangsdaten gesendet werden, antwortet der Server mit 401 (Unauthorized), und die Dokumente der Site werden nicht indexiert.
Ein 401 wird als Fehler-URL erfasst; prüfen Sie es unter :doc:`failureurl-guide`.
Die HTTP-Statuscodes, die als Fehler-URL erfasst werden, lassen sich mit ``crawler.failure.url.status.codes`` ändern (:doc:`../config/crawler-advanced`).
Ein 401 löscht bereits indexierte Dokumente nicht.

Konfiguration löschen
---------------------

Klicken Sie auf den Konfigurationsnamen auf der Übersichtsseite und dann auf die Schaltfläche „Löschen". Es wird ein Bestätigungsbildschirm angezeigt.
Klicken Sie auf die Schaltfläche „Löschen", um die Konfiguration zu löschen.

.. |image0| image:: ../../../resources/images/en/15.10/admin/webauth-1.png
.. |image1| image:: ../../../resources/images/en/15.10/admin/webauth-2.png
