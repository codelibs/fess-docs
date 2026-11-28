============================================
Eine Fess-Instanz für mehrere Organisationen
============================================

Einleitung
==========

Wenn Sie für jedes Konzernunternehmen oder jede Abteilung einen eigenen Suchdienst anbieten möchten und dafür pro Organisation ein eigenes Fess aufbauen, vervielfachen sich die Server und die zu verwaltenden Crawl-Konfigurationen mit der Zahl der Organisationen.
Mit der Funktion für virtuelle Hosts in Fess können Sie ein einziges Fess unter mehreren Hostnamen bereitstellen und Suchziele, Labels und Suchseite je Hostname umschalten.

Ein virtueller Host steuert jedoch nur, was abhängig vom angefragten Hostnamen angezeigt wird; er ist keine Zugriffskontrolle.
Damit die Dokumente einer Organisation für andere zuverlässig verborgen bleiben, müssen Sie ihn mit rollenbasierten Berechtigungen und einer Anmeldung kombinieren.

In diesem Artikel richten wir am Beispiel der beiden Mandanten Firma A und Firma B Schritt für Schritt Folgendes in Fess 15.9 ein.

- Hostnamen und Mandanten über „Virtueller Host“ unter [Allgemein] zuordnen
- Virtuellen Host und Berechtigungen in Crawl-Konfigurationen und Labels angeben, um die Dokumente der Mandanten zu trennen
- Mit einem Theme, das wie der Schlüssel des virtuellen Hosts heißt, jedem Mandanten eine eigene Suchseite geben
- Sich als Benutzer eines Mandanten anmelden und prüfen, dass die Dokumente anderer Mandanten nicht sichtbar sind
- Mandanten in der richtigen Reihenfolge hinzufügen und entfernen

Die Grundlagen zu Rollen, Gruppen und Benutzern behandelt :doc:`guide-05`.

Vorab das Wichtigste: Ein virtueller Host ist keine Zugriffskontrolle
=====================================================================

Fess wertet bei jeder Anfrage die Zeilen unter „Virtueller Host“ in [Allgemein] von oben nach unten aus und verwendet den Namen des virtuellen Hosts (im Folgenden: Schlüssel) aus der ersten Zeile, deren angegebener Header (normalerweise ``Host``) übereinstimmt.
Steht der Schlüssel fest, werden die folgenden Funktionen nach diesem Schlüssel gefiltert.

- Suchergebnisse: Es werden nur Dokumente zurückgegeben, deren Crawl-Konfiguration diesen Schlüssel unter „Virtuelle Hosts“ enthält (das gilt auch für die Such-API)
- Labels: Es werden nur Labels angezeigt, deren Feld „Virtueller Host“ diesen Schlüssel enthält
- Schlüsselübereinstimmung, Verwandter Inhalt und Verwandte Abfrage: Es werden nur Einstellungen verwendet, deren Feld „Virtueller Host“ diesen Schlüssel enthält
- Suchseite: Gibt es ein Theme, dessen Name dem Schlüssel in Kleinbuchstaben entspricht, wird die Seite mit diesem Theme angezeigt

Passt eine Anfrage dagegen auf keine Zeile, findet keine dieser Filterungen statt.
Greift jemand direkt über die IP-Adresse auf den Server zu oder schreibt ein Reverse Proxy den ``Host``-Header um, entfällt die Filterung nach virtuellem Host, und die Dokumente aller Mandanten werden durchsuchbar, soweit die Berechtigungen sie zulassen.
Auch ein falsch geschriebener Hostname oder eine fehlende Portnummer in [Allgemein] führt zu keinem Fehler, sondern wird einfach als „keine Übereinstimmung“ behandelt.

Damit Dokumente nicht über Mandantengrenzen hinweg sichtbar sind, kombinieren Sie daher die folgenden beiden Maßnahmen.

- Die Berechtigungen der Dokumente eines Mandanten auf dessen Rolle beschränken (z. B. ``{role}tenanta_user``)
- Für die Suchseite eine Anmeldung voraussetzen und den Benutzern die Rolle ihres Mandanten zuweisen

