====================
Upgrade-Verfahren
====================

Diese Seite beschreibt die Verfahren zum Upgrade von |Fess| von einer früheren Version auf die neueste Version.

.. warning::

   **Wichtige Hinweise vor dem Upgrade**

   - Erstellen Sie vor dem Upgrade unbedingt ein Backup
   - Es wird dringend empfohlen, das Upgrade zunächst in einer Testumgebung zu überprüfen
   - Während des Upgrades wird der Dienst gestoppt, planen Sie daher eine angemessene Wartungszeit ein
   - Je nach Version kann sich das Format der Konfigurationsdateien geändert haben

Unterstützte Versionen
======================

Dieses Upgrade-Verfahren unterstützt Upgrades zwischen folgenden Versionen:

- Fess 14.x → Fess 15.8
- Fess 15.x → Fess 15.8

.. important::

   |Fess| 14.x unterstützt OpenSearch der 2.x-Reihe, |Fess| 15.8 unterstützt OpenSearch 3.8.0.
   Da die OpenSearch-Plugins für |Fess| exakt mit der OpenSearch-Version übereinstimmen müssen,
   ist beim Upgrade von 14.x auch ein Major-Version-Upgrade von OpenSearch zwingend erforderlich.
   Siehe :ref:`upgrade-opensearch`.

.. note::

   Bei Upgrades von älteren Versionen (13.x oder früher) kann ein stufenweises Upgrade erforderlich sein.
   Details finden Sie in den Release Notes.

Vorbereitung vor dem Upgrade
==============================

Überprüfung der Versionskompatibilität
---------------------------------------

Überprüfen Sie die Kompatibilität zwischen der Zielversion und der aktuellen Version des Upgrades.

- `Release Notes <https://github.com/codelibs/fess/releases>`__
- :doc:`prerequisites` - Systemvoraussetzungen für |Fess| 15.8 (Java- und OpenSearch-Version)

Planung der Ausfallzeit
------------------------

Die Upgrade-Arbeiten erfordern einen Systemstopp. Planen Sie die Ausfallzeit unter Berücksichtigung folgender Punkte:

- Backup-Zeit: 10 Minuten ~ mehrere Stunden (abhängig vom Datenvolumen)
- Upgrade-Zeit: 10 ~ 30 Minuten
- Funktionsprüfungszeit: 30 Minuten ~ 1 Stunde
- Pufferzeit: 30 Minuten

**Empfohlene Wartungszeit**: Insgesamt 2 ~ 4 Stunden

Schritt 1: Daten-Backup
========================

Erstellen Sie vor dem Upgrade ein Backup aller Daten.

Backup der Konfigurationsdaten
-------------------------------

