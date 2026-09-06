===========================
SharePoint Server-Konnektor
===========================

Übersicht
=========

Der SharePoint Server-Konnektor ruft Dokumentbibliothek-Dateien und Listenelemente aus einer
On-Premises-Installation von **SharePoint Server** (2013, 2016, 2019 oder Subscription Edition)
über dessen REST/OData-API ab (bei 2013 über dessen XML/Atom-API) und registriert sie im
|Fess|-Index.

Für diese Funktion ist das Plugin ``fess-ds-sharepoint`` erforderlich.

.. note::

   Wenn Sie stattdessen SharePoint Online (Microsoft 365) crawlen möchten, verwenden Sie
   :doc:`ds-microsoft365` und nicht diesen Konnektor. Die OAuth-Unterstützung dieses Konnektors
   deckt ausschließlich die anwendungsspezifische Authentifizierung (application-only) von Azure
   ACS ab und bietet keine Integration mit der Microsoft Graph API.

Unterstützte Versionen: SharePoint Server 2013 / 2016 / 2019 / Subscription Edition (SE)

Unterstützte Inhalte
====================

- Dokumentbibliothek-Dateien
- Listenelemente
- Anhänge von Listenelementen

Voraussetzungen
===============

1. Die Installation des Plugins ist erforderlich
2. Das Crawl-Konto benötigt Lesezugriff auf die zu crawlenden Sites, Listen und
   Dokumentbibliotheken
3. Wählen Sie genau eine Authentifizierungsmethode – NTLM, Kerberos (SPNEGO) oder OAuth (ACS) –
   und halten Sie deren Anmeldedaten bereit

Plugin-Installation
-------------------

Installieren Sie es über die Administrationsoberfläche unter "System" -> "Plugin":

1. Laden Sie ``fess-ds-sharepoint-X.X.X.jar`` herunter
2. Platzieren Sie es unter ``$FESS_HOME/app/WEB-INF/lib`` (oder
   ``/usr/share/fess/app/WEB-INF/lib``)
3. Starten Sie |Fess| neu

Details finden Sie unter :doc:`../../admin/plugin-guide`.

Konfiguration
=============

Konfigurieren Sie diesen Konnektor über die Administrationsoberfläche unter "Crawler" ->
"Datenspeicher" -> "Neu erstellen".

Grundeinstellungen
------------------

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Einstellung
     - Beispielwert
   * - Name
     - SharePoint
   * - Handler-Name
     - SharePointDataStore
   * - Aktiviert
     - Ein

Parameter-Einstellungen
-----------------------

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

Parameterliste
~~~~~~~~~~~~~~

**URL / Site**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``url``
     - Ja
     - Basis-URL des SharePoint-Servers, z. B. ``http://sharepoint.example.com/``
   * - ``site.name``
     - Bedingt
     - Name der Site-Sammlung, die unter ``/sites/<site.name>/`` gecrawlt wird. Nicht
       erforderlich, wenn ``site.path`` gesetzt ist
   * - ``site.path``
     - Nein
     - Serverrelativer verwalteter Pfad der Site (z. B. ``/teams/eng``; für die
       Root-Site-Sammlung ``/`` verwenden). Wenn gesetzt, wird dieser Wert unverändert anstelle
       des fest codierten ``/sites/``-Präfixes verwendet, und ``site.name`` ist dann nicht mehr
       erforderlich
   * - ``site.list_id``
     - Nein
     - Eine einzelne Liste anhand ihrer GUID crawlen (Listen-Crawl-Modus)
   * - ``site.list_name``
     - Nein
     - Eine einzelne Liste anhand ihres Anzeigenamens crawlen (Listen-Crawl-Modus)
   * - ``site.doclib_path``
     - Nein
     - Pfad der Dokumentbibliothek unterhalb der Site (Dokumentbibliothek-Crawl-Modus), z. B.
       ``/Shared Documents``
   * - ``site.exclude_list``
     - Nein
     - Kommagetrennte Regex-Muster für auszuschließende Listen-Entitätstypnamen. Gilt nur für
       einen Crawl der gesamten Site
   * - ``site.exclude_folder``
     - Nein
     - Kommagetrennte Regex-Muster für auszuschließende Titel von Ordnern der obersten Ebene.
       Gilt nur für einen Crawl der gesamten Site
   * - ``site.crawl_subsites``
     - Nein
     - Rekursiv in die Subsites der Site absteigen (Standard: ``false``). Siehe `Subsites und
       verwaltete Pfade`_
   * - ``site.max_depth``
     - Nein
     - Wie viele Subsite-Ebenen ``site.crawl_subsites`` rekursiv durchlaufen darf (Standard:
       ``10``); die Root-Site hat Tiefe 0

**Authentifizierung**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``auth.ntlm.user``
     - Nein
     - NTLM-Benutzername. Durch das Setzen wird NTLM aktiviert (``DOMAIN\user`` funktioniert)
   * - ``auth.ntlm.password``
     - Nein
     - NTLM-Passwort
   * - ``auth.ntlm.domain``
     - Nein
     - Windows-Domäne, die als eigenes NTLM-Feld gesendet wird
   * - ``auth.ntlm.workstation``
     - Nein
     - Workstation-Name, der bei der NTLM-Aushandlung gesendet wird
   * - ``auth.kerberos.principal``
     - Nein
     - Client-Principal, geschrieben als ``user@REALM``. Durch das Setzen wird Kerberos/SPNEGO
       aktiviert
   * - ``auth.kerberos.keytab``
     - Nein
     - Pfad zu einer Keytab-Datei mit einem Schlüssel für den Principal. Schließt sich mit
       ``auth.kerberos.password`` gegenseitig aus
   * - ``auth.kerberos.password``
     - Nein
     - Das Passwort des Principals, wird nur verwendet, wenn keine Keytab-Datei gesetzt ist
   * - ``auth.kerberos.strip_port``
     - Nein
     - Entfernt den Port aus dem Service Principal Name (Standard: ``true``)
   * - ``auth.kerberos.use_canonical_hostname``
     - Nein
     - Löst den Zielhost vor dem Erstellen des Service Principal Name in seinen kanonischen
       Namen auf (Standard: ``false``)
   * - ``auth.kerberos.krb5_conf``
     - Nein
     - Pfad zu einer ``krb5.conf``. Wird nur angewendet, wenn ``java.security.krb5.conf`` noch
       nicht gesetzt ist
   * - ``auth.kerberos.debug``
     - Nein
     - Aktiviert die Debug-Ausgabe von ``Krb5LoginModule`` (Standard: ``false``)
   * - ``auth.oauth.client_id``
     - Nein
     - Azure-ACS-OAuth-Client-ID für die anwendungsspezifische Authentifizierung. Durch das
       Setzen wird OAuth aktiviert
   * - ``auth.oauth.client_secret``
     - Nein
     - OAuth-Client-Secret
   * - ``auth.oauth.tenant``
     - Nein
     - Mandantenname ohne ``.sharepoint.com``
   * - ``auth.oauth.realm``
     - Nein
     - Azure-AD-Realm/Verzeichnis-ID

