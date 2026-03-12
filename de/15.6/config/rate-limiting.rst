==================================
Rate-Limiting-Konfiguration
==================================

Übersicht
==========

|Fess| enthält Rate-Limiting-Funktionen zur Aufrechterhaltung der Systemstabilität und Leistung.
Diese Funktionen schützen das System vor übermäßigen Anfragen und ermöglichen eine faire Ressourcenzuteilung.

Rate-Limiting wird in folgenden Szenarien angewendet:

- Alle HTTP-Anfragen einschließlich Such-API und AI-Modus-API (``RateLimitFilter``)
- Crawler-Anfragen (Steuerung über Crawl-Konfiguration)

HTTP-Anfrage-Ratenbegrenzung
============================

Sie können die Anzahl der HTTP-Anfragen an |Fess| pro IP-Adresse begrenzen.
Diese Begrenzung gilt für alle HTTP-Anfragen einschließlich Such-API, AI-Modus-API, Admin-Seiten usw.

Konfiguration
-------------

``app/WEB-INF/conf/fess_config.properties``:

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
- Anfragen von IPs auf der Blockliste geben HTTP 403 (Forbidden) zurück
- Limits werden pro IP-Adresse angewendet
- Pro IP-Adresse beginnt das Fenster mit der ersten Anfrage; nach Ablauf der Fensterperiode wird der Zähler zurückgesetzt (Festes-Fenster-Verfahren)
- Bei Überschreitung wird die IP für die Dauer von ``rate.limit.block.duration.ms`` blockiert

AI-Modus Rate-Limiting
======================

Die AI-Modus-Funktionalität verfügt über Rate-Limiting zur Kontrolle von LLM-API-Kosten und Ressourcenverbrauch.
Für den AI-Modus gilt zusätzlich zur oben beschriebenen HTTP-Anfrage-Ratenbegrenzung eine eigene, AI-Modus-spezifische Ratenbegrenzung.

AI-Modus-spezifische Rate-Limiting-Einstellungen finden Sie unter :doc:`rag-chat`.

.. note::
   Das AI-Modus-Rate-Limiting wird separat vom Rate-Limiting des LLM-Anbieters angewendet.
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

Alle Rate-Limiting-Einstellungen
=================================

Alle in ``app/WEB-INF/conf/fess_config.properties`` konfigurierbaren Eigenschaften.

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
     - Vertrauenswürdige Proxy-IPs (für X-Forwarded-For/X-Real-IP)
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - Bereinigungsintervall zur Vermeidung von Speicherlecks (Anfragenzahl)
     - ``1000``

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

Überwachung und Warnungen
==========================

Konfiguration zur Überwachung des Rate-Limiting-Status:

Protokollausgabe
----------------

Wenn Rate-Limiting angewendet wird, wird es in den Protokollen aufgezeichnet:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

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

- :doc:`rag-chat` - AI-Modus-Konfiguration
- :doc:`../admin/webconfig-guide` - Web-Crawl-Konfigurationsleitfaden
- :doc:`../api/api-overview` - API-Übersicht
