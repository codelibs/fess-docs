==================================
Rate-Limiting-Konfiguration
==================================

Übersicht
==========

|Fess| enthält Rate-Limiting-Funktionen zur Aufrechterhaltung der Systemstabilität und Leistung.
Diese Funktionen schützen das System vor übermäßigen Anfragen und ermöglichen eine faire Ressourcenzuteilung.

Rate-Limiting wird in folgenden Szenarien angewendet:

- Alle HTTP-Anfragen einschließlich Such-API und AI-Suchmodus-API (``RateLimitFilter``)
- Crawler-Anfragen (Steuerung über Crawl-Konfiguration)

HTTP-Anfrage-Ratenbegrenzung
============================

Sie können die Anzahl der HTTP-Anfragen an |Fess| pro IP-Adresse begrenzen.
Diese Begrenzung gilt für alle HTTP-Anfragen einschließlich Such-API, AI-Suchmodus-API, Admin-Seiten usw.

Konfiguration
-------------

``app/WEB-INF/classes/fess_config.properties``:

::

    # Rate-Limiting aktivieren (Standard: false)
    rate.limit.enabled=true

    # Maximale Anfragen pro Fenster (Standard: 100)
    rate.limit.requests.per.window=100

    # Fenstergroesse (Millisekunden) (Standard: 60000)
    rate.limit.window.ms=60000

Verhalten
---------

- Anfragen, die das Rate-Limit überschreiten, geben HTTP 429 (Too Many Requests) zurück
- Anfragen von IPs, die wegen Überschreitung des Limits blockiert sind, sowie von IPs auf der Blockliste geben HTTP 403 (Forbidden) zurück
- Der Antwort-Body ist JSON (``{"error":"rate_limit_exceeded",...,"retry_after":60}`` bei 429, ``{"error":"ip_blocked",...}`` bei 403). Eine 429-Antwort hat einen ``Retry-After``-Header
- Limits werden pro IP-Adresse angewendet
- Pro IP-Adresse beginnt das Fenster mit der ersten Anfrage; nach Ablauf der Fensterperiode wird der Zähler zurückgesetzt (Festes-Fenster-Verfahren)
- Bei Überschreitung wird die IP für die Dauer von ``rate.limit.block.duration.ms`` blockiert

AI-Suchmodus Rate-Limiting
======================

Die AI-Suchmodus-Funktionalität verfügt über Rate-Limiting zur Kontrolle von LLM-API-Kosten und Ressourcenverbrauch.
Für den AI-Suchmodus gilt zusätzlich zur oben beschriebenen HTTP-Anfrage-Ratenbegrenzung eine eigene, AI-Suchmodus-spezifische Ratenbegrenzung.

AI-Suchmodus-spezifische Rate-Limiting-Einstellungen finden Sie unter :doc:`rag-chat`.

.. note::
   Das AI-Suchmodus-Rate-Limiting wird separat vom Rate-Limiting des LLM-Anbieters angewendet.
   Konfigurieren Sie beide Limits entsprechend.

Crawler Rate-Limiting
=====================

Sie können Anfrage-Intervalle konfigurieren, um zu verhindern, dass der Crawler Zielseiten überlastet.

Web-Crawl-Konfiguration
-----------------------

Konfigurieren Sie Folgendes im Admin-Panel unter "Crawler" -> "Web":

- **Anfrage-Intervall**: Wartezeit zwischen Anfragen (Millisekunden)
- **Thread-Anzahl**: Anzahl paralleler Crawling-Threads

Empfohlene Einstellungen:

::

    # Allgemeine Seiten
    intervalTime=1000
    numOfThread=1

    # Große Seiten (mit Genehmigung)
    intervalTime=500
    numOfThread=3

Beachtung von robots.txt
------------------------

|Fess| beachtet die Crawl-delay-Direktive in robots.txt standardmäßig.

::

    # robots.txt Beispiel
    User-agent: *
    Crawl-delay: 10

Die robots.txt-Verarbeitung wird über ``crawler.ignore.robots.txt`` in
``app/WEB-INF/classes/fess_config.properties`` gesteuert (Standard: ``false``).
Bei Setzen auf ``true`` wird die robots.txt-Verarbeitung einschließlich Crawl-delay deaktiviert.

::

    # robots.txt ignorieren (Standard: false)
    crawler.ignore.robots.txt=false

Crawl-delay gilt je Origin und ist auf 60 Sekunden begrenzt. Es taktet URLs, nicht Anfragen; bei
einem inkrementellen Crawl werden HEAD und GET einer URL daher direkt nacheinander gesendet. Das
Intervall einer Crawl-Konfiguration wirkt weiterhin getrennt davon als Wartezeit vor der nächsten URL.