Es darf **genau eines** von ``auth.kerberos.principal``, ``auth.ntlm.user`` und
``auth.oauth.client_id`` gesetzt werden. Siehe `Authentifizierung`_ weiter unten.

**Liste**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``list.items.number_per_page``
     - Nein
     - Seitengröße für ``GetListItems`` (Standard: ``100``)
   * - ``list.item.content.include_fields``
     - Nein
     - Kommagetrennte Feldnamen; wenn gesetzt, werden nur diese Listenelement-Felder zu
       ``content`` zusammengefügt
   * - ``list.item.content.exclude_fields``
     - Nein
     - Kommagetrennte Feldnamenmuster (jeweils als Regex behandelt), die zusätzlich zu einer
       umfangreichen fest eingebauten Menge an Standardfeldern von ``content`` ausgeschlossen
       werden
   * - ``list.is_sub_page``
     - Nein
     - Behandelt Listenelemente als SitePages-/Wiki-Unterseiten; wirkt sich auf den
       Paging-Fallback und die Form des Weblinks aus (Standard: ``false``)

**HTTP**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``http.connection_timeout``
     - Nein
     - HTTP-Verbindungs-Timeout in ms; wird auch als Wartezeit-Timeout für den Connection-Pool
       verwendet (Standard: ``30000``)
   * - ``http.socket_timeout``
     - Nein
     - HTTP-Socket-Timeout (Lesevorgang) in ms (Standard: ``30000``)
   * - ``proxy_host``
     - Nein
     - HTTP-Proxy-Host
   * - ``proxy_port``
     - Bedingt
     - HTTP-Proxy-Port; erforderlich, wenn ``proxy_host`` gesetzt ist (Standard: ``-1`` = kein
       Proxy)

**Filterung und Inhalt**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``include_pattern``
     - Nein
     - Regex, dem der Wert eines Elements entsprechen muss, damit es gecrawlt wird. Welcher
       Wert das genau ist, siehe Hinweis unter dieser Tabelle
   * - ``exclude_pattern``
     - Nein
     - Regex, das ein übereinstimmendes Element vom Crawling ausschließt
   * - ``supported_mimetypes``
     - Nein
     - Kommagetrennte Regex-Ausdrücke, von denen der MIME-Typ einer Datei mindestens einem
       entsprechen muss (Standard: ``.*``)
   * - ``max_content_length``
     - Nein
     - Maximale Dateigröße in Bytes; eine Datei über diesem Limit wird übersprungen, nicht als
       Fehler behandelt (Standard: ``-1`` = kein Limit)
   * - ``extractor_name``
     - Nein
     - Fallback-Extraktor, der nur für einen MIME-Typ verwendet wird, den die Extractor-Factory
       nicht zuordnen kann (Standard: ``tikaExtractor``)

**Verhalten**

.. list-table::
   :header-rows: 1
   :widths: 25 15 60

   * - Parameter
     - Erforderlich
     - Beschreibung
   * - ``sp.version``
     - Nein
     - Auf ``2013`` setzen, um für SharePoint 2013 auf die XML/Atom-API-Familie
       ``GetXxxByServerRelativeUrl`` umzuschalten (nicht gesetzt ⇒ REST-Dialekt von SharePoint
       Online / 2016+)
   * - ``retry_limit``
     - Nein
     - Maximale Anzahl an Wiederholungsversuchen pro Crawl-Einheit bei einer
       SharePoint-Server-/Client-Exception (Standard: ``2``)
   * - ``role.skip``
     - Nein
     - Überspringt das Abrufen der Berechtigungen pro Element vollständig (Standard: ``false``).
       Siehe `Berechtigungen`_
   * - ``ignore_error``
     - Nein
     - Protokolliert einen Fehler bei der Inhaltsextraktion einer Datei und überspringt ihn,
       anstatt das Crawl-Ziel fehlschlagen zu lassen (Standard: ``false``)
   * - ``default_permissions``
     - Nein
     - Kommagetrennte Berechtigungszeichenfolgen, die zusätzlich zu den von SharePoint
       zurückgegebenen Werten in die Rollenliste jedes Dokuments eingemischt werden
   * - ``delete_old_docs``
     - Nein
     - Ob Dokumente gelöscht werden, die in diesem Durchlauf nicht aktualisiert wurden (Standard
       im Kern: ``true``). Dieses Plugin erzwingt für den aktuellen Durchlauf den Wert
       ``false``, sobald irgendein Crawl-Ziel fehlgeschlagen ist
   * - ``number_of_threads``
     - Nein
     - Wie viele Crawl-Ziele gleichzeitig bearbeitet werden (Standard: ``1`` = kein Thread-Pool),
       gedeckelt auf das Doppelte der Prozessoranzahl. Siehe `Paralleles Crawling und Last`_
   * - ``script_type``
     - Nein
     - Skript-Engine für das Skript der Datenspeicher-Konfiguration (Standard: ``groovy``)
   * - ``readInterval``
     - Nein
     - Wartezeit zwischen aufeinanderfolgenden Crawl-Ergebnissen, in ms (Standard: ``0``).
       Beachten Sie die camelCase-Schreibweise, die von allen anderen Parametern hier abweicht

Skript-Einstellungen
--------------------

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