Der Aufbau in diesem Artikel
============================

.. list-table::
   :header-rows: 1
   :widths: 16 26 14 18 26

   * - Mandant
     - Öffentlicher Hostname
     - Schlüssel
     - Rolle
     - Crawl-Ziel
   * - Firma A
     - ``search-a.example.com``
     - ``tenanta``
     - ``tenanta_user``
     - ``https://portal-a.example.com/``
   * - Firma B
     - ``search-b.example.com``
     - ``tenantb``
     - ``tenantb_user``
     - ``https://portal-b.example.com/``

In einem Schlüssel sind nur alphanumerische Zeichen und Unterstriche (``a-zA-Z0-9_``) erlaubt.
Alle anderen Zeichen werden beim Speichern entfernt: Schreiben Sie ``tenant-a``, wird der Schlüssel zu ``tenanta``, und ein ``tenant-a`` in einer Crawl-Konfiguration passt dann nicht.
``admin``, ``common``, ``error``, ``login`` und ``profile`` sind reserviert und können nicht verwendet werden.

Die Felder „Virtuelle Hosts“ in Crawl-Konfigurationen und „Virtueller Host“ in Labels sind Freitextfelder, und der Abgleich mit dem Schlüssel unterscheidet Groß- und Kleinschreibung.
Da auch Theme-Namen nur aus Kleinbuchstaben bestehen dürfen, vermeiden Sie Fehler, wenn Sie die Schlüssel von Anfang an aus kleingeschriebenen alphanumerischen Zeichen bilden.

Schritt 1: Hostnamen den Schlüsseln zuordnen
============================================

Öffnen Sie in der Verwaltungsoberfläche [System] > [Allgemein], tragen Sie unter „Virtueller Host“ pro Zeile einen Eintrag ``Headername:Headerwert=Schlüssel`` ein und aktualisieren Sie.

::

    Host:search-a.example.com=tenanta
    Host:search-b.example.com=tenantb

Der Headerwert wird ohne Unterscheidung von Groß- und Kleinschreibung auf exakte Übereinstimmung verglichen.
Greift ein Browser über einen anderen als die Standardports (80 und 443) zu, hängt er die Portnummer an den ``Host``-Header an. Wenn die Benutzer direkt auf Port 8080 von Fess zugreifen, geben Sie daher wie folgt auch den Port an.
Sie können auch beide Schreibweisen untereinander angeben.

::

    Host:search-a.example.com:8080=tenanta
    Host:search-b.example.com:8080=tenantb

Die Einstellung wird mit dem Speichern wirksam; ein Neustart ist nicht nötig.
Sie können sie im gleichen Format auch unter ``virtual.host.headers`` in ``fess_config.properties`` angeben, doch hat ein Wert in [Allgemein] Vorrang.

Steht Fess hinter einem Reverse Proxy, reichen Sie den vom Browser gesendeten ``Host``-Header bis zu Fess durch.
Nginx setzt ``Host`` standardmäßig auf das Ziel von ``proxy_pass``, daher ist ``proxy_set_header Host $host;`` erforderlich.

::

    server {
        server_name search-a.example.com search-b.example.com;
        location / {
            proxy_pass http://127.0.0.1:8080;
            proxy_set_header Host $host;
        }
    }

In einem Aufbau, der ``Host`` umschreibt, können Sie stattdessen ``X-Forwarded-Host`` als Headernamen angeben (z. B. ``X-Forwarded-Host:search-a.example.com=tenanta``).

.. warning::

   Die Einstellungen unter [Allgemein] werden in ``system.properties`` im Container gespeichert.
   ``fess01`` in docker-fess hat kein Volume. Wenn Sie den Container mit ``docker compose down`` neu erstellen, geht daher auch der Wert von „Virtueller Host“ verloren (bei ``stop`` und ``start`` bleibt er erhalten).
   Das Theme, das Sie in einem späteren Schritt hochladen, liegt ebenfalls im Container und geht auf die gleiche Weise verloren.
   Wie Sie die Einstellungen erhalten, lesen Sie unter `Installation mit Docker (Detailliert) <https://fess.codelibs.org/de/stable/install/install-docker.html>`__.