robots.txt wird gemäß RFC 9309 ausgewertet. Zwischen ``Allow:`` und ``Disallow:`` gewinnt die längste
passende Regel, und auch die Start-URLs werden gegen robots.txt geprüft. Eine von robots.txt
verbotene URL wird in ``fess-crawler.log`` auf INFO protokolliert und nicht als Fehler-URL erfasst.

Request-rate
------------

Ab 15.10 beachtet |Fess| auch die Zeilen ``Request-rate`` und ``Visit-time`` in robots.txt (bis 15.9 wurden sie ignoriert). Beide sind nicht Teil von RFC 9309, sondern stammen aus dem `erweiterten Robots-Exclusion-Vorschlag <https://www.conman.org/people/spc/robots2.html>`__. SeznamBot verwendet ebenfalls Request-rate (`Dokumentation von Seznam <https://www.napoveda.seznam.cz/en/crawling-control>`__). Wie Crawl-delay gelten sie nur, solange die robots.txt-Verarbeitung aktiv ist: ``crawler.ignore.robots.txt=true`` schaltet alle drei ab, eine Einstellung für nur eine davon gibt es nicht. Sie sind keine ``Allow:``- oder ``Disallow:``-Regeln: Sie beenden nie eine ``User-agent``-Gruppe und ändern nie, welche URLs verboten sind.

``Request-rate: <Dokumente>/<Zeit>[ Einheit]`` bittet einen Crawler, in dieser Zeit höchstens so viele Dokumente abzurufen. Die Einheit der Zeit ist ``s`` (Sekunden, Standard), ``m``, ``h`` oder ``d``. Beispiele:

- ``1/10``: eine Seite pro 10 Sekunden
- ``10/10m``: zehn Seiten pro 10 Minuten
- ``20/1h``: zwanzig Seiten pro Stunde
- ``100/15 m``: hundert Seiten pro 15 Minuten

|Fess| rechnet die Rate in den Abstand zwischen zwei URLs um (``1/10`` sind 10 Sekunden, ``5/1m`` sind 12 Sekunden) und wartet je Origin vor der nächsten URL so lange wie der größere der beiden Abstände aus Crawl-delay und Request-rate. Die Obergrenze von 60 Sekunden gilt auch für diese Wartezeit; eine langsamere Rate wie ``1/1h`` wird auf 60 Sekunden begrenzt. Request-rate taktet URLs und ist kein Kontingent für einen Schwall von Anfragen. Wie bei Crawl-delay wird die erste URL eines Origin nicht getaktet, weil robots.txt beim Abruf dieser URL gelesen wird, und bei einem inkrementellen Crawl werden HEAD und GET einer URL direkt nacheinander gesendet.

Hinter der Rate kann eine Tageszeit stehen. Die Rate gilt dann nur in dieser Tageszeit; außerhalb davon setzt Request-rate keine Grenze (Crawl-delay gilt weiterhin):

::

    User-agent: *
    Request-rate: 1/10 s 1800-1900

Zeiten sind UT/GMT (UTC) von 00:00 bis 23:59, geschrieben als ``HHMM-HHMM`` oder ``HH:MM-HH:MM``; beide Enden sind eingeschlossen. Ein Bereich darf über Mitternacht gehen (``2300-0100``). Stehen mehrere Request-rate-Zeilen in der Datei, werden alle beachtet, und es gilt die langsamste, die gerade aktiv ist. Eine fehlerhafte Rate oder Tageszeit (zum Beispiel eine Stunde über 23 oder eine Minute über 59) wird ignoriert.

Visit-time
----------

``Visit-time: HH:MM-HH:MM`` (auch ``HHMM-HHMM``) bittet einen Crawler, die Website nur in dieser Tageszeit zu besuchen, in UTC und einschließlich beider Enden. Mehrere Zeilen sind erlaubt; zulässig ist dann die Vereinigung aller Zeiten.

::

    User-agent: *
    Visit-time: 02:00-06:00

|Fess| wartet nicht, bis das Zeitfenster beginnt, denn das würde einen Crawl-Thread stundenlang blockieren. Eine URL dieses Origin, die außerhalb des Fensters aus der Warteschlange genommen wird, wird übersprungen wie eine mit ``Disallow:`` verbotene URL: Sie wird je Origin einmal auf INFO protokolliert, nicht wieder in die Warteschlange gestellt (im selben Crawl also nicht später erneut versucht) und nicht als Fehler gezählt. Der Crawl muss daher innerhalb des Fensters beginnen. Eine Start-URL, die vor Beginn des Fensters aus der Warteschlange genommen wird, geht für diesen Crawl verloren, auch wenn der Crawl noch läuft, wenn das Fenster beginnt. Eine fehlerhafte Visit-time-Zeile wird ignoriert, es gibt dann keine Einschränkung.