Verfügbare Felder
~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 16 20 32 32

   * - Schlüssel
     - Listenelement (ItemCrawl)
     - Dokumentbibliothek-Datei (FolderCrawl->FileCrawl)
     - Anhang (ItemAttachmentsCrawl->FileCrawl)
   * - ``url``
     - Weblink
     - Datei-URL
     - Datei-URL
   * - ``host``
     - Hostname
     - Hostname
     - Hostname
   * - ``site``
     - Serverrelativer Pfad (``FileRef``)
     - Serverrelativer Pfad
     - Serverrelativer Pfad
   * - ``title``
     - ``Title``-Feld, sonst ``FileLeafRef``/Dateiname
     - Der eigene ``Title``-Listenwert der Dokumentbibliothek-Datei, falls vorhanden, sonst
       Dateiname
     - Dateiname
   * - ``titleWithListName``
     - ``"[listName] title"``
     - ``"[listName] filename"`` (der Listenname ist bei einem Dokumentbibliothek-Crawl immer
       leer, es bleibt also praktisch nur der Dateiname)
     - ``"[listName] filename"``
   * - ``listName``
     - Anzeigename der Liste, oder ``""``
     - Immer ``""``
     - Tatsächlicher Listenname
   * - ``content``
     - Verkettung der Feldwerte
     - Extrahierter Text
     - Extrahierter Text
   * - ``digest``
     - Gekürzter ``content``
     - Gekürzter ``content``
     - Gekürzter ``content``
   * - ``content_length``
     - ``content.length()``
     - ``content.length()``
     - ``content.length()``
   * - ``last_modified``
     - Aus der Listenabfrage
     - Aus der Listenabfrage
     - Aus der Listenabfrage
   * - ``created``
     - Aus der Listenabfrage
     - Aus der Listenabfrage
     - Aus der Listenabfrage
   * - ``mimetype``
     - Immer ``text/html``
     - Erkannt
     - Erkannt
   * - ``filetype``
     - Abgeleitet von ``mimetype``
     - Abgeleitet von ``mimetype``
     - Abgeleitet von ``mimetype``
   * - ``role``
     - Berechtigungsliste, nur wenn nicht leer
     - Berechtigungsliste, nur wenn nicht leer
     - Berechtigungsliste, nur wenn nicht leer
   * - ``list_name``
     - Vorhanden
     - **Nicht vorhanden**
     - Vorhanden
   * - ``list_id``
     - Vorhanden
     - **Nicht vorhanden**
     - Vorhanden
   * - ``item_id``
     - Vorhanden
     - **Nicht vorhanden**
     - Vorhanden

.. note::

   ``content_length`` ist ``content.length()`` – also die Zeichenanzahl (UTF-16-Codeeinheiten)
   des extrahierten bzw. verketteten Textes, nicht die Bytegröße der Datei. Das unterscheidet
   sich von ``file.size`` in den Konnektoren für Box, Google Drive und Dropbox, das die
   tatsächliche Bytegröße aus den jeweiligen Datei-Metadaten der Dienste ist. Vergleichen Sie
   ``content_length`` dieses Konnektors nicht mit jenen Werten.

**Dynamische Schlüssel: ``val_*``**

Jeder Schlüssel der ``FieldValuesAsText`` eines Listenelements (die rohe Feldwert-Map, die
SharePoint für dieses Element zurückgibt, einschließlich OData-Metadatenschlüsseln wie
``odata.metadata``) wird unter zwei Namen bereitgestellt: einmal ohne Präfix (nur wenn dieser
Name nicht bereits einem der oben genannten festen Schlüssel entspricht) und immer mit dem
Präfix ``val_`` – ein Feld ``Status`` wird also sowohl zu ``Status`` als auch zu ``val_Status``.

``val_*``-Schlüssel gibt es nur auf dem **Listenelement-Crawl-Pfad (ItemCrawl)**. Eine
Dokumentbibliothek-Datei (FolderCrawl->FileCrawl) oder ein Anhang eines Listenelements
(ItemAttachmentsCrawl->FileCrawl) erzeugt niemals einen ``val_*``-Schlüssel.

Authentifizierung
=================

Es stehen drei Authentifizierungsmethoden zur Verfügung, von denen **genau eine konfiguriert
werden darf**. Werden mehr als eines von ``auth.kerberos.principal``, ``auth.ntlm.user`` und
``auth.oauth.client_id`` gesetzt, schlägt der Datenspeicher-Konfigurationsjob mit einem
Validierungsfehler fehl, bevor überhaupt eine Anfrage gestellt wird. Das ist beabsichtigt: Beim
HTTP-Client wird nur ein einziges Credential registriert, und der Scope, unter dem es registriert
wird, passt ebenso gut auf eine ``Negotiate``-Challenge wie auf eine ``NTLM``-Challenge. Würde
man mehr als eines konfigurieren, kämen andernfalls 401-Fehler zustande, die im Log durch nichts
erklärt werden.

NTLM
----

::

    auth.ntlm.user={SharePoint-Benutzername}
    auth.ntlm.password={Passwort}
    auth.ntlm.domain={Windows-Domäne. Optional; standardmäßig nicht gesetzt.}
    auth.ntlm.workstation={Workstation-Name, der bei der NTLM-Aushandlung gesendet wird. Optional; standardmäßig nicht gesetzt.}

``auth.ntlm.domain`` und ``auth.ntlm.workstation`` sind standardmäßig beide nicht gesetzt,
wodurch genau das Credential entsteht, das dieser Konnektor schon immer gebaut hat. Die Domäne
weiterhin als ``DOMAIN\user`` in den Benutzernamen zu schreiben, funktioniert nach wie vor. Wird
``auth.ntlm.domain`` gesetzt, wird die Domäne stattdessen als eigenes NTLM-Feld gesendet – das
ist es, was ein Server erwartet, der die kombinierte Form ablehnt.

Kerberos (SPNEGO)
-----------------

**Unterstützter Rahmen:** eine einzelne Crawler-JVM, eine ``krb5.conf`` pro Fess-Instanz, eine
Keytab-Datei oder ein Passwort, keine Delegation, kein Channel Binding, und gegenseitig
ausschließend zu NTLM und OAuth. Alles außerhalb dieses Rahmens wird nicht unterstützt.

