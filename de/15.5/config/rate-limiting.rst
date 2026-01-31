==================================
Rate-Limiting-Konfiguration
==================================

Übersicht
==========

|Fess| enthaelt Rate-Limiting-Funktionen zur Aufrechterhaltung der Systemstabilitaet und Leistung.
Diese Funktionen schuetzen das System vor uebermaeessigen Anfragen und ermoeglichen eine faire Ressourcenzuteilung.

Rate-Limiting wird in folgenden Szenarien angewendet:

- Such-API
- AI-Modus-API
- Crawler-Anfragen

Such-API Rate-Limiting
======================

Sie koennen die Anzahl der Anfragen an die Such-API begrenzen.

Konfiguration
-------------

``app/WEB-INF/conf/system.properties``:

::

    # Rate-Limiting aktivieren
    api.rate.limit.enabled=true

    # Maximale Anfragen pro Minute pro IP-Adresse
    api.rate.limit.requests.per.minute=60

    # Rate-Limit-Fenstergroesse (Sekunden)
    api.rate.limit.window.seconds=60

Verhalten
---------

- Anfragen, die das Rate-Limit ueberschreiten, geben HTTP 429 (Too Many Requests) zurueck
- Limits werden pro IP-Adresse angewendet
- Grenzwerte werden mit einem gleitenden Fensteransatz gezaehlt

AI-Modus Rate-Limiting
======================

Die AI-Modus-Funktionalitaet verfuegt ueber Rate-Limiting zur Kontrolle von LLM-API-Kosten und Ressourcenverbrauch.

Konfiguration
-------------

``app/WEB-INF/conf/system.properties``:

::

    # Chat-Rate-Limiting aktivieren
    rag.chat.rate.limit.enabled=true

    # Maximale Anfragen pro Minute
    rag.chat.rate.limit.requests.per.minute=10

.. note::
   Das AI-Modus-Rate-Limiting wird separat vom Rate-Limiting des LLM-Anbieters angewendet.
   Konfigurieren Sie beide Limits entsprechend.

Crawler Rate-Limiting
=====================

Sie koennen Anfrage-Intervalle konfigurieren, um zu verhindern, dass der Crawler Zielseiten ueberlastet.

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

    # Grosse Seiten (mit Genehmigung)
    intervalTime=500
    numOfThread=3

Beachtung von robots.txt
------------------------

|Fess| beachtet die Crawl-delay-Direktive in robots.txt standardmaessig.

::

    # robots.txt Beispiel
    User-agent: *
    Crawl-delay: 10

Erweiterte Rate-Limiting-Konfiguration
======================================

Benutzerdefiniertes Rate-Limiting
---------------------------------

Um verschiedene Limits fuer bestimmte Benutzer oder Rollen anzuwenden,
ist eine benutzerdefinierte Komponentenimplementierung erforderlich.

::

    // Beispiel fuer benutzerdefinierten RateLimitHelper
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean isAllowed(String key) {
            // Benutzerdefinierte Logik
        }
    }

Burst-Limitierung
-----------------

Konfiguration, die kurze Bursts erlaubt, waehrend anhaltende hohe Last verhindert wird:

::

    # Burst-Toleranz
    api.rate.limit.burst.size=20

    # Anhaltende Begrenzung
    api.rate.limit.sustained.requests.per.second=1

Ausschluss-Einstellungen
========================

Sie koennen bestimmte IP-Adressen oder Benutzer vom Rate-Limiting ausschliessen.

::

    # Ausgeschlossene IP-Adressen (kommagetrennt)
    api.rate.limit.excluded.ips=192.168.1.100,10.0.0.0/8

    # Ausgeschlossene Rollen
    api.rate.limit.excluded.roles=admin

Ueberwachung und Warnungen
==========================

Konfiguration zur Ueberwachung des Rate-Limiting-Status:

Protokollausgabe
----------------

Wenn Rate-Limiting angewendet wird, wird es in den Protokollen aufgezeichnet:

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

Metriken
--------

Rate-Limiting-Metriken koennen ueber die Systemstatistik-API abgerufen werden:

::

    GET /api/admin/stats

Fehlerbehebung
==============

Legitime Anfragen werden blockiert
----------------------------------

**Ursache**: Grenzwerte sind zu streng

**Loesungen**:

1. ``requests.per.minute`` erhoehen
2. Bestimmte IPs zur Ausschlussliste hinzufuegen
3. Fenstergroesse anpassen

Rate-Limiting funktioniert nicht
--------------------------------

**Ursache**: Konfiguration wird nicht richtig angewendet

**Pruefen**:

1. Ist ``api.rate.limit.enabled=true`` konfiguriert?
2. Wird die Konfigurationsdatei korrekt gelesen?
3. Wurde |Fess| neu gestartet?

Leistungsauswirkung
-------------------

Wenn die Rate-Limiting-Pruefungen selbst die Leistung beeintraechtigen:

1. Rate-Limiting-Speicher auf Redis oder aehnliches aendern
2. Pruefhaeufigkeit anpassen

Referenzinformationen
=====================

- :doc:`rag-chat` - AI-Modus-Konfiguration
- :doc:`../admin/webconfig-guide` - Web-Crawl-Konfigurationsleitfaden
- :doc:`../api/api-overview` - API-Übersicht