Läuft der Crawl-Job einer Website, die Visit-time angibt, nie innerhalb des Fensters, wird die Website nicht gecrawlt und ihre indexierten Dokumente werden nicht aktualisiert. Mit der Standardeinstellung „Alte Dokumente löschen“ (``day.for.cleanup``, 3 Tage) laufen sie etwa 3 Tage nach dem letzten Crawl ab, der sie erreicht hat, genau wie bei einer nicht erreichbaren Website. Planen Sie den Crawl-Job innerhalb des Fensters.

Backoff nach 429/503-Antworten
------------------------------

Antwortet ein Server mit ``429 Too Many Requests`` oder ``503 Service Unavailable``, pausiert |Fess|
die Anfragen an diesen Origin und wiederholt die URL bis zu dreimal. Gewartet wird gemäß dem
``Retry-After``-Header, falls vorhanden, sonst exponentiell ab 10 Sekunden (höchstens 5 Minuten).
Schlägt auch der letzte Versuch fehl, wird ein WARN in ``fess-crawler.log`` geschrieben.

Wenn robots.txt nicht abgerufen werden kann
-------------------------------------------

Schlägt der Abruf von robots.txt mit 5xx, 429 oder einer Zeitüberschreitung fehl, werden die URLs
dieses Origins bis zum Ende des Backoffs wieder in die Warteschlange gestellt. Scheitern nach dem
ersten Fehler auch drei weitere Versuche, wird für den Rest des Crawls keine URL dieses Origins
gecrawlt, und ein einzelnes WARN wird in ``fess-crawler.log`` geschrieben. Bis 15.8 bedeutete eine
nicht abrufbare robots.txt „alles erlaubt“. Um dieses Verhalten wiederherzustellen, geben Sie in den
„Konfigurationsparametern“ der Web-Crawl-Konfiguration Folgendes an:

::

    client.robotsTxtAllowOnUnavailable=true

Um die robots.txt-Verarbeitung ganz abzuschalten, verwenden Sie ``client.robotsTxtEnabled=false``
(je Crawl-Konfiguration) oder ``crawler.ignore.robots.txt=true``.

Alle Rate-Limiting-Einstellungen
=================================

Alle in ``app/WEB-INF/classes/fess_config.properties`` konfigurierbaren Eigenschaften.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Eigenschaft
     - Beschreibung
     - Standard
   * - ``rate.limit.enabled``
     - Rate-Limiting aktivieren
     - ``false``
   * - ``rate.limit.requests.per.window``
     - Maximale Anfragen pro Fenster
     - ``100``
   * - ``rate.limit.window.ms``
     - Fenstergroesse (Millisekunden)
     - ``60000``
   * - ``rate.limit.block.duration.ms``
     - IP-Blockierungsdauer bei Überschreitung (Millisekunden)
     - ``300000``
   * - ``rate.limit.retry.after.seconds``
     - Retry-After-Header-Wert (Sekunden)
     - ``60``
   * - ``rate.limit.whitelist.ips``
     - Vom Rate-Limiting ausgeschlossene IP-Adressen (kommagetrennt)
     - ``127.0.0.1,::1``
   * - ``rate.limit.blocked.ips``
     - Blockierte IP-Adressen (kommagetrennt)
     - (leer)
   * - ``rate.limit.trusted.proxies``
     - Vertrauenswürdige Proxy-IPs (für X-Forwarded-For/X-Real-IP; auch für die Client-IP im Audit-Protokoll und im Suchprotokoll)
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - Bereinigungsintervall (Anfragenzahl, reserviert)
     - ``1000``

.. note::
   ``rate.limit.cleanup.interval`` ist eine für zukünftige Erweiterungen reservierte Einstellung.
   In der aktuellen Implementierung werden die Anfragezähler und die Informationen zu blockierten IPs
   automatisch auf Basis des internen Cache-Ablaufs (``rate.limit.window.ms`` und
   ``rate.limit.block.duration.ms``) bereinigt, sodass dieser Wert nicht verwendet wird.

Begrenzung der Anmeldeversuche
==============================