Schritt 2: Rollen und Benutzer der Mandanten anlegen
====================================================

1. Legen Sie unter [Benutzer] > [Rolle] die Rollen ``tenanta_user`` und ``tenantb_user`` an.
2. Legen Sie unter [Benutzer] > [Benutzer] die Benutzer der einzelnen Mandanten an und wählen Sie unter „Rollen“ die Rolle ihres Mandanten.
3. Aktivieren Sie unter [System] > [Allgemein] die Option „Anmeldung erforderlich“.

Angemeldete Benutzer erhalten kein ``{role}guest`` und suchen nur mit den Berechtigungen ihres Benutzers, ihrer Gruppen und Rollen.
Wenn Sie Gruppen aus LDAP oder SSO direkt verwenden möchten, können Sie statt einer Rolle ``{group}<Gruppenname>`` angeben.
Wie Berechtigungen funktionieren und wie die LDAP-Anbindung erfolgt, beschreibt :doc:`guide-05`; zu SSO siehe :doc:`guide-15`.

Schritt 3: Ein Label pro Mandant anlegen
========================================

Ein Label wird beim Crawlen den Dokumenten zugewiesen, deren URL auf „Eingeschlossene Pfade“ passt.
Legen Sie die Labels deshalb vor dem Crawlen an.

Klicken Sie unter [Crawler] > [Label] auf [Neu erstellen] und geben Sie für Firma A Folgendes ein (das Label für Firma B legen Sie auf die gleiche Weise an).

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Wert
   * - Name
     - ``Portal Firma A``
   * - Wert
     - ``tenanta_docs`` (nur alphanumerische Zeichen und Unterstriche)
   * - Eingeschlossene Pfade
     - ``https://portal-a\.example\.com/.*``
   * - Berechtigungen
     - ``{role}tenanta_user``
   * - Virtueller Host
     - ``tenanta``

In den Berechtigungen eines neuen Labels steht bereits ``{role}guest``.
Ein Label wird nur angezeigt, wenn der Benutzer eine Rolle aus seinen Berechtigungen besitzt. Belassen Sie ``{role}guest``, sehen angemeldete Benutzer des Mandanten das Label daher nicht.

Ein Label, dessen „Virtueller Host“ leer ist, wird beim Zugriff über einen virtuellen Host nicht angezeigt.
Ein Label kann nur einen virtuellen Host haben. Sollen mehrere Mandanten dasselbe Label sehen, legen Sie daher pro Mandant ein Label mit gleichem Namen und gleichem Wert an und tragen jeweils dessen Schlüssel unter „Virtueller Host“ ein.
Dasselbe gilt für Schlüsselübereinstimmung, Verwandter Inhalt und Verwandte Abfrage: Einstellungen mit leerem „Virtueller Host“ werden auf den Hosts der Mandanten nicht verwendet.

Schritt 4: Virtuellen Host und Berechtigungen in der Crawl-Konfiguration angeben
================================================================================

Legen Sie unter [Crawler] > [Web] die Crawl-Konfiguration für Firma A an.
Die Crawl-Konfigurationen für Dateisysteme und Datenspeicher haben dieselben beiden Felder.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Feld
     - Wert
   * - Name
     - ``Portal Firma A``
   * - URLs
     - ``https://portal-a.example.com/``
   * - Eingeschlossene URLs
     - ``https://portal-a.example.com/.*``
   * - Berechtigungen
     - ``{role}tenanta_user`` (löschen Sie das standardmäßig eingetragene ``{role}guest``)
   * - Virtuelle Hosts
     - ``tenanta``

Lassen Sie ``{role}guest`` stehen, werden diese Dokumente beim Zugriff über die IP-Adresse und vor der Anmeldung sichtbar.