::

    auth.kerberos.principal={Client-Principal, geschrieben als user@REALM. Durch das Setzen wird Kerberos aktiviert.}
    auth.kerberos.keytab={Pfad zu einer Keytab-Datei mit einem Schlüssel für den Principal. Schließt sich mit auth.kerberos.password gegenseitig aus.}
    auth.kerberos.password={Das Passwort des Principals. Wird nur verwendet, wenn keine Keytab-Datei gesetzt ist.}
    auth.kerberos.strip_port={true oder false. Entfernt den Port aus dem Service Principal Name. Standard ist true.}
    auth.kerberos.use_canonical_hostname={true oder false. Löst den Zielhost für den Service Principal Name in seinen kanonischen Namen auf. Standard ist false.}
    auth.kerberos.krb5_conf={Pfad zu einer krb5.conf. Wird nur angewendet, wenn java.security.krb5.conf noch nicht gesetzt ist.}
    auth.kerberos.debug={true oder false. Debug-Ausgabe von Krb5LoginModule. Standard ist false.}

- **``krb5.conf`` gehört in ``jvm.crawler.options``**, etwa als
  ``-Djava.security.krb5.conf=/path/to/krb5.conf``. Das Crawling von Datenspeichern läuft im
  **Kindprozess** des Crawlers, daher hat es keine Wirkung, diese Einstellung irgendwo zu setzen,
  das nur die Webapp betrifft, und ein Neustart der Webapp übernimmt eine Änderung nicht – der
  Crawl-Job muss erneut ausgeführt werden. ``auth.kerberos.krb5_conf`` ist eine Erleichterung für
  den Fall, dass diese Eigenschaft noch von nichts gesetzt wurde: Sie **überschreibt niemals
  einen bereits gesetzten Wert**, da die Eigenschaft JVM-global ist und eine einzelne
  Crawler-JVM innerhalb eines Crawl-Jobs jede Datenspeicher-Konfiguration ausführt. Wenn sie das
  Überschreiben verweigert, protokolliert sie eine Warnung, die beide Pfade nennt.
- **Setzen Sie ``udp_preference_limit = 1`` im Abschnitt ``[libdefaults]`` von ``krb5.conf``.**
  Ohne diese Einstellung versucht das JDK zuerst UDP, und wenn der KDC nicht antwortet (nicht
  erreichbar, eine Firewall verwirft UDP 88, oder die Antwort ist größer als die
  Datagrammgröße), wiederholt es dreimal je dreißig Sekunden, bevor es auf TCP zurückfällt. Ein
  Crawl, der pro Authentifizierung etwa anderthalb Minuten lang hängen zu bleiben scheint, ohne
  dass etwas im Log steht, hat meist diese Ursache.
- **Schreiben Sie den Principal immer als ``user@REALM``.** ``default_realm`` ist JVM-global,
  und mehrere SharePoint-Farmen in unterschiedlichen Realms müssen sich unter Umständen eine
  ``krb5.conf`` teilen, sodass ein bloßes ``user`` gegen den Realm aufgelöst wird, den diese
  Datei zufällig nennt.
- **``auth.kerberos.use_canonical_hostname`` ist standardmäßig ``false``** – bewusst abweichend
  vom eigenen Standardwert von Apache HttpClient. Ist es aktiviert, wird der Zielhost vor dem
  Erstellen des Service Principal Name einer Reverse-DNS-Auflösung unterzogen, was bei
  alternativen Access Mappings oder hinter einem Load Balancer einen Namen erzeugen kann, für
  den kein SPN registriert ist – und der daraus resultierende Fehler lässt in keiner Weise auf
  DNS als Ursache schließen. Aktivieren Sie es nur, wenn der SPN wirklich gegen den kanonischen
  Namen registriert ist.
- **IIS Extended Protection mit ``tokenChecking=Require`` kann nicht funktionieren.** Weder
  Apache HttpClient 4.5 noch 5.x unterstützt Channel Binding. IIS setzt diesen Wert
  standardmäßig auf ``None``, sodass dies meist nicht zutrifft; trifft es doch zu, gibt es keine
  Umgehungsmöglichkeit.
- **Das Ticket wird nur einmal beim Erstellen des HTTP-Clients für den Crawl abgerufen und
  danach nie erneuert.** Ein Crawl, der länger läuft als die Gültigkeitsdauer des Tickets,
  beginnt mittendrin, bei der Authentifizierung zu scheitern.
- **``auth.kerberos.password`` wird, genau wie ``auth.ntlm.password``, im Klartext gespeichert
  und angezeigt.** Fess besitzt keinen Maskierungsmechanismus für Parameter von
  Datenspeicher-Handlern; der Bearbeitungsbildschirm der Datenspeicher-Konfiguration stellt sie
  als einfaches Textfeld im Klartext dar. Bevorzugen Sie ``auth.kerberos.keytab`` und vergeben
  Sie für die Keytab-Datei restriktive Zugriffsrechte.
- ``auth.kerberos.debug=true`` bewirkt, dass ``Krb5LoginModule`` in die Standardausgabe des
  Crawler-Prozesses schreibt, nicht in das Fess-Log.

OAuth (ACS)
-----------

::

    auth.oauth.client_id={OAuth-Client-ID}
    auth.oauth.client_secret={OAuth-Client-Secret}
    auth.oauth.tenant={Mandantenname ohne .sharepoint.com}
    auth.oauth.realm={Azure-AD-Realm/Verzeichnis-ID}

Durch das Setzen von ``auth.oauth.client_id`` wird ein Client-Credentials-Flow
(anwendungsspezifisch) gegen den Windows Azure Access Control Service aktiviert,
``https://accounts.accesscontrol.windows.net/{realm}/tokens/OAuth/2``. Das Access Token wird
einmal beim Erstellen des HTTP-Clients für den Crawl abgerufen, bei jeder Anfrage als
``Bearer``-``Authorization``-Header angewendet und bei einem 401 einmal erneuert und erneut
versucht. **Microsoft hat ACS als veraltet eingestuft und dessen Abschaltung angekündigt**;
dieser Konnektor protokolliert bei jedem OAuth-konfigurierten Crawl eine entsprechende Warnung.
Ein Entra-ID-App-Registrierungsflow (per Zertifikat oder Client-Secret) ist hier nicht
implementiert – nur die veraltete anwendungsspezifische ACS-Authentifizierung.