Für die Anmeldung gibt es eine eigene Begrenzung, die unabhängig von der obigen ist und mit ``theme.api.login.*`` konfiguriert wird.
Ab 15.10 teilen sich ``/api/v2/auth/login`` und das Anmeldeformular der Anmeldeseite (``/login/``) dieselbe Begrenzung und Sperrung.
Jeder Versuch verbraucht einen Platz im Minutenkontingent der Client-IP (Standardwert ``10``); bei erfolgreicher Anmeldung wird der Platz zurückgegeben.
Überschreiten die Versuche von derselben IP-Adresse das Limit, wird diese IP-Adresse für ``theme.api.login.lockout.seconds`` (Standardwert ``900``) Sekunden gesperrt, und in dieser Zeit ist auch mit korrekten Zugangsdaten keine Anmeldung möglich.
Kommen daher von derselben IP-Adresse mehr Versuche als erlaubt (etwa gleichzeitige Anmeldungen), bevor einer erfolgreich ist, wird diese Adresse gesperrt.
Das Limit pro Benutzer (``theme.api.login.rate.limit.per.user.per.minute``) wird für jede Kombination aus Client-IP-Adresse und Benutzername gezählt. Die Groß- und Kleinschreibung des Benutzernamens wird nicht beachtet; ``alice`` und ``Alice`` teilen sich also einen Zähler. Der Benutzername, der für die Authentifizierung verwendet und in die Protokolle geschrieben wird, bleibt so, wie er eingegeben wurde.
Einzelheiten finden Sie unter :doc:`../api/api-auth`.

Erweiterte Rate-Limiting-Konfiguration
======================================

Benutzerdefiniertes Rate-Limiting
---------------------------------

Um verschiedene Rate-Limiting-Logik basierend auf bestimmten Bedingungen anzuwenden,
ist eine benutzerdefinierte Komponentenimplementierung erforderlich.

::

    // Beispiel für benutzerdefinierten RateLimitHelper
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean allowRequest(String ip) {
            // Benutzerdefinierte Logik
        }
    }

Ausschluss-Einstellungen
========================

Sie können bestimmte IP-Adressen vom Rate-Limiting ausschließen oder blockieren.

::

    # Whitelist-IPs (vom Rate-Limiting ausgeschlossen, kommagetrennt)
    rate.limit.whitelist.ips=127.0.0.1,::1,192.168.1.100

    # Blockierte IPs (immer blockiert, kommagetrennt)
    rate.limit.blocked.ips=203.0.113.50

    # Vertrauenswürdige Proxy-IPs (kommagetrennt)
    rate.limit.trusted.proxies=127.0.0.1,::1

.. note::
   Bei Verwendung eines Reverse-Proxys setzen Sie ``rate.limit.trusted.proxies`` auf
   die IP-Adresse des Proxys. Nur bei Anfragen von vertrauenswürdigen Proxys wird die
   Client-IP aus den X-Forwarded-For- und X-Real-IP-Headern ermittelt.
   Ist X-Forwarded-For auf mehrere Header-Zeilen verteilt (zum Beispiel, wenn ein Proxy eine eigene
   Zeile hinzufügt, wie es ``option forwardfor`` von HAProxy tut), verbindet 15.10 und neuer alle Zeilen
   in der empfangenen Reihenfolge, liest die Kette von rechts und verwendet die erste Adresse, die kein
   vertrauenswürdiger Proxy ist, als Client-IP. Bis 15.9 wurde nur die erste Zeile gelesen, also die vom
   Client gesendete.

Überwachung und Warnungen
==========================

Konfiguration zur Überwachung des Rate-Limiting-Status:

Protokollausgabe
----------------

Wenn Rate-Limiting angewendet wird, wird es in den Protokollen aufgezeichnet:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

Die Meldung steht auf INFO-Ebene und wird bei der Standard-Protokollstufe (``warn``) daher nicht geschrieben. Fügen Sie den obigen ``Logger`` in ``log4j2.xml`` ein (Speicherort siehe :doc:`admin-logging`) oder setzen Sie ``FESS_LOG_LEVEL`` auf ``info``.

Fehlerbehebung
==============

Legitime Anfragen werden blockiert
----------------------------------

**Ursache**: Grenzwerte sind zu streng

**Lösungen**:

1. ``rate.limit.requests.per.window`` erhöhen
2. Bestimmte IPs zur Whitelist hinzufügen (``rate.limit.whitelist.ips``)
3. Fenstergroesse (``rate.limit.window.ms``) anpassen

Rate-Limiting funktioniert nicht
--------------------------------

**Ursache**: Konfiguration wird nicht richtig angewendet

**Prüfen**:

1. Ist ``rate.limit.enabled=true`` konfiguriert?
2. Wird die Konfigurationsdatei korrekt gelesen?
3. Wurde |Fess| neu gestartet?

Leistungsauswirkung
-------------------

Wenn die Rate-Limiting-Prüfungen selbst die Leistung beeinträchtigen:

1. Whitelist nutzen, um Prüfungen für vertrauenswürdige IPs zu überspringen
2. Rate-Limiting deaktivieren (``rate.limit.enabled=false``)

Referenzinformationen
=====================

- :doc:`rag-chat` - AI-Suchmodus-Konfiguration
- :doc:`../admin/webconfig-guide` - Web-Crawl-Konfigurationsleitfaden
- :doc:`../api/api-overview` - API-Übersicht