Für Dokumente, die mehrere Mandanten sehen sollen, etwa konzernweite Richtlinien, tragen Sie in einer einzigen Crawl-Konfiguration unter „Virtuelle Hosts“ und „Berechtigungen“ jeweils eine Zeile pro Mandant für beide Mandanten ein.

::

    Virtuelle Hosts:
    tenanta
    tenantb

    Berechtigungen:
    {role}tenanta_user
    {role}tenantb_user

Virtuelle Hosts und Berechtigungen werden beim Crawlen in die Dokumente geschrieben.
Ändern Sie sie in einer Konfiguration, die bereits gecrawlt wurde, wirkt sich das auf vorhandene Dokumente erst nach einem erneuten Crawlen aus.

Nach dem Speichern erstellen Sie entweder über [Neuen Job erstellen] im Detailbildschirm einen eigenen Job für den Mandanten, oder Sie führen unter [System] > [Scheduler] den ``Default Crawler`` mit [Jetzt starten] aus.

Schritt 5: Eine eigene Suchseite für jeden Mandanten vorbereiten
================================================================

In Fess 15.9 wird die Suchseite durch ein Theme dargestellt.
Installieren Sie ein Theme, dessen ``name`` in ``theme.yml`` dem Schlüssel in Kleinbuchstaben entspricht, wird es für Anfragen mit diesem Schlüssel verwendet.
Sie müssen es nicht als Standard-Theme festlegen; für Anfragen, die zu keinem Schlüssel passen, wird das Standard-Theme verwendet.

Erstellen Sie es als Kopie des mitgelieferten Themes ``bootstrap``.
Unter Docker holen Sie es wie folgt aus dem Container.

::

    $ docker cp fess01:/usr/share/fess/app/themes/bootstrap ./tenanta

1. Ändern Sie in ``tenanta/theme.yml`` den Wert ``name`` in ``tenanta`` und ``displayName`` beispielsweise in ``Suche Firma A``.
2. Ersetzen Sie ``assets/styles.css`` (Farben) sowie ``assets/logo-head.png`` und ``assets/logo.png`` (Logos). ``index.html`` muss nicht geändert werden.
3. Packen Sie alles so, dass ``theme.yml`` im Wurzelverzeichnis des ZIP-Archivs liegt.

   ::

       $ cd tenanta && zip -r ../tenanta.zip .

4. Laden Sie ``tenanta.zip`` unter [System] > [Theme] über [Hochladen] hoch.

Die Anmeldeseite (``/login/``) ist für alle Mandanten gleich und lässt sich nicht per Theme ändern.
Einzelheiten zum Kopieren des mitgelieferten Themes finden Sie im `Theme-Entwicklungsleitfaden <https://fess.codelibs.org/de/stable/dev/theme-development.html>`__.

Trennung überprüfen
===================