Bevor OAuth verdrahtet wird, wird nur geprüft, ob ``auth.oauth.client_id`` vorhanden ist;
``client_secret``, ``tenant`` und ``realm`` werden bedingungslos gelesen und können, wenn sie
weggelassen werden, stillschweigend leer bleiben – das lässt den Tokenerwerb scheitern, ohne
dass eine eigene Validierungsmeldung erscheint.

**``sp.version=2013`` und OAuth haben noch nie zusammen funktioniert.** Jeder API-Aufruf, den
dieser Konnektor für SharePoint 2013 ausführt, läuft über den XML/Atom-Client, und kein
Codepfad in diesem Client hängt einer Anfrage ein OAuth-Token an – sind also beide gesetzt, wird
jede Anfrage unauthentifiziert gesendet. Der Crawl protokolliert eine Warnung mit genau diesem
Sachverhalt und nennt ``auth.ntlm.*`` als Alternative; der Job schlägt dadurch nicht fehl.
Verwenden Sie für SharePoint 2013 ``auth.ntlm.*``.

Berechtigungen
==============

``role.skip=true`` (Standard ``false``) überspringt das Abrufen der Berechtigungen pro Element
vollständig: Es wird kein ``GetListItemRole``-Aufruf gemacht, es wird nie ein ``role``-Schlüssel
für das Element gesetzt, und das Dokument trägt am Ende nur die statische Permission-Einstellung
der Datenspeicher-Konfiguration sowie, falls konfiguriert, ``default_permissions`` – von
SharePoint abgeleitete Berechtigungen erreichen es überhaupt nicht.

Wenn Rollen abgerufen werden, werden SharePoints eigene Benutzer, Sicherheitsgruppen und
SharePoint-Gruppen expandiert und auf Fess-Suchrollen abgebildet:

- Ein **On-Premises-AD**-Konto oder eine solche Gruppe (Anmeldename enthält einen Backslash und
  beginnt nicht mit einem Azure-Claim-Präfix) wird über die Standard-Rollenhelfer für
  AD-Benutzer/-Gruppen abgebildet.