1. **Backup über die Verwaltungsseite**

   Melden Sie sich in der Verwaltungsseite an und klicken Sie auf „Systeminformationen" → „Sicherung".

   Auf der Sicherungsseite werden die folgenden Konfigurationsdaten als einzelne Einträge aufgelistet.
   Klicken Sie auf die jeweilige Zeile, um sie herunterzuladen (keine einzelne ZIP-Datei, sondern eine
   individuelle Datei pro Eintrag. Eine Sammel-Download-Funktion gibt es nicht, laden Sie die
   benötigten Einträge daher einzeln herunter).

   - ``fess_basic_config.bulk`` - Konfigurationsindizes (Crawl-Einstellungen, Scheduler, Labels,
     Key-Matches, Rollen, Web-/Datei-Authentifizierung usw., 19 Indizes)
   - ``fess_config.bulk`` - zusätzlich zu den oben genannten 19 Indizes Laufzeitdaten wie
     Crawl-Informationen, fehlgeschlagene URLs, Job-Protokolle und Thumbnail-Warteschlange,
     insgesamt 25 Indizes
   - ``fess_user.bulk`` - Benutzer, Rollen und Gruppen
   - ``system.properties`` - Systemeinstellungen einschließlich der allgemeinen Einstellungen
   - ``fess.json`` - Indexeinstellungen (Anzahl der Shards, ``index.knn`` usw.)
   - ``doc.json`` - Dokumenten-Mapping (Felddefinitionen)

   .. note::

      ``fess_config.bulk`` enthält bereits alle Daten aus ``fess_basic_config.bulk``. Als
      Konfigurationssicherung vor dem Upgrade genügen daher ``fess_basic_config.bulk``,
      ``fess_user.bulk`` und ``system.properties``.

   .. note::

      Protokolldaten wie Suchanfragenprotokolle und Klickprotokolle (``search_log.ndjson``, ``click_log.ndjson``,
      ``favorite_log.ndjson``, ``user_info.ndjson``) können ebenfalls von derselben Seite heruntergeladen werden.
      Falls nur die Konfiguration gesichert wird, ist dies nicht erforderlich. Diese ``*.ndjson``-Dateien
      können außerdem nicht über die Sicherungsseite hochgeladen und wiederhergestellt werden
      (siehe „Rollback-Verfahren").

2. **Backup der Konfigurationsdateien**

   TAR.GZ/ZIP-Version::

       $ cp /path/to/fess/app/WEB-INF/conf/system.properties /backup/
       $ cp /path/to/fess/app/WEB-INF/classes/fess_config.properties /backup/
       $ cp /path/to/fess/bin/fess.in.sh /backup/

   RPM-Version::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/sysconfig/fess /backup/

   DEB-Version::

       $ sudo cp /etc/fess/system.properties /backup/
       $ sudo cp /etc/fess/fess_config.properties /backup/
       $ sudo cp /etc/default/fess /backup/

   .. note::

      ``/etc/sysconfig/fess`` (RPM-Version) und ``/etc/default/fess`` (DEB-Version) sind
      Umgebungsvariablen-Dateien, in denen u. a. ``FESS_PORT``, ``FESS_HEAP_SIZE``,
      ``SEARCH_ENGINE_HTTP_URL`` und ``FESS_DICTIONARY_PATH`` festgelegt werden.
      Bei der TAR.GZ/ZIP-Version befinden sich die entsprechenden Einstellungen in ``bin/fess.in.sh``.

3. **Angepasste Konfigurationsdateien**

   Falls angepasste Konfigurationsdateien vorhanden sind, erstellen Sie auch von diesen Backups::

       $ cp /path/to/fess/app/WEB-INF/classes/log4j2.xml /backup/

   .. note::

      ``app/WEB-INF/classes/log4j2.xml`` enthält die Protokollkonfiguration für den |Fess|-Hauptprozess
      (Web). Untergeordnete Prozesse wie der Crawler verwenden eigene Dateien
      (u. a. ``app/WEB-INF/env/crawler/resources/log4j2.xml`` für ``crawler``, ``suggest``,
      ``thumbnail`` und ``chunk`` — insgesamt vier). Wenn Sie diese angepasst haben, sichern Sie
      sie ebenfalls.

Backup der Indexdaten
----------------------

Erstellen Sie ein Backup der OpenSearch-Indexdaten.

Methode 1: Verwendung der Snapshot-Funktion (empfohlen)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Verwenden Sie die Snapshot-Funktion von OpenSearch für das Backup der Indizes.

.. note::

   Um ein Dateisystem-Repository (``fs``) zu registrieren, müssen Sie zuvor in der ``opensearch.yml`` von OpenSearch
   das Zielverzeichnis für das Backup unter ``path.repo`` angeben und OpenSearch neu starten.

1. Repository-Konfiguration::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup" -H 'Content-Type: application/json' -d'
       {
         "type": "fs",
         "settings": {
           "location": "/backup/opensearch/snapshots"
         }
       }'

2. Snapshot-Erstellung::

       $ curl -X PUT "http://localhost:9200/_snapshot/fess_backup/snapshot_1?wait_for_completion=true"

3. Snapshot-Überprüfung::

       $ curl -X GET "http://localhost:9200/_snapshot/fess_backup/snapshot_1"

Methode 2: Backup des gesamten Verzeichnisses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stoppen Sie OpenSearch und erstellen Sie ein Backup des Datenverzeichnisses.

::

    $ sudo systemctl stop opensearch
    $ sudo tar czf /backup/opensearch-data-$(date +%Y%m%d).tar.gz /var/lib/opensearch/data
    $ sudo systemctl start opensearch

Backup der Docker-Version
--------------------------

Die OpenSearch-Daten werden in Docker-Volumes gespeichert. ``compose-opensearch3.yaml`` definiert zwei Volumes:
``search01_data`` für Indexdaten und ``search01_dictionary`` für Wörterbuchdateien.

.. note::

   Die tatsächlichen Volume-Namen werden mit dem Compose-Projektnamen als Präfix versehen (standardmäßig der Name des
   Verzeichnisses, das die Compose-Dateien enthält). Überprüfen Sie die genauen Namen mit folgendem Befehl::

       $ docker volume ls

Stoppen Sie die Container und erstellen Sie dann ein Backup der Volumes. Geben Sie bei ``-v`` in
``docker run`` den tatsächlichen Volume-Namen inklusive Präfix an::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml stop
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-data-backup.tar.gz /data
    $ docker run --rm -v ${PROJECT}_search01_dictionary:/data -v $(pwd):/backup ubuntu tar czf /backup/search01-dictionary-backup.tar.gz /data
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml start

.. warning::

   Wenn Sie bei ``-v`` den Namen ``search01_data`` ohne Präfix angeben, greift Docker nicht auf das
   vorhandene Volume zu, sondern legt ein neues, leeres Volume mit demselben Namen an. Der Befehl
   liefert dabei keinen Fehler, sondern erzeugt ein leeres Archiv, sodass es so aussieht, als wäre
   das Backup erfolgreich erstellt worden.

.. note::

   Der |Fess|-Hauptcontainer (``fess01``) besitzt kein eigenes Volume, daher sind ausschließlich die
   beiden oben genannten Volumes zu sichern. Über die Verwaltungsseite geänderte allgemeine
   Einstellungen sowie über die Verwaltungsseite installierte Plugins werden jedoch nur innerhalb des
   Containers gespeichert und gehen beim Neuerstellen des Containers verloren. Sorgen Sie mit
   ``FESS_JAVA_OPTS`` bzw. ``FESS_PLUGINS`` in der Compose-Datei für deren dauerhafte Persistenz.

Schritt 2: Stopp der aktuellen Version
=======================================

Stoppen Sie Fess und OpenSearch.

Die TAR.GZ/ZIP-Version enthält kein Skript zum Stoppen. Wenn Sie ``bin/fess`` mit der Option ``-p``
gestartet haben, stoppen Sie den Prozess anhand der PID-Datei::

    $ kill $(cat /path/to/fess/fess.pid)
    $ kill <opensearch_pid>

Wenn Sie ohne ``-p`` gestartet haben, ermitteln Sie die Prozess-ID und beenden Sie den Prozess mit
``kill`` (mit ``-d`` allein wird keine PID-Datei erstellt).

RPM/DEB-Version (systemd)::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Docker-Version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down

Schritt 3: Installation der neuen Version
==========================================

Die Vorgehensweise unterscheidet sich je nach Installationsmethode.

TAR.GZ/ZIP-Version
------------------

1. Neue Version herunterladen und entpacken::

       $ wget https://github.com/codelibs/fess/releases/download/fess-15.8.0/fess-15.8.0.zip
       $ unzip fess-15.8.0.zip

   .. note::

      Die Archivversion von |Fess| wird ausschließlich im ZIP-Format bereitgestellt
      (``fess-15.8.0.tar.gz`` steht nicht zur Verfügung).

2. Konfiguration der alten Version kopieren::

       $ cp /path/to/old-fess/app/WEB-INF/conf/system.properties /path/to/fess-15.8.0/app/WEB-INF/conf/
       $ cp /path/to/old-fess/app/WEB-INF/classes/fess_config.properties /path/to/fess-15.8.0/app/WEB-INF/classes/
       $ cp /path/to/old-fess/bin/fess.in.sh /path/to/fess-15.8.0/bin/

3. Falls Sie Anpassungen vorgenommen haben, kopieren Sie zusätzlich Folgendes::

       # Protokollkonfiguration
       $ cp /path/to/old-fess/app/WEB-INF/classes/log4j2.xml /path/to/fess-15.8.0/app/WEB-INF/classes/
       # Installierte Plugins
       $ cp -r /path/to/old-fess/app/WEB-INF/plugin/. /path/to/fess-15.8.0/app/WEB-INF/plugin/
       # Theme
       $ cp -r /path/to/old-fess/app/themes/. /path/to/fess-15.8.0/app/themes/

   .. warning::

      Kopieren Sie JSPs, die Sie über „Design" in der Verwaltungsseite bearbeitet haben
      (``app/WEB-INF/view/``), nicht unverändert. Wenn sich die Struktur der JSPs in der neuen
      Version geändert hat, wird die Seite nicht mehr korrekt angezeigt. Wenden Sie Ihre Änderungen
      stattdessen erneut auf die JSPs der neuen Version an.

4. Wenn Sie das eingebettete OpenSearch verwenden (Start von ``bin/fess`` ohne gesetzte
   ``SEARCH_ENGINE_HTTP_URL``), kopieren Sie zusätzlich die Indexdaten::

       $ cp -r /path/to/old-fess/es/data/. /path/to/fess-15.8.0/es/data/

5. Überprüfen Sie Konfigurationsdifferenzen und passen Sie diese bei Bedarf an

RPM/DEB-Version
---------------

Installieren Sie das Paket der neuen Version::

    # RPM
    $ sudo rpm -Uvh fess-15.8.0.rpm

    # DEB
    $ sudo dpkg -i fess-15.8.0.deb

.. note::

   Bei der RPM-Version sind die Konfigurationsdateien unter ``/etc/fess/*`` als
   ``%config(noreplace)`` registriert und bleiben daher auch beim Upgrade erhalten (die neuen
   Standarddateien werden zusätzlich als ``.rpmnew`` abgelegt). Bei neuen Konfigurationsoptionen ist
   dennoch eine manuelle Anpassung erforderlich.

.. warning::

   Bei der DEB-Version sind die Dateien unter ``/etc/fess/*`` nicht als Conffile registriert (als
   Conffile sind nur ``/etc/default/fess``, ``/etc/init.d/fess`` und
   ``/usr/lib/systemd/system/fess.service`` eingetragen). Beim Ausführen von ``dpkg -i`` werden daher
   Dateien wie ``/etc/fess/fess_config.properties`` durch die Dateien der neuen Version überschrieben.
   Spielen Sie die in Schritt 1 gesicherte Konfiguration nach dem Upgrade erneut ein.
   ``/etc/fess/system.properties`` wird zur Laufzeit erzeugt und ist nicht Teil des Pakets, sodass
   diese Datei nicht überschrieben wird.

Docker-Version
--------------

1. Neue Version der Compose-Dateien herunterladen::

       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose.yaml
       $ wget https://raw.githubusercontent.com/codelibs/docker-fess/v15.8.0/compose/compose-opensearch3.yaml

2. Neue Images herunterladen::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml pull

.. _upgrade-opensearch:

Schritt 4: Upgrade von OpenSearch
=================================

|Fess| 15.8 unterstützt OpenSearch 3.8.0. Wenn das verbundene OpenSearch älter ist, aktualisieren
Sie es anhand der folgenden Schritte.

.. note::

   Diese Anleitung gilt für die manuelle Verwaltung von OpenSearch bei der TAR.GZ/ZIP-Version und der RPM/DEB-Version.
   Bei der Docker-Version werden OpenSearch und die Plugins durch das Herunterladen der neuen Images in Schritt 3
   gemeinsam aktualisiert, sodass dieser Schritt nicht erforderlich ist.

.. important::

   |Fess| 15.8 nimmt unabhängig davon, ob die Chunk-Vektor-Suche (semantische Suche) genutzt wird,
   immer ``index.knn`` in die Einstellungen des Suchindex und ``content_chunk_vector`` (Typ
   ``knn_vector``) in das Mapping auf. Daher ist das **k-NN-Plugin im verbundenen OpenSearch
   zwingend erforderlich**.

   - Es ist in der Standarddistribution von OpenSearch sowie im Docker-Image bereits enthalten.
   - **In der Minimal-Distribution ist es nicht enthalten, wodurch die Neuerstellung des Index
     fehlschlägt und |Fess| nicht starten kann.**
   - In den Indexeinstellungen wird außerdem stets ``knn.derived_source.enabled`` übermittelt. Bei
     älteren OpenSearch-Versionen, die diese Option nicht kennen, schlägt die Indexerstellung
     unabhängig vom k-NN-Plugin fehl.

   Details finden Sie im Abschnitt „Voraussetzungen" von :doc:`../config/search-semantic`.

.. warning::

   Führen Sie Major-Version-Upgrades von OpenSearch vorsichtig durch.
   Es können Index-Kompatibilitätsprobleme auftreten.
   |Fess| 14.x setzt auf OpenSearch der 2.x-Reihe, daher trifft dies bei einem Upgrade von 14.x
   immer zu.

1. Installieren Sie die neue Version von OpenSearch

2. Plugins neu installieren::

       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-fess:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-analysis-extension:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-minhash:3.8.0
       $ sudo /usr/share/opensearch/bin/opensearch-plugin install org.codelibs.opensearch:opensearch-configsync:3.8.0

   .. note::

      Die Versionen dieser Plugins müssen mit der verwendeten OpenSearch-Version übereinstimmen.
      |Fess| 15.8 ist kompatibel mit OpenSearch 3.8.0. Bei Versionsabweichungen schlägt die
      Plugin-Installation fehl.

3. OpenSearch starten::

       $ sudo systemctl start opensearch.service

Schritt 5: Start der neuen Version
====================================

TAR.GZ/ZIP-Version::

    $ cd /path/to/fess-15.8.0
    $ ./bin/fess -d -p /path/to/fess-15.8.0/fess.pid

.. note::

   Mit ``-p`` wird eine PID-Datei erstellt, mit der Sie den Prozess beim nächsten Stoppen über
   ``kill $(cat /path/to/fess-15.8.0/fess.pid)`` beenden können.

RPM/DEB-Version::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Docker-Version::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

Schritt 6: Funktionsprüfung
============================

1. **Überprüfung der Protokolle**

   Stellen Sie sicher, dass keine Fehler vorliegen.

   TAR.GZ/ZIP-Version::

       $ tail -f /path/to/fess/logs/fess.log

   RPM/DEB-Version::

       $ sudo tail -f /var/log/fess/fess.log

   Docker-Version::

       $ docker compose -f compose.yaml -f compose-opensearch3.yaml logs -f fess01

   .. note::

      Im selben Protokollverzeichnis werden außerdem ``fess-crawler.log`` (Crawl-Verarbeitung),
      ``audit.log`` (Authentifizierung und Verwaltungsvorgänge) sowie ``searchlog.log``
      (Suchanfragen) ausgegeben.

2. **Zugriff auf die Weboberfläche**

   Greifen Sie mit dem Browser auf http://localhost:8080/ zu.

3. **Anmeldung in der Verwaltungsseite**

   Greifen Sie auf http://localhost:8080/admin zu und melden Sie sich mit dem Administratorkonto an.

4. **Versionsüberprüfung**

   Klicken Sie in der Verwaltungsseite auf „Systeminformationen" → „Konfigurationsinformationen" und überprüfen Sie,
   dass ``fess.version`` unter „Systemeigenschaften" die neue Version anzeigt.

5. **Funktionsprüfung der Suche**

   Führen Sie auf der Suchseite eine Suche durch und überprüfen Sie, dass Ergebnisse korrekt zurückgegeben werden.

Schritt 7: Neuerstellung des Index (empfohlen)
===============================================

Bei Major-Version-Upgrades wird die Neuerstellung des Index empfohlen.

.. note::

   Die folgenden Schritte führen den Crawl erneut aus; sie aktualisieren nicht das Index-Mapping
   (Felddefinitionen). Wenn Sie eine Neuindizierung benötigen, die das Mapping aktualisiert — zum
   Beispiel, um die Chunk-Vektor-Suche (semantische Suche) neu zu aktivieren —, führen Sie separat
   die „Neuindizierung" unter „Systeminformationen" → „Wartung" in der Admin-Oberfläche aus. Siehe
   :ref:`semantic-search-migration` (:doc:`../config/search-semantic`) für Details.

1. Überprüfen Sie bestehende Crawl-Zeitpläne
2. Führen Sie „Default Crawler" unter „System" → „Scheduler" aus
3. Warten Sie, bis der Crawl abgeschlossen ist
4. Überprüfen Sie die Suchergebnisse

.. warning::

   Da bei der Neuindizierung der Index mit dem neuen Mapping neu erstellt wird, schlägt dieser
   Vorgang bei OpenSearch ohne k-NN-Plugin fehl. Beachten Sie die Hinweise in Schritt 4.

Migrationsaufgaben speziell für 15.8
====================================

Wenn Sie von 15.7 oder früher auf 15.8 aktualisieren, sind je nach genutzten Funktionen die
folgenden Arbeiten erforderlich.

Falls Sie die semantische Suche genutzt haben
---------------------------------------------

Das Plugin ``fess-webapp-semantic-search``, das bis 15.7 die semantische Suche bereitstellte, wurde
in 15.8 in den Kern integriert und ist daher nicht mehr erforderlich (veraltet). Sie müssen das
Plugin entfernen, ``-Dfess.semantic_search.*`` sowie ``-Drank.fusion.searchers=default,semantic``
löschen und die alte Ingest-Pipeline lösen (detach). Das Vorgehen ist unter
:ref:`semantic-search-migration` (:doc:`../config/search-semantic`) beschrieben.

Falls Sie den KI-Suchmodus (RAG-Chat) genutzt haben
---------------------------------------------------

Ab 15.8 wurde die Funktion des KI-Suchmodus (RAG-Chat) in separate Plugins wie ``fess-llm-ollama``,
``fess-llm-openai`` und ``fess-llm-gemini`` ausgelagert. Installieren Sie das zu Ihrem verwendeten
Anbieter passende Plugin über die Verwaltungsseite unter „System" → „Plugins".

Falls Sie SPNEGO (Windows-integrierte Authentifizierung) genutzt haben
----------------------------------------------------------------------

Ab 15.8 wird eine SPNEGO-Anmeldung abgelehnt, wenn sich die Kerberos-Realm des Client-Principals
von der Realm des Servers unterscheidet. Melden sich Ihre Benutzer aus einer untergeordneten
Domäne einer AD-Domänenstruktur oder aus einer vertrauten Gesamtstruktur an, tragen Sie diese
Realms kommagetrennt in ``spnego.allowed.realms`` ein, entweder über die Verwaltungsseite unter
„System" → „Allgemein" oder in ``app/WEB-INF/conf/system.properties``. Andernfalls werden
Benutzer, die sich bis 15.7 anmelden konnten, mit ``Kerberos realm is not allowed`` abgewiesen.
Einzelheiten finden Sie unter :doc:`../config/sso-spnego`.

Falls Sie SAML-Authentifizierung (SSO) genutzt haben
----------------------------------------------------

Ab 15.8 bindet |Fess| jede SAML-Antwort an die ID der von ihm gesendeten AuthnRequest, sodass
IdP-initiiertes (unaufgefordertes) SSO nicht mehr funktioniert. Eine Anmeldung, die von einer
|Fess|-Kachel in einem IdP-Portal wie dem Okta-Dashboard oder dem Portal „Meine Apps" von
Microsoft Entra ID aus gestartet wird, hat keine zugehörige AuthnRequest und wird abgelehnt. Bis
15.7 funktionierte dies, weil |Fess| die nicht zuordenbare Antwort an den IdP zurückschickte und
der IdP sofort eine angeforderte Assertion lieferte. Wenn Sie auf der IdP-Seite eine Kachel
anlegen, lassen Sie diese auf den |Fess|-Endpunkt ``/sso/`` verweisen, damit die Anmeldung
SP-initiiert erfolgt.

Zudem sendet der IdP die Assertion als seitenübergreifenden POST zurück, weshalb
``tomcat.sameSiteCookies`` in ``tomcat_config.properties`` auf ``none`` gesetzt werden muss. Mit
dem ausgelieferten Standardwert ``lax`` wird das Sitzungs-Cookie bei dieser Anfrage nicht
mitgesendet und die SAML-Anmeldung kann nicht abgeschlossen werden. Diese Datei liegt beim
ZIP-Paket unter ``lib/classes/`` und bei den DEB-/RPM-Paketen unter ``/etc/fess/``; nach der
Änderung muss |Fess| neu gestartet werden. Browser akzeptieren ``none`` nur bei einem Cookie, das
auch das Attribut ``Secure`` trägt, sodass |Fess| über HTTPS bereitgestellt werden muss. Bis 15.7
führte dieselbe Fehlkonfiguration nicht zu einem klaren Fehler, sondern zu einer endlosen
Weiterleitungsschleife zum IdP; prüfen Sie die Einstellung daher auch bei einer Installation, die
zu funktionieren schien. In 15.8 schlägt die Anmeldung einmalig fehl, statt in einer Schleife zu
laufen. Einzelheiten finden Sie unter :doc:`../config/sso-saml`.

Falls Sie Microsoft Entra ID (Azure AD) genutzt haben
-----------------------------------------------------

Ab 15.8 lautet der Standardwert des beim Autorisierungsendpunkt angeforderten Response-Modus
``query`` statt ``form_post``. Bis 15.7 wurde der Callback als websiteübergreifender POST
zurückgegeben, und beim |Fess|-Standardwert ``tomcat.sameSiteCookies = lax`` wird das
Sitzungscookie dabei nicht mitgesendet, sodass ``tomcat.sameSiteCookies = none`` erforderlich
war. Wenn Sie ``none`` nur aus diesem Grund gesetzt haben, können Sie zum Standardwert
zurückkehren. Um das bisherige Verhalten beizubehalten, setzen Sie
``entraid.response.mode=form_post`` und belassen ``tomcat.sameSiteCookies = none``.

Außerdem führt 15.8 ``entraid.require.membership`` ein. Damit legen Sie fest, was geschieht, wenn
Microsoft Graph bei der Anmeldung die Gruppen und Rollen des Benutzers nicht zurückgibt. Der
Standardwert ``false`` verhält sich wie 15.7: Es wird eine Warnung protokolliert und die
Anmeldung wird fortgesetzt. Der Benutzer besitzt dann jedoch nur ``entraid.default.groups`` und
``entraid.default.roles``, sodass Dokumente, die er eigentlich sehen dürfte, in den
Suchergebnissen fehlen. Mit ``true`` wird eine solche Anmeldung stattdessen abgelehnt.
Einzelheiten finden Sie unter :doc:`../config/sso-entraid`.

Aktualisierung der Plugin-Versionen
-----------------------------------

Die unter ``app/WEB-INF/plugin/`` installierten Plugins müssen durch die zur |Fess|-Version
passenden Versionen ersetzt werden. Wenn Sie bei der Docker-Version ``FESS_PLUGINS`` angeben,
aktualisieren Sie den Versionsanteil entsprechend, z. B. ``fess-ds-wikipedia:15.8.0``.

Rollback-Verfahren
==================

Bei fehlgeschlagenem Upgrade können Sie mit folgenden Schritten ein Rollback durchführen.

Schritt 1: Stopp der neuen Version
-----------------------------------

::

    $ sudo systemctl stop fess.service
    $ sudo systemctl stop opensearch.service

Schritt 2: Wiederherstellung der alten Version
-----------------------------------------------

Stellen Sie Konfigurationsdateien und Daten aus dem Backup wieder her.

Bei RPM/DEB-Version::

    $ sudo rpm -Uvh --oldpackage fess-<old-version>.rpm

oder::

    $ sudo dpkg -i fess-<old-version>.deb

Schritt 3: Datenwiederherstellung
----------------------------------

Wiederherstellung aus Snapshot::

    $ curl -X POST "http://localhost:9200/_snapshot/fess_backup/snapshot_1/_restore?wait_for_completion=true"

Oder Wiederherstellung des Verzeichnisses aus dem Backup::

    $ sudo systemctl stop opensearch
    $ sudo rm -rf /var/lib/opensearch/data/*
    $ sudo tar xzf /backup/opensearch-data-backup.tar.gz -C /
    $ sudo systemctl start opensearch

Setzen Sie bei der Docker-Version zunächst die Compose-Dateien der alten Version wieder ein und
stellen Sie dann den Inhalt der Volumes wieder her::

    $ docker compose -f compose.yaml -f compose-opensearch3.yaml down
    $ PROJECT=$(basename "$(pwd)")
    $ docker run --rm -v ${PROJECT}_search01_data:/data -v $(pwd):/backup ubuntu \
        sh -c "rm -rf /data/* && tar xzf /backup/search01-data-backup.tar.gz -C /"
    $ docker compose -f compose.yaml -f compose-opensearch3.yaml up -d

.. note::

   Die über die Verwaltungsseite heruntergeladenen Konfigurationsdaten können nach dem Start von
   |Fess| über die Upload-Funktion auf der Seite „Systeminformationen" → „Sicherung" erneut
   importiert und wiederhergestellt werden. Hochgeladen werden können ausschließlich ``*.bulk``,
   ``*.properties``-Dateien, die mit ``system`` beginnen, ``*.xml``-Dateien, die mit ``gsa``
   beginnen, sowie ``*.json``-Dateien, die mit ``fess`` oder ``doc`` beginnen — jeweils eine Datei
   pro Vorgang. ``*.ndjson``-Dateien wie Suchprotokolle werden nicht akzeptiert und führen zu einem
   Fehler.

.. warning::

   Das Hochladen von ``fess.json`` und ``doc.json`` überschreibt die in |Fess| enthaltenen
   Indexdefinitionsdateien selbst. Wenn Sie nach einem Upgrade die ``fess.json`` oder ``doc.json``
   einer älteren Version hochladen, gehen die Indexeinstellungen und das Mapping der neuen Version
   verloren. Laden Sie diese Dateien nur zum Zweck eines Rollbacks hoch.

.. note::

   Eine hochgeladene ``system.properties`` wird nur in den Arbeitsspeicher geladen und nicht in eine
   Datei geschrieben. Der Inhalt von ``system.properties`` geht daher bei einem Neustart von |Fess|
   verloren. Um eine zuverlässige Wiederherstellung zu gewährleisten, platzieren Sie die gesicherte
   Datei vor dem Start direkt am vorgesehenen Ort (TAR.GZ/ZIP-Version: ``app/WEB-INF/conf/``,
   RPM/DEB-Version: ``/etc/fess/``).

.. note::

   Der Import wird asynchron ausgeführt, und auf dem Bildschirm wird lediglich angezeigt, dass er
   gestartet wurde. Ob der Import tatsächlich erfolgreich war, überprüfen Sie anhand von
   ``fess.log``.

Schritt 4: Start und Überprüfung des Dienstes
----------------------------------------------

::

    $ sudo systemctl start opensearch.service
    $ sudo systemctl start fess.service

Überprüfen Sie den Betrieb und stellen Sie sicher, dass alles wieder normal läuft.

Häufig gestellte Fragen
=======================

F: Ist ein Upgrade ohne Ausfallzeit möglich?
---------------------------------------------

A: Ein Upgrade von Fess erfordert einen Dienststopp. Um die Ausfallzeit zu minimieren, sollten Sie Folgendes in Betracht ziehen:

- Überprüfung der Vorgehensweise in der Testumgebung im Voraus
- Backup im Voraus erstellen
- Ausreichend Wartungszeit einplanen

F: Muss auch OpenSearch aktualisiert werden?
---------------------------------------------

A: Für jede |Fess|-Version ist eine bestimmte OpenSearch-Version vorgesehen.
|Fess| 15.8 unterstützt OpenSearch 3.8.0.
Da die |Fess|-spezifischen OpenSearch-Plugins wie ``opensearch-analysis-fess`` exakt mit der
OpenSearch-Version übereinstimmen müssen, aktualisieren Sie beim Upgrade von OpenSearch die Plugins
auf die entsprechende Version (3.8.0).

|Fess| 15.8 setzt außerdem zwingend das k-NN-Plugin voraus und sendet in den Indexeinstellungen
stets ``knn.derived_source.enabled``. Mit einem älteren OpenSearch schlägt die Erstellung neuer
Indizes fehl, sodass ein Upgrade von OpenSearch faktisch erforderlich ist. Details finden Sie in
Schritt 4.

F: Muss der Index neu erstellt werden?
---------------------------------------

A: Bei einem Minor-Version-Upgrade von |Fess| (15.x → 15.8) ist dies normalerweise nicht
erforderlich, sofern Sie die Chunk-Vektor-Suche nicht nutzen. Der bestehende Index kann unverändert
weiterverwendet werden, und da Optionen wie ``content_chunker.enabled`` standardmäßig deaktiviert
sind, ändert sich das Verhalten nicht.

In folgenden Fällen ist eine Neuerstellung bzw. Neuindizierung erforderlich:

- **Wenn Sie die Chunk-Vektor-Suche (semantische Suche) neu aktivieren**: Da das neue Mapping bei
  bestehenden Indizes nicht übernommen wird, ist eine Neuindizierung zwingend erforderlich. Details
  finden Sie unter :ref:`semantic-search-migration` (:doc:`../config/search-semantic`).
- **Beim Upgrade von 14.x**: Da OpenSearch dabei ein Major-Version-Upgrade von 2.x auf 3.x
  durchläuft, wird die Neuerstellung des Index empfohlen.

.. warning::

   Vorgänge, die einen Index neu anlegen (einschließlich der Neuindizierung), schlagen bei
   OpenSearch ohne k-NN-Plugin fehl. Beachten Sie die Hinweise in Schritt 4.

F: Nach dem Upgrade werden keine Suchergebnisse angezeigt
----------------------------------------------------------

A: Überprüfen Sie Folgendes:

1. Überprüfen Sie, ob OpenSearch läuft
2. Überprüfen Sie, ob Indizes vorhanden sind (``curl http://localhost:9200/_cat/indices``)
3. Crawl erneut ausführen

Nächste Schritte
================

Nach Abschluss des Upgrades:

- :doc:`run` - Überprüfung von Start und Erstkonfiguration
- :doc:`security` - Überprüfung der Sicherheitseinstellungen
- :doc:`../config/search-semantic` - Konfiguration und Migrationsschritte für die
  Chunk-Vektor-Suche (semantische Suche)
- Überprüfung neuer Funktionen in den Release Notes