Bevor Sie das DNS umstellen, können Sie ``127.0.0.1 search-a.example.com search-b.example.com`` in Ihre lokale ``/etc/hosts`` eintragen und jeden Host im Browser ausprobieren, etwa über ``http://search-a.example.com:8080/`` ([Allgemein] braucht dafür die Zeilen mit Port).
Prüfen Sie die folgenden vier Fälle, indem Sie nach einem Wort suchen, das in den Crawl-Zielen vorkommt.

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - Zugriff
     - Erwartetes Ergebnis
   * - Benutzer von Firma A über ``search-a.example.com``
     - Nur Dokumente von Firma A erscheinen. Das einzige Label ist „Portal Firma A“. Die Seite wird mit dem Theme von Firma A angezeigt
   * - Benutzer von Firma A über ``search-b.example.com``
     - 0 Treffer (für die Dokumente von Firma B fehlt die Berechtigung, die Dokumente von Firma A schließt der virtuelle Host aus)
   * - Benutzer von Firma A über die IP-Adresse (``http://<Server>:8080/``)
     - Nur Dokumente von Firma A erscheinen (es gibt keine Filterung nach virtuellem Host, aber die Berechtigungen schützen sie)
   * - Zugriff ohne Anmeldung
     - Eine Suche ist erst nach der Anmeldung möglich

Haben Sie gemeinsame Dokumente für beide Mandanten angelegt, erscheinen diese in den Zeilen 1 bis 3 ebenfalls.
Erscheinen in Zeile 3 Dokumente von Firma B, steht in einer der Crawl-Konfigurationen noch ``{role}guest``.
Liefert Zeile 1 0 Treffer, vergleichen Sie die Zeilen in [Allgemein] (mit oder ohne Portnummer) mit der Schreibweise unter „Virtuelle Hosts“ in der Crawl-Konfiguration.

Dieselbe Prüfung ist auch mit der Such-API möglich.
Erstellen Sie unter [System] > [Zugriffstoken] ein Token mit der Berechtigung ``{role}tenanta_user`` und rufen Sie die API mit unterschiedlichen ``Host``-Headern auf.

::

    $ curl -s -H "Authorization: Bearer <Token von Firma A>" \
        -H "Host: search-a.example.com:8080" \
        "http://localhost:8080/api/v2/search?q=fess"
    $ curl -s -H "Authorization: Bearer <Token von Firma A>" \
        -H "Host: search-b.example.com:8080" \
        "http://localhost:8080/api/v2/search?q=fess"

Wie erwartet funktioniert es, wenn ``response.record_count`` beim ersten Aufruf 1 oder mehr und beim zweiten 0 ist.
Ein Zugriffstoken ist nicht an einen virtuellen Host gebunden; der virtuelle Host ergibt sich aus dem Hostnamen, an den die Anfrage gesendet wird.
Was ein Token sehen kann, bestimmen die Berechtigungen des Tokens. Geben Sie Tokens, die Sie an Systeme eines Mandanten weitergeben, daher immer nur die Rolle dieses Mandanten.
Zur Verwendung der API siehe :doc:`guide-11`.

Im laufenden Betrieb können Sie die Zahl der Suchen je virtuellem Host auf der Registerkarte [Zielgruppe] unter [Systeminformationen] > [Suchprotokoll] einsehen.

Mandanten hinzufügen und entfernen
==================================

Gehen Sie beim Hinzufügen eines Mandanten in der folgenden Reihenfolge vor, da spätere Schritte Werte aus früheren verwenden.

1. Unter [Allgemein] eine Zeile zu „Virtueller Host“ hinzufügen
2. Rolle, Benutzer und bei Bedarf Zugriffstokens anlegen
3. Labels (mit virtuellem Host und Berechtigungen) anlegen
4. Crawl-Konfigurationen (mit virtuellem Host und Berechtigungen) anlegen und crawlen
5. Das Theme hochladen
6. Die vier Fälle aus „Trennung überprüfen“ prüfen
7. Über DNS und Reverse Proxy veröffentlichen

Beim Entfernen eines Mandanten schließen Sie umgekehrt zuerst die Zugänge.

1. Den Hostnamen aus DNS und Reverse Proxy entfernen
2. Die Crawl-Konfigurationen und die dafür angelegten Jobs ([System] > [Scheduler]) löschen
3. Die Dokumente aus dem Index löschen (siehe unten)
4. Zugriffstokens, Benutzer und Rolle löschen
5. Labels, Schlüsselübereinstimmungen und andere Einstellungen für diesen Schlüssel sowie das Theme löschen
6. Die Zeile unter „Virtueller Host“ in [Allgemein] löschen

Das Löschen einer Crawl-Konfiguration entfernt die bereits gecrawlten Dokumente nicht aus dem Index.
Löschen Sie die Dokumente unter [Systeminformationen] > [Suche].
Dieser Bildschirm filtert weder nach Rollen noch nach virtuellen Hosts, daher sind die Dokumente aller Mandanten betroffen.
Suchen Sie im Suchfeld mit dem Label des Mandanten, etwa ``label:tenantb_docs``, vergewissern Sie sich, dass Anzahl und Ergebnisse nur Dokumente von Firma B enthalten, und klicken Sie dann auf [Alle mit dieser Abfrage löschen].
Bei Webdokumenten können Sie auch den Anfang der URL angeben, etwa ``site:portal-b.example.com``.

Verwenden Sie keine Angabe wie ``virtual_host:tenantb``.
``virtual_host`` gehört standardmäßig nicht zu den für die Suche verfügbaren Feldern. Der gesamte Ausdruck wird deshalb als Suche nach diesem Text im Dokumentinhalt behandelt und trifft nicht die beabsichtigten Dokumente.

Die Alternative: getrennte Instanzen
====================================

Wenn sich mehrere Mandanten ein Fess teilen, lassen sich die folgenden Punkte nicht trennen.

- Verwaltungsoberfläche und Administratoren: Jeder Administrator kann Einstellungen, Benutzer und Dokumente aller Mandanten bearbeiten
- Systemweite Einstellungen wie die Einstellungen unter [Allgemein] und die Wörterbücher
- Die Anmeldeseite

Wenn Sie die Verwaltung an die einzelnen Mandanten delegieren möchten oder Verträge getrennte Indizes verlangen, starten Sie pro Mandant ein eigenes Fess und verwenden unterschiedliche Indexnamen.
``compose/multi-instance`` in docker-fess verbindet zwei Fess-Instanzen (Ports 8080 und 8081) mit einem OpenSearch.

::

    $ git clone https://github.com/codelibs/docker-fess.git
    $ cd docker-fess
    $ git checkout v15.9.0
    $ cd compose/multi-instance
    $ docker compose -f compose.yaml -f compose-fess01.yaml -f compose-fess02.yaml up -d

In ``FESS_JAVA_OPTS`` jedes Fess sind die Indexnamen für Dokumente, Vorschläge, Crawling, Konfiguration, Benutzer, Protokolle und Wörterbücher (8 Einträge, z. B. ``-Dfess.config.index.document.search.index=fess01.search``) pro Instanz unterschiedlich.
Da auch Konfiguration und Benutzer nach Index getrennt sind, gelten Verwaltungsoberfläche, Benutzer und Suchprotokolle ebenfalls pro Mandant.
Um einen Mandanten hinzuzufügen, kopieren Sie ``compose-fess02.yaml`` und ändern Dienstname, Port und alle Indexnamen.

.. warning::

   Das OpenSearch in diesem Aufbau gibt Port 9200 frei, während das Security-Plugin deaktiviert ist.
   Wer Port 9200 erreicht, kann die Indizes aller Mandanten lesen. Schließen Sie den Port daher im Produktivbetrieb.

Weiterführende Artikel
======================

- Mehr über das Berechtigungsdesign mit Rollen, Gruppen und LDAP erfahren: :doc:`guide-05`
- Die Such-API aus den Systemen eines Mandanten aufrufen: :doc:`guide-11`
- Anmeldung per SSO und Zugriffsschutz einrichten: :doc:`guide-15`
- Fess und OpenSearch erweitern, wenn die Zahl der Mandanten wächst: :doc:`guide-14`
- Die Suchseite in eine bestehende Website einbetten: :doc:`guide-03`

Referenzen
==========

- `Virtueller Host <https://fess.codelibs.org/de/stable/config/security-virtual-host.html>`__
- `Multitenancy-Konfiguration <https://fess.codelibs.org/de/stable/config/multitenancy.html>`__
- `Konfiguration rollenbasierter Suche <https://fess.codelibs.org/de/stable/config/security-role.html>`__
- `Label <https://fess.codelibs.org/de/stable/admin/labeltype-guide.html>`__
- `Theme <https://fess.codelibs.org/de/stable/admin/theme-guide.html>`__
- `Suche <https://fess.codelibs.org/de/stable/admin/searchlist-guide.html>`__
- `docker-fess multi-instance (v15.9.0) <https://github.com/codelibs/docker-fess/tree/v15.9.0/compose/multi-instance>`__