- Ein **Azure-AD-(Entra-ID-)**-Konto (Anmeldename beginnt mit ``i:0#.f|membership|``) wird
  **zweimal** abgebildet – einmal über den vollständigen Azure-Claim-Wert, einmal über den
  AD-Kontoanteil vor dem ``@`` in diesem Claim –, sodass für denselben Benutzer sowohl eine
  Rolle im Entra-ID-Stil als auch eine im AD-Stil hinzugefügt wird. Eine Sicherheitsgruppe, die
  als Azure-Gruppe erkannt wird (anhand eines von mehreren Claim-Stil-Präfixen, darunter die
  spezielle "Alle"-Gruppe ``spo-grid-all-users``), wird auf dieselbe Weise in beiden Formen
  abgebildet.
- Bei einer **SharePoint-Gruppe** wird deren eigene Mitgliedschaft (Benutzer,
  Sicherheitsgruppen, verschachtelte Gruppen) rekursiv expandiert, wobei eine Schutzmaßnahme
  gegen bereits besuchte Gruppen unendliche Rekursion zwischen Gruppen verhindert, die sich
  gegenseitig enthalten.

``default_permissions`` (kommagetrennt) wird **nach** all dem Vorstehenden eingemischt und gilt
selbst dann, wenn SharePoint für das Element überhaupt keine Rolle zurückgegeben hat – der Fall,
den sowohl ``role.skip=true`` als auch "SharePoint hat nichts zurückgegeben" erzeugen. Die
endgültige Rollenliste ist die – dedupliziert – Vereinigung aus der statischen
Permission-Einstellung der Datenspeicher-Konfiguration, den von SharePoint abgeleiteten Rollen
(sofern nicht übersprungen) und ``default_permissions``.

Subsites und verwaltete Pfade
=============================

Wird ``site.path`` gesetzt, wird der angegebene serverrelative verwaltete Pfad unverändert
anstelle des fest codierten ``/sites/``-Präfixes verwendet, und ``site.name`` ist dann nicht
mehr erforderlich.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Szenario
     - Einstellung
   * - Root-Site-Sammlung
     - ``site.path=/``
   * - Die Site ``/teams/eng``
     - ``site.path=/teams/eng``
   * - Die klassische Form ``/sites/mysite/``
     - ``site.name=mysite`` (``site.path`` nicht setzen)

Wird ``site.crawl_subsites`` (Standard ``false``) gesetzt, steigt ein vollständiger Site-Crawl –
also einer, bei dem weder ``site.list_name`` noch ``site.doclib_path`` gesetzt ist – rekursiv in
die Subsites der Site ab, die über ``_api/web/webinfos`` ermittelt werden. Bleibt der Parameter
ungesetzt, stellt der Crawl weiterhin exakt dieselben Anfragen wie bisher, einschließlich der
Tatsache, dass ``webinfos`` überhaupt nie angefragt wird.

Die Dokumente einer Subsite landen in derselben Datenspeicher-Konfiguration wie die der
Root-Site, unter ihren eigenen serverrelativen Pfaden – im Index gibt es nichts, das ein
Dokument als von einer Subsite statt von der Root-Site stammend kennzeichnet.

``site.max_depth`` (Standard ``10``) begrenzt, wie viele Subsite-Ebenen unterhalb der Root-Site
gecrawlt werden, sobald ``site.crawl_subsites=true`` gilt. Die Root-Site selbst hat Tiefe 0,
sodass ``site.max_depth=1`` nur die direkten Kinder der Root-Site crawlt und nicht weiter. Wird
bei ``site.crawl_subsites=true`` ein Wert unter ``1`` gesetzt, schaltet das die Funktion wieder
ab – es wird dann überhaupt keine Subsite gecrawlt – und dies wird beim Start des Crawls als
Warnung protokolliert.

Das Aktivieren des Subsite-Crawlings **vervielfacht die Gesamtdauer des Crawls** ungefähr um die
Anzahl der gefundenen Subsites (begrenzt durch ``site.max_depth``): Jede Subsite erhält ihre
eigene vollständige Ordner- und Listenauflistung sowie, falls die Tiefenbegrenzung noch nicht
erreicht ist, ihren eigenen ``webinfos``-Aufruf – zusätzlich zu allem, was der Crawl der
Root-Site ohnehin schon leistet.

``number_of_threads`` und ``readInterval``, beschrieben unter `Paralleles Crawling und Last`_,
gelten für einen rekursiven Subsite-Crawl genauso wie für jeden anderen Crawl.

Paralleles Crawling und Last
============================

``number_of_threads`` (Standard ``1``) gibt an, wie viele Crawl-Ziele gleichzeitig bearbeitet
werden. Beim Standardwert läuft der Crawl exakt wie bisher: Jedes Ziel wird auf dem
Crawling-Thread gecrawlt, und **es wird überhaupt kein Thread-Pool erstellt**.

Der Wert wird auf **das Doppelte der Prozessoranzahl** der Maschine gedeckelt, auf der Fess
läuft, damit eine Datenspeicher-Konfiguration nicht mehr Parallelität anfordern kann, als der
Host leisten kann. Ein Wert unter ``1`` – oder ein leerer bzw. nicht parsbarer Wert – fällt auf
``1`` zurück, anstatt berücksichtigt zu werden oder den Job scheitern zu lassen. Wurde ein Wert
gedeckelt oder lag er unter ``1``, werden sowohl der angeforderte als auch der tatsächliche Wert
protokolliert; ein nicht parsbarer Wert protokolliert eine Warnung. Ein leerer Wert protokolliert
nichts, da ein leeres Feld lediglich bedeutet, dass der Parameter schlicht nicht gesetzt wurde.

Der HTTP-Connection-Pool wird entsprechend dimensioniert. Apache HttpClient erlaubt
standardmäßig nur 2 Verbindungen pro Route, und ein gesamter Crawl gilt als eine einzige Route:
Ohne diese Anhebung würde jeder Thread ab dem dritten seine Zeit damit verbringen, auf eine
Verbindung zu warten, statt Anfragen zu stellen.

**``readInterval`` taktet die Übergabe der Dokumente weiterhin mit einem Dokument pro Intervall,
unabhängig davon, worauf es gesetzt ist.** Threads machen das Auffinden und Abrufen beim Crawl
schneller; sie machen nicht, dass Dokumente schneller beim Indexer ankommen. Das ist
beabsichtigt: Das vom Betreiber konfigurierte Intervall durch die Thread-Anzahl zu teilen, würde
genau die Last vervielfachen, die dieses Intervall eigentlich begrenzen soll. Ein Worker, der
ein Dokument fertigbearbeitet hat, während vorherige Dokumente noch übergeben werden, wartet
einfach.

Was das Erhöhen von ``number_of_threads`` tatsächlich vervielfacht, ist die Anfragerate
gegenüber SharePoint. Der weiter unten beschriebene 503-Backoff und die Wartezeit durch
``X-SharePointHealthScore`` werden pro Crawl-Ziel auf dem Thread angewendet, der es crawlt,
sodass ``n`` Threads bis zu ``n``-mal so viele Anfragen stellen wie ein einzelner Thread – auch
während eines Zeitraums, in dem die Farm signalisiert, dass sie ausgelastet ist. Erhöhen Sie
diesen Wert bei einer On-Premises-Farm nur schrittweise.

Zwei Dinge setzen dem tatsächlichen Nutzen zusätzlicher Threads eine Obergrenze:

- **Die Mitgliedschaft jeder SharePoint-Gruppe wird beim ersten Lesen jeweils nur von einem
  Thread nach dem anderen gelesen.** Berechtigungen werden über einen Cache aufgelöst, der sich
  über den gesamten Crawl erstreckt und durch eine einzelne Sperre geschützt wird, die während
  der Mitgliederabfrage einer Gruppe gehalten wird. Diese Sperre verhindert, dass ein Thread
  einem anderen eine Gruppe übergibt, deren Mitglieder noch gelesen werden – was dazu führen
  würde, dass die von dieser Gruppe geschützten Elemente ohne jede ihrer Berechtigungen
  indexiert werden. Sobald eine Gruppe im Cache liegt, ist jeder spätere Zugriff darauf eine
  billige Abfrage; es handelt sich also um **Cold-Cache-Kosten**: Der Crawl einer Site mit vielen
  unterschiedlichen Gruppen verbringt seine ersten Minuten näher an einem einzelnen Thread als
  an ``n`` Threads, während eine Site, deren Elemente sich eine Handvoll Gruppen teilen, davon
  kaum etwas merkt. ``role.skip=true``, das überhaupt keine Berechtigungen liest, vermeidet
  diese Kosten vollständig.
- Die Discovery erfolgt pro Site sequenziell: Die Ordner- und Listenauflistung einer Site bilden
  ein einziges Crawl-Ziel, sodass es für Threads nichts zu verteilen gibt, bis dieses Ziel
  abgeschlossen ist und seine Funde in die Warteschlange eingereiht hat.

**Eine 503-Antwort** wird wie jeder andere Fehler bis zu ``retry_limit``-mal erneut versucht,
jedoch mit einer vor jedem erneuten Versuch wachsenden Wartezeit: 2 Sekunden, dann 4, dann 8,
verdoppelnd bis zu einer Obergrenze von 30 Sekunden, jeweils zufällig auf 70–129 % dieses Werts
variiert. Ein Crawl-Ziel, das weiterhin 503 zurückgibt, zahlt diese Wartezeit vor jedem
tatsächlich stattfindenden erneuten Versuch, aber nicht nach dem letzten.

**Jede Antwort** – ob erfolgreich oder nicht, einschließlich einer Seite einer Auflistung, die
der Crawl gleich verwerfen wird – wird auf den Response-Header ``X-SharePointHealthScore``
(0 = im Leerlauf bis 10 = sehr ausgelastet) untersucht. Ein Wert von 9 oder darüber lässt den
Crawl warten, bevor irgendetwas anderes geschieht: Bei Score 9 wird etwa 2 Sekunden gewartet, bei
Score 10 etwa 4 Sekunden, und so weiter, wobei sich der Wert für jeden Punkt über 9 verdoppelt.
**Das summiert sich über den gesamten Crawl hinweg auf, ohne eine Obergrenze für die Summe**:
Eine Farm, die unter anhaltender Last bei Health Score 9 verharrt, fügt zu *jeder einzelnen
Anfrage* dieses Konnektors rund 2 Sekunden hinzu – einschließlich jeder Seite jeder Ordner- und
Listenauflistung –, wodurch aus einem Crawl, der sonst Stunden dauern würde, einer werden kann,
der erheblich länger dauert. Wenn sich ein Crawl unerwartet um eine Größenordnung verlangsamt,
prüfen Sie zuerst den Health Score der Farm in diesem Zeitraum, bevor Sie eine andere Ursache
vermuten.

Anwendungsbeispiele
===================

Alle folgenden Beispiele setzen NTLM voraus. Um stattdessen Kerberos oder OAuth zu verwenden,
siehe `Authentifizierung`_ und ersetzen Sie die ``auth.ntlm.*``-Zeilen.

Listen-Crawl
------------

Parameter:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.list_name=Tasks

Skript:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Dokumentbibliothek-Crawl
------------------------

Parameter:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.name=mysite
    site.doclib_path=/Shared Documents

Skript:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Crawlen einer ``/teams/``-Site
------------------------------

Mit ``site.path`` können Sie direkt auf eine Dokumentbibliothek einer Site unter einem anderen
verwalteten Pfad als ``/sites/`` verweisen.

Parameter:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/teams/eng
    site.doclib_path=/Shared Documents

Skript:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified

Rekursiver Subsite-Crawl
------------------------

Startet bei der Root-Site-Sammlung und folgt Subsites bis zu einer Tiefe von 3 Ebenen.

Parameter:

::

    url=http://sharepoint.example.com/
    auth.ntlm.user=DOMAIN\svc-fess
    auth.ntlm.password=changeit
    site.path=/
    site.crawl_subsites=true
    site.max_depth=3

Skript:

::

    url=url
    title=title
    content=content
    digest=digest
    content_length=content.length()
    last_modified=last_modified
    role=role

Einschränkungen
===============

- **Keinerlei inkrementelles oder Delta-Crawling.** Es gibt in diesem Konnektor nirgends ein
  Change-Token, eine Delta-Query oder eine Filterung nach "zuletzt geändert seit" – jeder
  Durchlauf listet vollständig jede Liste, jeden Ordner und jede Datei auf, die er erreichen
  soll. ``delete_old_docs`` steuert lediglich, ob Dokumente, die der aktuelle vollständige Crawl
  nicht erneut gesehen hat, im Nachhinein gelöscht werden; das ist nachträgliches Aufräumen,
  kein inkrementelles Abrufen.
- **``%`` und ``#`` in Datei-/Ordnernamen** werden auf dem Standard-Codepfad (nicht ``2013``)
  unterstützt. Nur SharePoint Server 2019 und die Subscription Edition lassen diese beiden
  Zeichen in einem Namen überhaupt zu; 2016 lehnt sie ausdrücklich weiterhin ab, und 2013
  ebenso. Der Standard-Codepfad erreicht eine solche Datei über die
  ``...ByServerRelativePath(decodedUrl=...)``-Endpunkte, die den dekodierten Pfad
  entgegennehmen, und der Crawl maskiert beide Zeichen zusätzlich in dem Link, unter dem er die
  Datei indexiert. **Mit ``sp.version=2013`` lässt sich eine solche Datei nicht erreichen**, da
  dieser Pfad die älteren ``...ByServerRelativeUrl(...)``-Endpunkte verwendet, die ihr Argument
  als bereits kodierte URL lesen. Das ist eine bewusste Einschränkung und keine Lücke: Eine
  SharePoint-2013-Farm kann einen solchen Namen gar nicht enthalten. Relevant wird es nur, wenn
  ``sp.version=2013`` gegen einen 2019- oder Subscription-Edition-Server verwendet wird, was
  keine zu verwendende Konfiguration ist. Siehe
  `Use of # and % characters in file and folder names
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2019>`__
  und `File names - expanded support for special characters
  <https://learn.microsoft.com/en-us/sharepoint/what-s-new/new-and-improved-features-in-sharepoint-server-2016>`__.
- **IIS Extended Protection mit ``tokenChecking=Require`` kann nicht unterstützt werden.** Weder
  Apache HttpClient 4.5 noch 5.x implementiert Channel Binding, worauf Extended Protection bei
  ``Require`` angewiesen ist. IIS setzt diese Einstellung standardmäßig auf ``None``, sodass die
  meisten Farmen nicht betroffen sind; für eine Farm, bei der ``Require`` gesetzt ist, gibt es
  keine Umgehungsmöglichkeit.
- **Passwörter in Parametern der Datenspeicher-Konfiguration werden im Klartext gespeichert und
  angezeigt.** Das gilt gleichermaßen für ``auth.ntlm.password`` und ``auth.kerberos.password``:
  Fess besitzt keinen Maskierungsmechanismus für Parameter von Datenspeicher-Handlern, und der
  Bearbeitungsbildschirm der Datenspeicher-Konfiguration stellt sie als einfaches Textfeld im
  Klartext dar. Bevorzugen Sie, wo Kerberos verfügbar ist, ``auth.kerberos.keytab`` gegenüber
  ``auth.kerberos.password``, und vergeben Sie für die Keytab-Datei restriktive Zugriffsrechte.
- **``sp.version=2013`` und OAuth haben noch nie zusammen funktioniert.** Jeder API-Aufruf für
  SharePoint 2013 läuft über den XML/Atom-Client, und kein Codepfad in diesem Client hängt einer
  Anfrage ein OAuth-Token an, sodass bei beiden gesetzten Werten jede Anfrage unauthentifiziert
  gesendet wird. Verwenden Sie für SharePoint 2013 ``auth.ntlm.*``.
- **Verwaltete Pfade außer ``/sites/`` und dem über ``site.path`` gesetzten werden weiterhin
  nicht von selbst entdeckt.** ``site.crawl_subsites`` steigt nur ausgehend von der
  konfigurierten Root-Site rekursiv ab, und ``site.path`` erreicht genau den einen von Ihnen
  gesetzten verwalteten Pfad, nicht jeden verwalteten Pfad auf der Farm.

Fehlerbehebung
==============

Authentifizierung schlägt lautlos fehl
--------------------------------------

**Symptom**: Anfragen liefern 401 (oder Ähnliches) zurück, ohne dass das Log einen klaren Grund
dafür nennt

**Zu überprüfen**:

1. Prüfen Sie, ob mehr als eines von ``auth.kerberos.principal``, ``auth.ntlm.user`` und
   ``auth.oauth.client_id`` gesetzt ist – zwei oder mehr lassen den Job vor Beginn des Crawls
   mit einem Validierungsfehler scheitern
2. Stellen Sie bei Kerberos sicher, dass ``-Djava.security.krb5.conf=...`` in
   ``jvm.crawler.options`` gesetzt ist. Wird es irgendwo gesetzt, das nur die Webapp betrifft,
   hat das keine Wirkung. Führen Sie nach einer Änderung den Crawl-Job erneut aus – ein Neustart
   der Webapp übernimmt die Änderung nicht
3. Stellen Sie bei Kerberos sicher, dass ``udp_preference_limit = 1`` im Abschnitt
   ``[libdefaults]`` von ``krb5.conf`` gesetzt ist. Ohne diese Einstellung kann ein nicht
   antwortender KDC dazu führen, dass jede Authentifizierung etwa 90 Sekunden lang hängen
   bleibt (drei UDP-Wiederholungen zu je 30 Sekunden), ohne dass etwas im Log steht
4. Stellen Sie sicher, dass der Principal als ``user@REALM`` geschrieben ist – ein bloßes
   ``user`` wird gegen den ``default_realm`` aufgelöst, den die gemeinsam genutzte
   ``krb5.conf`` zufällig nennt
5. Stellen Sie bei OAuth sicher, dass ``client_secret``, ``tenant`` und ``realm`` nicht leer
   sind – validiert wird nur, ob ``client_id`` vorhanden ist, sodass die übrigen stillschweigend
   leer bleiben können
6. Stellen Sie sicher, dass IIS Extended Protection nicht auf ``tokenChecking=Require`` gesetzt
   ist – für diese Einstellung gibt es keine Umgehungsmöglichkeit
7. Prüfen Sie bei einem lange laufenden Crawl, ob er erst mittendrin zu scheitern begonnen hat –
   das Kerberos-Ticket wird nur einmal beim Erstellen des HTTP-Clients abgerufen und nie
   erneuert, sodass ein Crawl, der die Ticketlaufzeit überdauert, mittendrin zu scheitern
   beginnt

Der Crawl ist langsam (503-Fehler und der Health Score)
-------------------------------------------------------

**Symptom**: Der Crawl dauert erheblich länger als erwartet oder läuft in ein Timeout

**Zu überprüfen**:

1. Prüfen Sie den ``X-SharePointHealthScore`` der SharePoint-Farm während des langsamen
   Zeitraums. Ein Wert von 9 oder darüber fügt vor jeder Anfrage eine Wartezeit hinzu (bei 9
   etwa 2 Sekunden, bei 10 etwa 4 Sekunden, sich danach verdoppelnd, ohne Obergrenze für die
   Summe), wodurch aus einem Crawl, der eigentlich Stunden dauern sollte, einer werden kann,
   der erheblich länger dauert
2. Prüfen Sie auf wiederholte 503-Antworten. Ein 503 wird bis zu ``retry_limit``-mal erneut
   versucht, wobei vor jedem Versuch 2, dann 4, dann 8 Sekunden (gedeckelt bei 30) gewartet wird
3. Prüfen Sie, ob ``number_of_threads`` zu stark erhöht wurde. Mehr Threads bedeuten ungefähr
   proportional mehr Anfragen gegenüber SharePoint, was den Health Score weiter nach oben
   treiben kann. Erhöhen Sie ihn bei einer On-Premises-Farm schrittweise
4. Denken Sie bei ``site.crawl_subsites=true`` daran, dass die Gesamtdauer des Crawls ungefähr
   mit der Anzahl der gefundenen Subsites wächst – erwägen Sie, den Umfang mit
   ``site.max_depth`` einzugrenzen

Es wird nichts indexiert
------------------------

**Symptom**: Der Crawl endet normal, aber die Suche liefert null Ergebnisse

**Zu überprüfen**:

1. Prüfen Sie das Crawler-Log auf Fehler oder Warnungen (setzen Sie ``org.codelibs.fess.ds`` in
   ``app/WEB-INF/env/crawler/resources/log4j2.xml`` auf ``DEBUG``)
2. Prüfen Sie ``url``, ``site.name`` (bzw. ``site.path``) und ``site.list_name`` auf Tippfehler –
   denken Sie daran, dass ``site.name`` nicht mehr benötigt wird, sobald ``site.path`` gesetzt
   ist
3. Stellen Sie sicher, dass die Authentifizierung tatsächlich erfolgreich ist (keine
   401-Fehler) – eine Anfrage, die nie authentifiziert wird, ist eine weitaus häufigere Ursache
   als ein falsch konfiguriertes ``role.skip`` oder ``default_permissions``
4. Denken Sie, falls ``include_pattern`` oder ``exclude_pattern`` gesetzt ist, daran, dass diese
   gegen einen serverrelativen Pfad (bei einer Dokumentbibliothek-Datei oder einem Anhang eines
   Listenelements) oder gegen ``FileRef`` (bei einem Listenelement) abgeglichen werden – nicht
   gegen die in den Suchergebnissen angezeigte URL. Prüfen Sie, ob ein Muster versehentlich für
   eine vollständige URL geschrieben wurde
5. Prüfen Sie, ob ``supported_mimetypes`` oder ``max_content_length`` die erwarteten Dateien
   ausschließt
6. Prüfen Sie, ob ``site.exclude_list`` oder ``site.exclude_folder`` das Ziel unbeabsichtigt
   ausschließt

Weiterführende Informationen
============================

- :doc:`ds-overview` - Übersicht der Datenspeicher-Konnektoren
- :doc:`ds-microsoft365` - Microsoft 365-Konnektor (für SharePoint Online)
- :doc:`../../admin/dataconfig-guide` - Leitfaden zur Datenspeicher-Konfiguration
- :doc:`../../admin/plugin-guide` - Leitfaden zur Plugin-Verwaltung
