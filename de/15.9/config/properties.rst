=============================
Fess Configuration Properties
=============================

Every configuration property Fess reads, with its description and its default value.
The values themselves live in ``fess_config.properties``; see :doc:`crawler-advanced`
for how to override them.

The tables below are generated from ``fess_config.properties``. To correct a
description, change the comment above the property in the Fess repository. To translate
one, fill in ``properties.po`` beside this file.

.. GENERATED-BEGIN: properties -- from fess_config.properties via tools/update_properties_doc.sh
.. DO NOT EDIT. Descriptions and headings come from fess_config.properties in the
.. fess repository; translations come from properties.po beside this file.
.. Regenerate with tools/update_properties_doc.sh.

Kern
----

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - domain.title
    - Der Titel der Domain für Protokollierung und Anzeige.
    - ``Fess``

.. list-table:: Suchmaschine
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - search_engine.type
    - Typ des Suchmaschinen-Backends. Zulässige Werte: default (OpenSearch mit den CodeLibs-Plugins), vanilla (OpenSearch ohne die CodeLibs-Plugins), aws (vanilla mit AWS-spezifischer Behandlung). cloud ist ein veralteter Alias für vanilla.
    - ``default``
  * - search_engine.http.url
    - Die URL des HTTP-Endpunkts der Suchmaschine. Verwenden Sie in IPv6-Umgebungen eckige Klammern um die IPv6-Adresse (z. B. http://[::1]:9200)
    - ``http://localhost:9200``
  * - search_engine.http.ssl.certificate_authorities
    - Pfad zu den SSL-Zertifizierungsstellen für sichere HTTP-Verbindungen.
    - (empty)
  * - search_engine.username
    - Benutzername für die Authentifizierung bei der Suchmaschine.
    - (empty)
  * - search_engine.password
    - Passwort für die Authentifizierung bei der Suchmaschine.
    - (empty)
  * - search_engine.heartbeat_interval
    - Intervall (ms) für Heartbeat-Prüfungen der Suchmaschine.
    - ``10000``
  * - app.cipher.algorithm
    - Für die Verschlüsselung verwendeter Cipher-Algorithmus.
    - ``aes``
  * - app.cipher.key
    - Geheimer Schlüssel für die Verschlüsselung (ändern Sie diesen Wert für den Produktionsbetrieb).
    - ``___change__me___``
  * - app.digest.algorithm
    - Algorithmus für die Digest-Berechnung.
    - ``sha256``
  * - app.password.algorithm
    - Passwort-Hashing (neuer Mechanismus, kompatibel mit Spring Security v5.8) Unterstützt: bcrypt (derzeit nur dieser)
    - ``bcrypt``
  * - app.password.bcrypt.cost
    - BCrypt-Kostenfaktor (Log-Runden). 10 entspricht dem Standardwert von Spring Security v5.8. Bereich: 4-31.
    - ``10``
  * - app.password.upgrade.enabled
    - Verzögertes erneutes Hashing bei erfolgreicher Anmeldung für Legacy-Hashes.
    - ``true``
  * - app.encrypt.property.pattern
    - HINWEIS: app.digest.algorithm bleibt nur für die Überprüfung von LEGACY-Passwörtern erhalten (Hashes von vor dem Upgrade, die kein {id}-Präfix haben). Nicht für neue Passwörter verwenden. Regex-Muster für zu verschlüsselnde Eigenschaften.
    - ``.*password|.*key|.*token|.*secret``
  * - app.log.sensitive.property.pattern
    - Regex-Muster für sensible Werte, die in Debug-Protokollen maskiert werden (Abgleich ohne Beachtung der Groß-/Kleinschreibung mit den Schlüsseln von Eigenschaften/Umgebungsvariablen).
    - ``.*password.*|.*secret.*|.*key.*|.*token.*|.*credential.*|.*auth.*|.*private.*``
  * - app.extension.names
    - Erweiterungsnamen für die Anwendungsanpassung.
    - (empty)
  * - app.audit.log.format
    - Format des Audit-Protokolls.
    - (empty)
  * - script.audit.log.enabled
    - Einstellungen für das Skript-Audit-Protokoll.
    - ``true``
  * - script.audit.log.max.length
    - Maximale Zeichenanzahl des Skripttexts, die in einem Skript-Audit-Protokolleintrag erhalten bleibt; längerer Text wird abgeschnitten.
    - ``100``
  * - jvm.crawler.options
    - JVM-Optionen für den Crawler-Prozess.
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Dhttp.maxConnections=20``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx512m``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:-OmitStackTraceInFastThrow``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=1m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=5``
      | ``-Djcifs.client.responseTimeout=30000``
      | ``-Djcifs.client.soTimeout=35000``
      | ``-Djcifs.client.connTimeout=60000``
      | ``-Djcifs.client.sessionTimeout=60000``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j.skipJansi=true``
      | ``-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider``
      | ``-Dorg.apache.pdfbox.rendering.UsePureJavaCMYKConversion=true``
  * - jvm.suggest.options
    - JVM-Optionen (durch Zeilenumbrüche getrennt), die an den Suggest-Creator-Kindprozess übergeben werden.
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx256m``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=1m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=30``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j.skipJansi=true``
  * - jvm.chunk.options
    - JVM-Optionen für den Chunk-Vektor-Indexer-Prozess. Heap-Budget. Diese Kind-JVM wird nur gestartet, solange der Job "Content Chunk Vector Indexer" läuft, sodass ein großzügiges -Xmx nichts kostet, wenn das Content-Chunking deaktiviert ist. Der Live-Bestand wird von den laufenden Batches dominiert, von denen jeder pro Dokument das vollständige _source, die Chunk-Strings des Dokuments und die Embedding-Vektoren des Dokuments behält: content_chunker.job.bulk_size          (Standard   20) x content_chunker.max_chunks_per_document (Standard 1000) x content_chunker.embedding.dimension  (Standard  768) x 4 Byte pro Float x content_chunker.job.concurrency      (Standard    2) = ~117 MB allein für Vektoren, vor Chunk-Strings und Dokumentquellen. Mit den mitgelieferten Standardwerten beträgt der ungünstigste Fall etwa 190-250 MB im Live-Bestand (und ~235 MB allein für Vektoren bei dimension=1536), was nicht in einen 256-MB-Heap mit nennenswertem GC-Spielraum passt. Erhöhen Sie -Xmx weiter, wenn Sie bulk_size, max_chunks_per_document, concurrency oder die Embedding-Dimension erhöhen.
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx1g``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=1m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=30``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j.skipJansi=true``
  * - jvm.thumbnail.options
    - JVM-Optionen für den Thumbnail-Prozess.
    - | ``-Djava.awt.headless=true``
      | ``-Dfile.encoding=UTF-8``
      | ``-Djna.nosys=true``
      | ``-Djdk.io.permissionsUseCanonicalPath=true``
      | ``-Djava.util.logging.manager=org.apache.logging.log4j.jul.LogManager``
      | ``-server``
      | ``-Xms128m``
      | ``-Xmx256m``
      | ``-XX:MaxMetaspaceSize=128m``
      | ``-XX:CompressedClassSpaceSize=32m``
      | ``-XX:-UseGCOverheadLimit``
      | ``-XX:+UseTLAB``
      | ``-XX:+DisableExplicitGC``
      | ``-XX:-HeapDumpOnOutOfMemoryError``
      | ``-XX:-OmitStackTraceInFastThrow``
      | ``-XX:+UnlockExperimentalVMOptions``
      | ``-XX:+UseG1GC``
      | ``-XX:InitiatingHeapOccupancyPercent=45``
      | ``-XX:G1HeapRegionSize=4m``
      | ``-XX:MaxGCPauseMillis=60000``
      | ``-XX:G1NewSizePercent=5``
      | ``-XX:G1MaxNewSizePercent=50``
      | ``-Djcifs.client.responseTimeout=30000``
      | ``-Djcifs.client.soTimeout=35000``
      | ``-Djcifs.client.connTimeout=60000``
      | ``-Djcifs.client.sessionTimeout=60000``
      | ``-Dio.netty.noUnsafe=true``
      | ``-Dio.netty.noKeySetOptimization=true``
      | ``-Dio.netty.recycler.maxCapacityPerThread=0``
      | ``-Dlog4j.shutdownHookEnabled=false``
      | ``-Dlog4j2.disable.jmx=true``
      | ``-Dlog4j2.formatMsgNoLookups=true``
      | ``-Dlog4j.skipJansi=true``
      | ``-Dsun.java2d.cmm=sun.java2d.cmm.kcms.KcmsServiceProvider``
      | ``-Dorg.apache.pdfbox.rendering.UsePureJavaCMYKConversion=true``

.. list-table:: Job
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - job.system.job.ids
    - System-Job-IDs für geplante Jobs.
    - ``default_crawler``
  * - job.template.title.web
    - Vorlage für den Titel des Web-Crawler-Jobs.
    - ``Web Crawler - {0}``
  * - job.template.title.file
    - Vorlage für den Titel des Datei-Crawler-Jobs.
    - ``File Crawler - {0}``
  * - job.template.title.data
    - Vorlage für den Titel des Datenspeicher-Crawler-Jobs.
    - ``Data Crawler - {0}``
  * - job.template.script
    - Skriptvorlage für die Job-Ausführung.
    - ``return container.getComponent("crawlJob").logLevel("info").webConfigIds([{0}]).fileConfigIds([{1}]).dataConfigIds([{2}]).jobExecutor(executor).execute();``
  * - job.max.crawler.processes
    - Maximale Anzahl von Crawler-Prozessen.
    - ``0``
  * - job.default.script
    - Standard-Skriptsprache für Jobs.
    - ``javascript``
  * - job.system.property.filter.pattern
    - Muster zum Filtern von Systemeigenschaften für Jobs.
    - (empty)
  * - processors
    - Anzahl der zu verwendenden Prozessoren.
    - ``0``
  * - java.command.path
    - Pfad zum Java-Befehl.
    - ``java``
  * - python.command.path
    - Pfad zum Python-Befehl.
    - ``python``
  * - path.encoding
    - Kodierung für Dateipfade.
    - ``UTF-8``
  * - use.own.tmp.dir
    - Gibt an, ob ein eigenes temporäres Verzeichnis verwendet werden soll.
    - ``true``
  * - max.log.output.length
    - Maximale Länge der Protokollausgabe.
    - ``4000``
  * - adaptive.load.control
    - Wert für die adaptive Laststeuerung.
    - ``50``
  * - web.load.control
    - CPU-Schwellenwert (%) für die Laststeuerung von Web-Anfragen. Gibt 429 zurück, wenn CPU >= diesem Wert. (100: deaktiviert)
    - ``100``
  * - api.load.control
    - CPU-Schwellenwert (%) für die Laststeuerung von API-Anfragen. Gibt 429 zurück, wenn CPU >= diesem Wert. (100: deaktiviert)
    - ``100``
  * - load.control.monitor.interval
    - Intervall (Sekunden) für die Überwachung der OpenSearch-CPU-Last.
    - ``1``
  * - supported.languages
    - Unterstützte Sprachen.
    - ``ar,bg,bn,ca,ckb_IQ,cs,da,de,el,en_IE,en,es,et,eu,fa,fi,fr,gl,gu,he,hi,hr,hu,hy,id,it,ja,ko,lt,lv,mk,ml,nl,no,pa,pl,pt_BR,pt,ro,ru,si,sq,sv,ta,te,th,tl,tr,uk,ur,vi,zh_CN,zh_TW,zh``
  * - api.access.token.length
    - Länge des API-Zugriffstokens.
    - ``60``
  * - api.access.token.request.parameter
    - Anfrageparameter für das API-Zugriffstoken.
    - (empty)
  * - api.admin.access.permissions
    - Berechtigungen für den API-Administratorzugriff.
    - ``Radmin-api``
  * - api.search.accept.referers
    - Zulässige Referer für die API-Suche.
    - (empty)
  * - api.search.scroll
    - Gibt an, ob Scroll für die API-Suche aktiviert werden soll.
    - ``false``
  * - api.search.export
    - Gibt an, ob der Export von Suchergebnissen (CSV/JSON) durch Endbenutzer unter /api/v2/documents/export aktiviert werden soll.
    - ``false``
  * - api.search.export.max.size
    - Maximale Anzahl von Dokumenten, die ein Suchergebnis-Export schreibt.
    - ``1000``
  * - api.search.export.fields
    - Vom Suchergebnis-Export geschriebene Felder (kommagetrennt). Ein Feld, das kein API-Antwortfeld ist, wird ignoriert.
    - ``title,url_link,last_modified,content_length,filetype``
  * - api.search.export.rate.limit.per.minute
    - Maximale Anzahl von Suchergebnis-Exporten pro Minute für jeden Benutzer (für einen Gast pro Client-IP). 0 oder weniger deaktiviert das Limit.
    - ``10``
  * - api.json.response.headers
    - Header für die API-JSON-Antwort. Access-Control-\* und Timing-Allow-Origin werden hier ignoriert (CORS wird über api.cors.\* / CorsFilter gesteuert). Setzen Sie Vary nicht.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.json.response.exception.included
    - Gibt an, ob Ausnahmen in die API-JSON-Antwort aufgenommen werden sollen.
    - ``false``
  * - api.gsa.response.headers
    - Header für die API-GSA-Antwort. Access-Control-\* und Timing-Allow-Origin werden hier ignoriert (CORS wird über api.cors.\* / CorsFilter gesteuert). Setzen Sie Vary nicht.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.gsa.response.exception.included
    - Gibt an, ob Ausnahmen in die API-GSA-Antwort aufgenommen werden sollen.
    - ``false``
  * - api.dashboard.response.headers
    - Header für die API-Dashboard-Antwort. Access-Control-\* und Timing-Allow-Origin werden hier ignoriert (CORS wird über api.cors.\* / CorsFilter gesteuert). Setzen Sie Vary nicht.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.cors.allow.origin
    - Zulässige Origins für CORS. "\*" gibt ein literales "\*" zurück (der Origin der Anfrage wird NICHT gespiegelt) und deaktiviert Anmeldedaten. Legen Sie explizite Origins (durch Zeilenumbruch oder Komma getrennt) fest, um Cross-Origin-Zugriff mit Anmeldedaten zu erlauben.
    - ``*``
  * - api.cors.allow.methods
    - Zulässige HTTP-Methoden für CORS.
    - ``GET, POST, OPTIONS, DELETE, PUT``
  * - api.cors.max.age
    - Max-Age für CORS-Preflight-Anfragen.
    - ``3600``
  * - api.cors.allow.headers
    - Zulässige Anfrage-Header für den CORS-Preflight. Es wird eine statische Liste zurückgegeben (Access-Control-Request-Headers wird nicht gespiegelt). Enthält X-Fess-CSRF-Token für Cross-Origin-SPAs, die das CSRF-Token senden.
    - ``Origin, Content-Type, Accept, Authorization, X-Requested-With, X-Fess-CSRF-Token``
  * - api.cors.allow.credentials
    - Gibt an, ob Anmeldedaten für CORS zugelassen werden sollen. Wird nur bei exakter Übereinstimmung mit einem expliziten Origin berücksichtigt; wird ignoriert, wenn api.cors.allow.origin "\*" ist.
    - ``true``
  * - api.jsonp.enabled
    - Gibt an, ob JSONP für die API aktiviert werden soll.
    - ``false``
  * - api.ping.search_engine.fields
    - Felder für den API-Ping an die Suchmaschine.
    - ``status,timed_out``

Rate-Limiting
-------------

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rate.limit.enabled
    - Gibt an, ob Rate-Limiting aktiviert ist.
    - ``false``
  * - rate.limit.requests.per.window
    - Maximal zulässige Anzahl von Anfragen pro Fenster.
    - ``100``
  * - rate.limit.window.ms
    - Fenstergröße in Millisekunden.
    - ``60000``
  * - rate.limit.block.duration.ms
    - Dauer in Millisekunden, für die die IP bei Überschreitung des Limits blockiert wird.
    - ``300000``
  * - rate.limit.retry.after.seconds
    - Wert des Retry-After-Headers in Sekunden.
    - ``60``
  * - rate.limit.whitelist.ips
    - Kommagetrennte Liste von IPs auf der Whitelist (z. B. 127.0.0.1,::1).
    - ``127.0.0.1,::1``
  * - rate.limit.blocked.ips
    - Kommagetrennte Liste blockierter IPs.
    - (empty)
  * - rate.limit.trusted.proxies
    - Kommagetrennte Liste vertrauenswürdiger Proxy-IPs. Vertrauen Sie X-Forwarded-For/X-Real-IP nur von diesen IPs.
    - ``127.0.0.1,::1``
  * - rate.limit.cleanup.interval
    - Anzahl der Anfragen zwischen Bereinigungsvorgängen zur Vermeidung von Speicherlecks.
    - ``1000``
  * - virtual.host.headers
    - Virtueller Host: Host:fess.codelibs.org=fess
    - (empty)
  * - http.proxy.host
    - Hostname des HTTP-Proxy-Servers.
    - (empty)
  * - http.proxy.port
    - Portnummer des HTTP-Proxy-Servers (z. B. 8080).
    - ``8080``
  * - http.proxy.username
    - Benutzername für die HTTP-Proxy-Authentifizierung.
    - (empty)
  * - http.proxy.password
    - Passwort für die HTTP-Proxy-Authentifizierung.
    - (empty)
  * - http.fileupload.max.size
    - Maximale Größe (Bytes) für HTTP-Datei-Uploads.
    - ``262144000``
  * - http.fileupload.threshold.size
    - Schwellenwert (Bytes) für die Pufferung von HTTP-Datei-Uploads.
    - ``262144``
  * - http.fileupload.max.file.count
    - Maximal zulässige Anzahl von Dateien pro HTTP-Upload.
    - ``10``

Index
-----

.. list-table:: Crawler: Allgemein
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.http.thread_pool.size
    - Anzahl der Threads für das HTTP-Crawling.
    - ``0``
  * - crawler.data.serializer
    - Serializer-Typ für Crawler-Daten (z. B. kryo).
    - ``kryo``
  * - crawler.document.max.site.length
    - Maximale Länge des Site-Namens in Dokumenten.
    - ``100``
  * - crawler.document.site.encoding
    - Kodierung für Site-Namen in Dokumenten.
    - ``UTF-8``
  * - crawler.document.unknown.hostname
    - Hostname, der in Dokumenten verwendet wird, wenn er unbekannt ist.
    - ``unknown``
  * - crawler.document.use.site.encoding.on.english
    - Gibt an, ob die Site-Kodierung für englische Dokumente verwendet werden soll.
    - ``false``
  * - crawler.document.append.data
    - Gibt an, ob Daten an Dokumente angehängt werden sollen.
    - ``true``
  * - crawler.document.append.filename
    - Gibt an, ob der Dateiname an Dokumente angehängt werden soll.
    - ``false``
  * - crawler.document.max.alphanum.term.size
    - Maximale Größe alphanumerischer Begriffe in Dokumenten.
    - ``20``
  * - crawler.document.max.symbol.term.size
    - Maximale Größe von Symbolbegriffen in Dokumenten.
    - ``10``
  * - crawler.document.duplicate.term.removed
    - Gibt an, ob doppelte Begriffe in Dokumenten entfernt werden sollen.
    - ``false``
  * - crawler.document.space.chars
    - Unicode-Leerzeichen für das Parsen von Dokumenten.
    - ``u0009u000Au000Bu000Cu000Du001Cu001Du001Eu001Fu0020u00A0u1680u180Eu2000u2001u2002u2003u2004u2005u2006u2007u2008u2009u200Au200Bu200Cu202Fu205Fu3000uFEFFuFFFDu00B6``
  * - crawler.document.fullstop.chars
    - Unicode-Punktzeichen für das Parsen von Dokumenten.
    - ``u002eu06d4u2e3cu3002``
  * - crawler.crawling.data.encoding
    - Kodierung für Crawling-Daten.
    - ``UTF-8``
  * - crawler.web.protocols
    - Unterstützte Web-Protokolle für das Crawling.
    - ``http,https``
  * - crawler.file.protocols
    - Unterstützte Dateiprotokolle für das Crawling.
    - ``file,smb,smb1,ftp``
  * - crawler.data.env.param.key.pattern
    - Muster für Schlüssel von Umgebungsvariablen in Crawling-Daten.
    - ``^FESS_ENV_.*``
  * - crawler.ignore.robots.txt
    - Gibt an, ob robots.txt beim Crawling ignoriert werden soll.
    - ``false``
  * - crawler.ignore.robots.tags
    - Gibt an, ob Robots-Meta-Tags beim Crawling ignoriert werden sollen.
    - ``false``
  * - crawler.ignore.content.exception
    - Gibt an, ob Inhaltsausnahmen beim Crawling ignoriert werden sollen.
    - ``true``
  * - crawler.failure.url.status.codes
    - HTTP-Statuscodes, die als Fehler-URLs gelten.
    - ``404,403,410``
  * - crawler.system.monitor.interval
    - Intervall (Sekunden) für die Systemüberwachung während des Crawlings.
    - ``60``
  * - crawler.hotthread.ignore_idle_threads
    - Gibt an, ob Leerlauf-Threads bei der Hot-Thread-Überwachung ignoriert werden sollen.
    - ``true``
  * - crawler.hotthread.interval
    - Intervall für die Hot-Thread-Überwachung (z. B. 500ms).
    - ``500ms``
  * - crawler.hotthread.snapshots
    - Anzahl der Snapshots für die Hot-Thread-Überwachung.
    - ``10``
  * - crawler.hotthread.threads
    - Anzahl der Threads für die Hot-Thread-Überwachung.
    - ``3``
  * - crawler.hotthread.timeout
    - Timeout für die Hot-Thread-Überwachung (z. B. 30s).
    - ``30s``
  * - crawler.hotthread.type
    - Typ der Hot-Thread-Überwachung (z. B. cpu).
    - ``cpu``
  * - crawler.metadata.content.excludes
    - Metadatenfelder, die vom Dokumentinhalt ausgeschlossen werden.
    - ``resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*``
  * - crawler.metadata.name.mapping
    - Zuordnung für Dokument-Metadatennamen.
    - | ``title=title:string``
      | ``Title=title:string``
      | ``dc:title=title:string``
      | ``frontmatter.title=title:string``

.. list-table:: Crawler: HTML
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.html.content.xpath
    - XPath zum Extrahieren des Hauptinhalts aus HTML-Dokumenten.
    - ``//BODY``
  * - crawler.document.html.lang.xpath
    - XPath zum Extrahieren des Sprachattributs aus HTML-Dokumenten.
    - ``//HTML/@lang``
  * - crawler.document.html.digest.xpath
    - XPath zum Extrahieren des Digest (Beschreibung) aus HTML-Dokumenten.
    - ``//META[@name='description']/@content``
  * - crawler.document.html.canonical.xpath
    - XPath zum Extrahieren der kanonischen URL aus HTML-Dokumenten.
    - ``//LINK[@rel='canonical'][1]/@href``
  * - crawler.document.html.pruned.tags
    - HTML-Tags, die bei der Dokumentverarbeitung beschnitten (entfernt) werden.
    - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
  * - crawler.document.html.max.digest.length
    - Maximale Länge des aus HTML-Dokumenten extrahierten Digest.
    - ``120``
  * - crawler.document.html.default.lang
    - Standardsprache für HTML-Dokumente.
    - (empty)
  * - crawler.document.html.default.include.index.patterns
    - Muster, die bei der HTML-Indexverarbeitung eingeschlossen werden.
    - (empty)
  * - crawler.document.html.default.exclude.index.patterns
    - Muster, die bei der HTML-Indexverarbeitung ausgeschlossen werden.
    - ``(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)``
  * - crawler.document.html.default.include.search.patterns
    - Muster, die bei der HTML-Suchverarbeitung eingeschlossen werden.
    - (empty)
  * - crawler.document.html.default.exclude.search.patterns
    - Muster, die bei der HTML-Suchverarbeitung ausgeschlossen werden.
    - (empty)

.. list-table:: Crawler: Datei
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.file.name.encoding
    - Kodierung für Dateinamen in Dokumenten.
    - (empty)
  * - crawler.document.file.no.title.label
    - Label, das verwendet wird, wenn eine Datei keinen Titel hat.
    - ``No title.``
  * - crawler.document.file.ignore.empty.content
    - Gibt an, ob Dateien mit leerem Inhalt ignoriert werden sollen.
    - ``false``
  * - crawler.document.file.max.title.length
    - Maximale Länge des Dateititels in Dokumenten.
    - ``100``
  * - crawler.document.file.max.digest.length
    - Maximale Länge des Datei-Digest in Dokumenten.
    - ``200``
  * - crawler.document.file.append.meta.content
    - Gibt an, ob Meta-Inhalte aus Dateien angehängt werden sollen.
    - ``true``
  * - crawler.document.file.append.body.content
    - Gibt an, ob Body-Inhalte aus Dateien angehängt werden sollen.
    - ``true``
  * - crawler.document.file.default.lang
    - Standardsprache für Dateidokumente.
    - (empty)
  * - crawler.document.file.default.include.index.patterns
    - Muster, die bei der Dateiindexverarbeitung eingeschlossen werden.
    - (empty)
  * - crawler.document.file.default.exclude.index.patterns
    - Muster, die bei der Dateiindexverarbeitung ausgeschlossen werden.
    - (empty)
  * - crawler.document.file.default.include.search.patterns
    - Muster, die bei der Dateisuchverarbeitung eingeschlossen werden.
    - (empty)
  * - crawler.document.file.default.exclude.search.patterns
    - Muster, die bei der Dateisuchverarbeitung ausgeschlossen werden.
    - (empty)
  * - crawler.document.file.owner.enabled
    - Gibt an, ob der Eigentümer gecrawlter Dateien (SMB, lokales Dateisystem und FTP) indiziert werden soll. Der Crawl-Konfigurationsparameter config.owner.enabled überschreibt dies.
    - ``true``
  * - crawler.document.file.last.modifier.enabled
    - Gibt an, ob der letzte Bearbeiter gecrawlter Dateien indiziert werden soll; er wird aus den Dokumentmetadaten gelesen und fällt auf den Dateieigentümer zurück. Der Crawl-Konfigurationsparameter config.last.modifier.enabled überschreibt dies.
    - ``true``

.. list-table:: Crawler: Cache
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.cache.enabled
    - Gibt an, ob der Dokument-Cache aktiviert ist.
    - ``true``
  * - crawler.document.cache.max.size
    - Maximale Größe (Bytes) für den Dokument-Cache.
    - ``2621440``
  * - crawler.document.cache.supported.mimetypes
    - Unterstützte MIME-Typen für den Dokument-Cache.
    - ``text/html``
  * - crawler.document.cache.html.mimetypes
    - ,text/plain,application/xml,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation MIME-Typen für den HTML-Dokument-Cache.
    - ``text/html``
  * - crawler.document.mimetype.extension.overrides
    - Überschreibende Zuordnungen von Erweiterung zu MIME-Typ für die MIME-Typ-Erkennung (eine pro Zeile: .ext=mime/type).
    - (empty)
  * - crawler.document.ocr.enabled
    - Gibt an, ob Text aus Bildern und gescannten PDFs mit Tesseract OCR extrahiert werden soll (erfordert den Befehl tesseract).
    - ``false``
  * - crawler.document.ocr.language
    - Sprachen für Tesseract OCR, verbunden mit '+' (z. B. jpn+eng).
    - ``eng``
  * - crawler.document.ocr.timeout
    - Timeout in Sekunden für einen Tesseract-OCR-Lauf.
    - ``120``

.. list-table:: Indexer
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - indexer.thread.dump.enabled
    - Gibt an, ob der Thread-Dump für den Indexer aktiviert werden soll.
    - ``true``
  * - indexer.unprocessed.document.size
    - Maximale Anzahl unverarbeiteter Dokumente für den Indexer.
    - ``1000``
  * - indexer.click.count.enabled
    - Gibt an, ob die Nachverfolgung der Klickanzahl im Indexer aktiviert werden soll.
    - ``true``
  * - indexer.favorite.count.enabled
    - Gibt an, ob die Nachverfolgung der Favoritenanzahl im Indexer aktiviert werden soll.
    - ``true``
  * - indexer.webfs.commit.margin.time
    - Commit-Pufferzeit (ms) für webfs im Indexer.
    - ``5000``
  * - indexer.webfs.max.empty.list.count
    - Maximale Anzahl leerer Listen für webfs im Indexer.
    - ``3600``
  * - indexer.webfs.update.interval
    - Aktualisierungsintervall (ms) für webfs im Indexer.
    - ``10000``
  * - indexer.webfs.max.document.cache.size
    - Maximale Dokument-Cache-Größe für webfs im Indexer.
    - ``10``
  * - indexer.webfs.max.document.request.size
    - Maximale Größe von Dokumentanfragen (Bytes) für webfs im Indexer.
    - ``1048576``
  * - indexer.data.max.document.cache.size
    - Maximale Dokument-Cache-Größe für Daten im Indexer.
    - ``10000``
  * - indexer.data.max.document.request.size
    - Maximale Größe von Dokumentanfragen (Bytes) für Daten im Indexer.
    - ``1048576``
  * - indexer.data.max.delete.cache.size
    - Maximale Lösch-Cache-Größe für Daten im Indexer.
    - ``100``
  * - indexer.data.max.redirect.count
    - Maximale Anzahl von Weiterleitungen für Daten im Indexer.
    - ``10``
  * - indexer.language.fields
    - Felder, die für die Spracherkennung im Indexer verwendet werden.
    - ``content,important_content,title``
  * - indexer.language.detect.length
    - Textlänge für die Spracherkennung im Indexer.
    - ``1000``
  * - indexer.max.result.window.size
    - Maximale Ergebnisfenstergröße für den Indexer.
    - ``10000``
  * - indexer.max.search.doc.size
    - Maximale Anzahl von Suchdokumenten für den Indexer.
    - ``50000``

.. list-table:: Index-Einstellungen
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.codec
    - Codec-Typ für den Index.
    - ``default``
  * - index.number_of_shards
    - Anzahl der Primär-Shards für den Index.
    - ``5``
  * - index.auto_expand_replicas
    - Einstellung zur automatischen Erweiterung der Replikate für den Index.
    - ``0-1``
  * - index.id.digest.algorithm
    - Digest-Algorithmus für Index-IDs.
    - ``SHA-512``
  * - index.user.initial_password
    - Initiales Passwort für den Index-Benutzer.
    - ``admin``

.. list-table:: Feldnamen
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.field.favorite_count
    - Feldname für die Favoritenanzahl im Index.
    - ``favorite_count``
  * - index.field.click_count
    - Feldname für die Klickanzahl im Index.
    - ``click_count``
  * - index.field.config_id
    - Feldname für die Konfigurations-ID im Index.
    - ``config_id``
  * - index.field.expires
    - Feldname für das Ablaufdatum im Index.
    - ``expires``
  * - index.field.url
    - Feldname für die URL im Index.
    - ``url``
  * - index.field.doc_id
    - Feldname für die Dokument-ID im Index.
    - ``doc_id``
  * - index.field.id
    - Feldname für die interne ID im Index.
    - ``_id``
  * - index.field.version
    - Feldname für die Version im Index.
    - ``_version``
  * - index.field.seq_no
    - Feldname für die Sequenznummer im Index.
    - ``_seq_no``
  * - index.field.primary_term
    - Feldname für den Primary Term im Index.
    - ``_primary_term``
  * - index.field.lang
    - Feldname für die Sprache im Index.
    - ``lang``
  * - index.field.has_cache
    - Feldname für den Cache-Status im Index.
    - ``has_cache``
  * - index.field.last_modified
    - Feldname für das Datum der letzten Änderung im Index.
    - ``last_modified``
  * - index.field.etag
    - Feldname für den ETag-Antwort-Header des gecrawlten Dokuments im Index.
    - ``etag``
  * - index.field.owner
    - Feldname für den Eigentümer der gecrawlten Datei im Index.
    - ``owner``
  * - index.field.last_modifier
    - Feldname für den letzten Bearbeiter der gecrawlten Datei im Index.
    - ``last_modifier``
  * - index.field.anchor
    - Feldname für den Anker im Index.
    - ``anchor``
  * - index.field.segment
    - Feldname für das Segment im Index.
    - ``segment``
  * - index.field.role
    - Feldname für die Rolle im Index.
    - ``role``
  * - index.field.boost
    - Feldname für den Boost-Wert im Index.
    - ``boost``
  * - index.field.created
    - Feldname für das Erstellungsdatum im Index.
    - ``created``
  * - index.field.timestamp
    - Feldname für den Zeitstempel im Index.
    - ``timestamp``
  * - index.field.label
    - Feldname für das Label im Index.
    - ``label``
  * - index.field.tag
    - Feldname für die Benutzer-Tags des Dokuments im Index.
    - ``tag``
  * - index.field.mimetype
    - Feldname für den MIME-Typ im Index.
    - ``mimetype``
  * - index.field.parent_id
    - Feldname für die übergeordnete ID im Index.
    - ``parent_id``
  * - index.field.important_content
    - Feldname für den wichtigen Inhalt im Index.
    - ``important_content``
  * - index.field.content
    - Feldname für den Inhalt im Index.
    - ``content``
  * - index.field.content_minhash_bits
    - Feldname für die Inhalts-Minhash-Bits im Index.
    - ``content_minhash_bits``
  * - index.field.cache
    - Feldname für den Cache im Index.
    - ``cache``
  * - index.field.digest
    - Feldname für den Digest im Index.
    - ``digest``
  * - index.field.title
    - Feldname für den Titel im Index.
    - ``title``
  * - index.field.host
    - Feldname für den Host im Index.
    - ``host``
  * - index.field.site
    - Feldname für die Site im Index.
    - ``site``
  * - index.field.content_length
    - Feldname für die Inhaltslänge im Index.
    - ``content_length``
  * - index.field.filetype
    - Feldname für den Dateityp im Index.
    - ``filetype``
  * - index.field.filename
    - Feldname für den Dateinamen im Index.
    - ``filename``
  * - index.field.thumbnail
    - Feldname für das Thumbnail im Index.
    - ``thumbnail``
  * - index.field.virtual_host
    - Feldname für den virtuellen Host im Index.
    - ``virtual_host``
  * - response.field.content_title
    - Feldname für den Inhaltstitel in der Antwort.
    - ``content_title``
  * - response.field.content_description
    - Feldname für die Inhaltsbeschreibung in der Antwort.
    - ``content_description``
  * - response.field.url_link
    - Feldname für den URL-Link in der Antwort.
    - ``url_link``
  * - response.field.site_path
    - Feldname für den Site-Pfad in der Antwort.
    - ``site_path``
  * - response.max.title.length
    - Maximale Länge des Inhaltstitels in der Antwort.
    - ``50``
  * - response.max.site.path.length
    - Maximale Länge des Site-Pfads in der Antwort.
    - ``100``
  * - response.highlight.content_title.enabled
    - Gibt an, ob die Hervorhebung des Inhaltstitels in der Antwort aktiviert werden soll.
    - ``true``
  * - response.inline.mimetypes
    - Inline-MIME-Typen für die Antwort.
    - ``application/pdf,text/plain``
  * - response.headers
    - HTTP-Header für die Antwort. Access-Control-\* und Timing-Allow-Origin werden ignoriert (CORS wird über api.cors.\* / CorsFilter gesteuert). Setzen Sie Vary hier nicht.
    - | ``text/html=X-XSS-Protection: 1; mode=block``
      | ``text/html=X-Frame-Options: SAMEORIGIN``

.. list-table:: Dokumentindex
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.document.search.index
    - Indexname für Suchdokumente.
    - ``fess.search``
  * - index.document.update.index
    - Indexname für Aktualisierungsdokumente.
    - ``fess.update``
  * - index.document.suggest.index
    - Indexname für Vorschlagsdokumente.
    - ``fess``
  * - index.document.crawler.index
    - Indexname für Crawler-Dokumente.
    - ``fess_crawler``
  * - index.document.crawler.queue.number_of_shards
    - Anzahl der Primär-Shards für den Crawler-Warteschlangen-Index.
    - ``10``
  * - index.document.crawler.data.number_of_shards
    - Anzahl der Primär-Shards für den Crawler-Daten-Index.
    - ``10``
  * - index.document.crawler.filter.number_of_shards
    - Anzahl der Primär-Shards für den Crawler-Filter-Index.
    - ``10``
  * - index.document.crawler.queue.number_of_replicas
    - Anzahl der Replikate für den Crawler-Warteschlangen-Index.
    - ``1``
  * - index.document.crawler.data.number_of_replicas
    - Anzahl der Replikate für den Crawler-Daten-Index.
    - ``1``
  * - index.document.crawler.filter.number_of_replicas
    - Anzahl der Replikate für den Crawler-Filter-Index.
    - ``1``
  * - index.config.index
    - Indexname für Konfigurationsdaten.
    - ``fess_config``
  * - index.user.index
    - Indexname für Benutzerdaten.
    - ``fess_user``
  * - index.log.index
    - Indexname für Protokolldaten.
    - ``fess_log``
  * - index.dictionary.prefix
    - Präfix für Wörterbuch-Indexnamen.
    - (empty)

.. list-table:: Dokumentenverwaltung
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.admin.array.fields
    - Felder vom Typ Array für die Administration im Index.
    - ``lang,role,label,anchor,virtual_host``
  * - index.admin.date.fields
    - Felder vom Typ Datum für die Administration im Index.
    - ``expires,created,timestamp,last_modified``
  * - index.admin.integer.fields
    - Felder vom Typ Integer für die Administration im Index.
    - (empty)
  * - index.admin.long.fields
    - Felder vom Typ Long für die Administration im Index.
    - ``content_length,favorite_count,click_count``
  * - index.admin.float.fields
    - Felder vom Typ Float für die Administration im Index.
    - ``boost``
  * - index.admin.double.fields
    - Felder vom Typ Double für die Administration im Index.
    - (empty)
  * - index.admin.required.fields
    - Pflichtfelder für die Administration im Index.
    - ``url,title,role,boost``

.. list-table:: Timeouts
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.search.timeout
    - Timeout für Index-Suchvorgänge.
    - ``3m``
  * - index.scroll.search.timeout
    - Timeout für Scroll-Suchvorgänge.
    - ``3m``
  * - index.index.timeout
    - Timeout für Index-Vorgänge.
    - ``3m``
  * - index.bulk.timeout
    - Timeout für Bulk-Index-Vorgänge.
    - ``3m``
  * - index.delete.timeout
    - Timeout für Löschvorgänge im Index.
    - ``3m``
  * - index.health.timeout
    - Timeout für Index-Integritätsprüfungen.
    - ``10m``
  * - index.indices.timeout
    - Timeout für Index-Indices-Vorgänge.
    - ``1m``

.. list-table:: Dateitypen
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.filetype
    - Zuordnung von MIME-Typen zu Dateityp-Labels für die Indexierung.
    - | ``text/html=html``
      | ``application/msword=word``
      | ``application/vnd.openxmlformats-officedocument.wordprocessingml.document=word``
      | ``application/vnd.ms-excel=excel``
      | ``application/vnd.ms-excel.sheet.2=excel``
      | ``application/vnd.ms-excel.sheet.3=excel``
      | ``application/vnd.ms-excel.sheet.4=excel``
      | ``application/vnd.ms-excel.workspace.3=excel``
      | ``application/vnd.ms-excel.workspace.4=excel``
      | ``application/vnd.openxmlformats-officedocument.spreadsheetml.sheet=excel``
      | ``application/vnd.ms-powerpoint=powerpoint``
      | ``application/vnd.openxmlformats-officedocument.presentationml.presentation=powerpoint``
      | ``application/vnd.oasis.opendocument.text=odt``
      | ``application/vnd.oasis.opendocument.spreadsheet=ods``
      | ``application/vnd.oasis.opendocument.presentation=odp``
      | ``application/pdf=pdf``
      | ``application/x-fictionbook+xml=fb2``
      | ``application/e-pub+zip=epub``
      | ``application/x-ibooks+zip=ibooks``
      | ``text/plain=txt``
      | ``application/rtf=rtf``
      | ``application/vnd.ms-htmlhelp=chm``
      | ``application/zip=zip``
      | ``application/x-7z-comressed=7z``
      | ``application/x-bzip=bz``
      | ``application/x-bzip2=bz2``
      | ``application/x-tar=tar``
      | ``application/x-rar-compressed=rar``
      | ``video/3gp=3gp``
      | ``video/3g2=3g2``
      | ``video/x-msvideo=avi``
      | ``video/x-flv=flv``
      | ``video/mpeg=mpeg``
      | ``video/mp4=mp4``
      | ``video/ogv=ogv``
      | ``video/quicktime=qt``
      | ``video/x-m4v=m4v``
      | ``audio/x-aif=aif``
      | ``audio/midi=midi``
      | ``audio/mpga=mpga``
      | ``audio/mp4=mp4a``
      | ``audio/ogg=oga``
      | ``audio/x-wav=wav``
      | ``image/webp=webp``
      | ``image/bmp=bmp``
      | ``image/x-icon=ico``
      | ``image/x-icon=ico``
      | ``image/png=png``
      | ``image/svg+xml=svg``
      | ``image/tiff=tiff``
      | ``image/jpeg=jpg``
  * - index.reindex.size
    - Anzahl der Dokumente, die pro Neuindizierungsvorgang verarbeitet werden.
    - ``100``
  * - index.reindex.body
    - Request-Body-Vorlage für Neuindizierungsvorgänge.
    - ``{"source":{"index":"__SOURCE_INDEX__","size":__SIZE__},"dest":{"index":"__DEST_INDEX__"},"script":{"source":"__SCRIPT_SOURCE__"}}``
  * - index.reindex.requests_per_second
    - Anfragen pro Sekunde für Neuindizierungsvorgänge ("adaptive" für automatisch).
    - ``adaptive``
  * - index.reindex.refresh
    - Gibt an, ob der Index nach der Neuindizierung aktualisiert werden soll.
    - ``false``
  * - index.reindex.timeout
    - Timeout für Neuindizierungsvorgänge.
    - ``1m``
  * - index.reindex.scroll
    - Scroll-Timeout für Neuindizierungsvorgänge.
    - ``5m``
  * - index.reindex.max_docs
    - Maximale Anzahl von Dokumenten für Neuindizierungsvorgänge.
    - (empty)

.. list-table:: Abfrage
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.max.length
    - Maximale Länge von Suchanfragen.
    - ``1000``
  * - query.timeout
    - Timeout (ms) für Suchanfragen.
    - ``10000``
  * - query.timeout.logging
    - Gibt an, ob Suchen protokolliert werden sollen, deren Ergebnisse unvollständig sind, weil für die Abfrage ein Timeout eingetreten ist oder ein Shard ausgefallen ist.
    - ``true``
  * - query.track.total.hits
    - Maximale Anzahl von Gesamttreffern, die in Abfragen verfolgt werden. Unterstützt werden nur eine positive Zahl oder true: false lässt die Antwort ohne Trefferanzahl, und eine Suche, die dies anfordert, hier oder als Suchparameter, wird abgelehnt.
    - ``10000``
  * - query.geo.fields
    - Felder, die für Geosuch-Abfragen verwendet werden.
    - ``location``
  * - query.browser.lang.parameter.name
    - Parametername für die Browsersprache in Abfragen.
    - ``browser_lang``
  * - query.replace.term.with.prefix.query
    - Gibt an, ob ein Begriff durch eine Präfix-Abfrage ersetzt werden soll.
    - ``true``
  * - query.orsearch.min.hit.count
    - Minimale Trefferanzahl für OR-Suchabfragen.
    - ``-1``
  * - query.highlight.terminal.chars
    - Unicode-Abschlusszeichen für die Such-Hervorhebung.
    - ``u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61``
  * - query.highlight.fragment.size
    - Fragmentgröße für die Such-Hervorhebung.
    - ``60``
  * - query.highlight.number.of.fragments
    - Anzahl der Fragmente für die Such-Hervorhebung.
    - ``2``
  * - query.highlight.type
    - Typ der Such-Hervorhebung.
    - ``fvh``
  * - query.highlight.tag.pre
    - Tag, das vor hervorgehobenem Text verwendet wird.
    - ``<strong>``
  * - query.highlight.tag.post
    - Tag, das nach hervorgehobenem Text verwendet wird.
    - ``</strong>``
  * - query.highlight.boundary.chars
    - Begrenzungszeichen für die Such-Hervorhebung.
    - ``u0009u000Au0013u0020``
  * - query.highlight.boundary.max.scan
    - Maximaler Scan für die Grenzen der Such-Hervorhebung.
    - ``20``
  * - query.highlight.boundary.scanner
    - Scanner-Typ für die Grenzen der Such-Hervorhebung.
    - ``chars``
  * - query.highlight.encoder
    - Encoder-Typ für die Such-Hervorhebung.
    - ``default``
  * - query.highlight.force.source
    - Gibt an, ob die Quelle für die Such-Hervorhebung erzwungen werden soll.
    - ``false``
  * - query.highlight.fragmenter
    - Fragmenter-Typ für die Such-Hervorhebung.
    - ``span``
  * - query.highlight.fragment.offset
    - Offset für Fragmente der Such-Hervorhebung.
    - ``-1``
  * - query.highlight.no.match.size
    - Größe für die Such-Hervorhebung ohne Treffer.
    - ``0``
  * - query.highlight.order
    - Reihenfolge für Fragmente der Such-Hervorhebung.
    - ``score``
  * - query.highlight.phrase.limit
    - Phrasenlimit für die Such-Hervorhebung.
    - ``256``
  * - query.highlight.content.description.fields
    - Felder für die Inhaltsbeschreibung in der Such-Hervorhebung.
    - ``hl_content,digest``
  * - query.highlight.boundary.position.detect
    - Gibt an, ob die Grenzposition in der Such-Hervorhebung erkannt werden soll.
    - ``true``
  * - query.highlight.text.fragment.type
    - Typ für das Textfragment in der Such-Hervorhebung.
    - ``query``
  * - query.highlight.text.fragment.size
    - Größe für das Textfragment in der Such-Hervorhebung.
    - ``3``
  * - query.highlight.text.fragment.prefix.length
    - Präfixlänge für das Textfragment in der Such-Hervorhebung.
    - ``5``
  * - query.highlight.text.fragment.suffix.length
    - Suffixlänge für das Textfragment in der Such-Hervorhebung.
    - ``5``
  * - query.max.search.result.offset
    - Maximaler Offset der Suchergebnisse für Abfragen.
    - ``100000``
  * - query.additional.default.fields
    - Zusätzliche Standardfelder für Abfragen.
    - (empty)
  * - query.additional.response.fields
    - Zusätzliche Felder, die für Suchergebnisse aus dem Index abgerufen werden. Die Such-API gibt ein hier hinzugefügtes Feld nur zurück, wenn es auch in query.additional.api.response.fields aufgeführt ist.
    - (empty)
  * - query.additional.api.response.fields
    - Zusätzliche API-Antwortfelder für Abfragen. Dieser Schlüssel hängt Felder nur an die Zulassungsliste der v2-API-Antwort an (nur Hinzufügen); er ruft sie nicht ab. Ein Feld muss zusätzlich abgerufen werden: Fügen Sie es für die Such-API zu query.additional.response.fields oder für die Scroll-API zu query.additional.scroll.response.fields hinzu. Fügen Sie keine ACL- oder internen Felder hinzu (zum Beispiel role, virtual_host); ihr Hinzufügen würde Zugriffskontrollinformationen in der Antwort der Such-API offenlegen.
    - (empty)
  * - query.additional.scroll.response.fields
    - Zusätzliche Felder, die für Scroll-Suchergebnisse aus dem Index abgerufen werden. Die Scroll-API gibt ein hier hinzugefügtes Feld nur zurück, wenn es auch in query.additional.api.response.fields aufgeführt ist.
    - (empty)
  * - query.additional.cache.response.fields
    - Zusätzliche Cache-Antwortfelder für Abfragen.
    - (empty)
  * - query.additional.highlighted.fields
    - Zusätzliche hervorgehobene Felder für Abfragen.
    - (empty)
  * - query.additional.search.fields
    - Zusätzliche Suchfelder für Abfragen.
    - (empty)
  * - query.additional.facet.fields
    - Zusätzliche Facettenfelder für Abfragen.
    - (empty)
  * - query.additional.sort.fields
    - Zusätzliche Sortierfelder für Abfragen.
    - (empty)
  * - query.additional.analyzed.fields
    - Zusätzliche analysierte Felder für Abfragen.
    - (empty)
  * - query.additional.not.analyzed.fields
    - Zusätzliche nicht analysierte Felder für Abfragen.
    - (empty)
  * - query.gsa.response.fields
    - Felder für die GSA-Antwort in Abfragen.
    - ``UE,U,T,RK,S,LANG``
  * - query.gsa.default.lang
    - Standardsprache für GSA-Abfragen.
    - ``en``
  * - query.gsa.default.sort
    - Standardsortierung für GSA-Abfragen.
    - (empty)
  * - query.gsa.meta.prefix
    - Meta-Präfix für GSA-Abfragen.
    - ``MT_``
  * - query.gsa.index.field.charset
    - Zeichensatzfeld für GSA-Indexabfragen.
    - ``charset``
  * - query.gsa.index.field.content_type.
    - Content-Type-Feld für GSA-Indexabfragen.
    - ``content_type``
  * - query.collapse.max.concurrent.group.results
    - Maximale Anzahl gleichzeitiger Gruppenergebnisse für Collapse-Abfragen.
    - ``4``
  * - query.collapse.inner.hits.name
    - Inner-Hits-Name für Collapse-Abfragen.
    - ``similar_docs``
  * - query.collapse.inner.hits.size
    - Inner-Hits-Größe für Collapse-Abfragen.
    - ``0``
  * - query.collapse.inner.hits.sorts
    - Sortierungen für Inner Hits in Collapse-Abfragen.
    - (empty)
  * - query.default.languages
    - Standardsprachen für Abfragen.
    - (empty)
  * - query.json.default.preference
    - Standardpräferenz für JSON-Abfragen.
    - ``_query``
  * - query.gsa.default.preference
    - Standardpräferenz für GSA-Abfragen.
    - ``_query``
  * - query.language.mapping
    - Sprachzuordnung für Abfragen.
    - | ``ar=ar``
      | ``bg=bg``
      | ``bn=bn``
      | ``ca=ca``
      | ``ckb-iq=ckb-iq``
      | ``ckb_IQ=ckb-iq``
      | ``cs=cs``
      | ``da=da``
      | ``de=de``
      | ``el=el``
      | ``en=en``
      | ``en-ie=en-ie``
      | ``en_IE=en-ie``
      | ``es=es``
      | ``et=et``
      | ``eu=eu``
      | ``fa=fa``
      | ``fi=fi``
      | ``fr=fr``
      | ``gl=gl``
      | ``gu=gu``
      | ``he=he``
      | ``hi=hi``
      | ``hr=hr``
      | ``hu=hu``
      | ``hy=hy``
      | ``id=id``
      | ``it=it``
      | ``ja=ja``
      | ``ko=ko``
      | ``lt=lt``
      | ``lv=lv``
      | ``mk=mk``
      | ``ml=ml``
      | ``nl=nl``
      | ``no=no``
      | ``pa=pa``
      | ``pl=pl``
      | ``pt=pt``
      | ``pt-br=pt-br``
      | ``pt_BR=pt-br``
      | ``ro=ro``
      | ``ru=ru``
      | ``si=si``
      | ``sq=sq``
      | ``sv=sv``
      | ``ta=ta``
      | ``te=te``
      | ``th=th``
      | ``tl=tl``
      | ``tr=tr``
      | ``uk=uk``
      | ``ur=ur``
      | ``vi=vi``
      | ``zh-cn=zh-cn``
      | ``zh_CN=zh-cn``
      | ``zh-tw=zh-tw``
      | ``zh_TW=zh-tw``
      | ``zh=zh``

.. list-table:: Boost
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.boost.title
    - Boost-Wert für das Titelfeld in Abfragen.
    - ``0.5``
  * - query.boost.title.lang
    - Boost-Wert für das Titelfeld mit Sprache in Abfragen.
    - ``1.0``
  * - query.boost.content
    - Boost-Wert für das Inhaltsfeld in Abfragen.
    - ``0.05``
  * - query.boost.content.lang
    - Boost-Wert für das Inhaltsfeld mit Sprache in Abfragen.
    - ``0.1``
  * - query.boost.important_content
    - Boost-Wert für das Feld für wichtigen Inhalt in Abfragen.
    - ``-1.0``
  * - query.boost.important_content.lang
    - Boost-Wert für das Feld für wichtigen Inhalt mit Sprache in Abfragen.
    - ``-1.0``
  * - query.boost.fuzzy.min.length
    - Mindestlänge für das Fuzzy-Boosting in Abfragen.
    - ``4``
  * - query.boost.fuzzy.title
    - Boost-Wert für Fuzzy-Titelabfragen.
    - ``0.01``
  * - query.boost.fuzzy.title.fuzziness
    - Fuzziness für Fuzzy-Titelabfragen.
    - ``AUTO``
  * - query.boost.fuzzy.title.expansions
    - Anzahl der Expansionen für Fuzzy-Titelabfragen.
    - ``10``
  * - query.boost.fuzzy.title.prefix_length
    - Präfixlänge für Fuzzy-Titelabfragen.
    - ``0``
  * - query.boost.fuzzy.title.transpositions
    - Gibt an, ob Transpositionen in Fuzzy-Titelabfragen zugelassen werden sollen.
    - ``true``
  * - query.boost.fuzzy.content
    - Boost-Wert für Fuzzy-Inhaltsabfragen.
    - ``0.005``
  * - query.boost.fuzzy.content.fuzziness
    - Fuzziness für Fuzzy-Inhaltsabfragen.
    - ``AUTO``
  * - query.boost.fuzzy.content.expansions
    - Anzahl der Expansionen für Fuzzy-Inhaltsabfragen.
    - ``10``
  * - query.boost.fuzzy.content.prefix_length
    - Präfixlänge für Fuzzy-Inhaltsabfragen.
    - ``0``
  * - query.boost.fuzzy.content.transpositions
    - Gibt an, ob Transpositionen in Fuzzy-Inhaltsabfragen zugelassen werden sollen.
    - ``true``
  * - query.default.query_type
    - Standard-Abfragetyp.
    - ``bool``
  * - query.dismax.tie_breaker
    - Tie-Breaker-Wert für Dismax-Abfragen.
    - ``0.1``
  * - query.bool.minimum_should_match
    - Minimum-should-match-Wert für boolesche Abfragen.
    - (empty)
  * - query.prefix.expansions
    - Anzahl der Expansionen für Präfix-Abfragen.
    - ``50``
  * - query.prefix.slop
    - Slop-Wert für Präfix-Abfragen.
    - ``0``
  * - query.fuzzy.prefix_length
    - Präfixlänge für Fuzzy-Abfragen.
    - ``0``
  * - query.fuzzy.expansions
    - Anzahl der Expansionen für Fuzzy-Abfragen.
    - ``50``
  * - query.fuzzy.transpositions
    - Gibt an, ob Transpositionen in Fuzzy-Abfragen zugelassen werden sollen.
    - ``true``

.. list-table:: Facette
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.facet.fields
    - Felder für Facettenabfragen.
    - ``label``
  * - query.facet.fields.size
    - Größe der Facettenfelder.
    - ``100``
  * - query.facet.fields.size.max
    - Obere Begrenzung für facet.size (wird am zentralen Durchlaufpunkt der Suche angewendet).
    - ``1000``
  * - query.facet.fields.min_doc_count
    - Mindestanzahl von Dokumenten für Facettenfelder.
    - ``1``
  * - query.facet.fields.min_doc_count.max
    - Obere Begrenzung für facet.minDocCount (wird am zentralen Durchlaufpunkt der Suche angewendet).
    - ``2147483647``
  * - query.facet.fields.sort
    - Sortierreihenfolge für Facettenfelder.
    - ``count.desc``
  * - query.facet.fields.missing
    - Wert für fehlende Facettenfelder.
    - (empty)
  * - query.facet.queries
    - Definition der Facettenabfragen.
    - | ``labels.facet_timestamp_title:labels.facet_timestamp_1day=timestamp:[now/d-1d TO *]	labels.facet_timestamp_1week=timestamp:[now/d-7d TO *]	labels.facet_timestamp_1month=timestamp:[now/d-1M TO *]	labels.facet_timestamp_1year=timestamp:[now/d-1y TO *]``
      | ``labels.facet_contentLength_title:labels.facet_contentLength_10k=content_length:[0 TO 9999]	labels.facet_contentLength_10kto100k=content_length:[10000 TO 99999]	labels.facet_contentLength_100kto500k=content_length:[100000 TO 499999]	labels.facet_contentLength_500kto1m=content_length:[500000 TO 999999]	labels.facet_contentLength_1m=content_length:[1000000 TO *]``
      | ``labels.facet_filetype_title:labels.facet_filetype_html=filetype:html	labels.facet_filetype_word=filetype:word	labels.facet_filetype_excel=filetype:excel	labels.facet_filetype_powerpoint=filetype:powerpoint	labels.facet_filetype_odt=filetype:odt	labels.facet_filetype_ods=filetype:ods	labels.facet_filetype_odp=filetype:odp	labels.facet_filetype_pdf=filetype:pdf	labels.facet_filetype_txt=filetype:txt	labels.facet_filetype_others=filetype:others``

.. list-table:: Ranking
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rank.fusion.window_size
    - Fenstergröße für Rank Fusion.
    - ``200``
  * - rank.fusion.rank_constant
    - Rang-Konstante für Rank Fusion.
    - ``20``
  * - rank.fusion.threads
    - Anzahl der Threads für Rank Fusion.
    - ``-1``
  * - rank.fusion.timeout
    - Maximale Zeit (Millisekunden), die auf die Searcher außer dem Haupt-Searcher gewartet wird, wenn Fess deren Ergebnisse selbst fusioniert (rank.fusion.engine.enabled=false). Ein Searcher, der bis dahin nicht geantwortet hat, wird aus dieser Suche ausgelassen, und die Ergebnisse werden als partiell und mit Timeout gekennzeichnet. Auf den Haupt-Searcher wird immer gewartet. 0 oder weniger wartet ohne Limit.
    - ``10000``
  * - rank.fusion.score_field
    - Score-Feld für Rank Fusion.
    - ``rf_score``
  * - rank.fusion.engine.enabled
    - Gibt an, ob die Suchmaschine Rank Fusion durchführt. Bei true steuern die Searcher, die teilnehmen können, ihre Abfragen zu einer einzigen Anfrage bei, sodass Facetten und Gesamttreffer die fusionierte Ergebnismenge beschreiben. Bei false fusioniert Fess die Ergebnisse der Searcher selbst.
    - ``false``
  * - rank.fusion.combination.technique
    - Wie die Suchmaschine die fusionierten Scores kombiniert: rrf, arithmetic_mean, geometric_mean oder harmonic_mean.
    - ``rrf``
  * - rank.fusion.normalization.technique
    - Wie Scores vor ihrer Kombination normalisiert werden: min_max, l2 oder z_score. Wird von rrf ignoriert. z_score kann nur mit arithmetic_mean kombiniert werden; jeder andere Mittelwert wird abgelehnt, und Fess fusioniert die Ergebnisse selbst.
    - ``min_max``
  * - rank.fusion.combination.weights
    - Gewicht pro Searcher für die Fusion auf Suchmaschinenseite als name:weight-Paare, z. B. default:0.7,semantic_chunk:0.3. Die Gewichte müssen in der Summe 1.0 ergeben und jeden teilnehmenden Searcher benennen. Leer gewichtet sie gleich.
    - (empty)
  * - rank.fusion.pagination_depth
    - Wie viele Ergebnisse jeder Searcher pro Shard zur Fusion auf Suchmaschinenseite beisteuert. Dies begrenzt sowohl, wie tief ein Client blättern kann, als auch die Menge der Dokumente, die die Suchmaschine in ein Ranking bringt: Eine fusionierte Suche blättert durch so viele Ergebnisse, jedoch nie durch mehr als indexer.max.result.window.size.
    - ``1000``

.. list-table:: ACL
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - smb.role.from.file
    - Gibt an, ob SMB-Rollen aus einer Datei bezogen werden sollen.
    - ``true``
  * - smb.available.sid.types
    - Verfügbare SID-Typen für SMB.
    - ``1,2,4:2,5:1``
  * - file.role.from.file
    - Gibt an, ob Datei-Rollen aus einer Datei bezogen werden sollen.
    - ``true``
  * - ftp.role.from.file
    - Gibt an, ob FTP-Rollen aus einer Datei bezogen werden sollen.
    - ``true``

.. list-table:: Sicherung
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.backup.targets
    - Zieldateien für die Index-Sicherung.
    - ``fess_basic_config.bulk,fess_config.bulk,fess_user.bulk,system.properties,fess.json,doc.json``
  * - index.backup.log.targets
    - Ziel-Protokolldateien für die Index-Sicherung.
    - ``chat_log.ndjson,click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
  * - index.backup.log.load.timeout
    - Timeout für das Laden von Index-Sicherungsprotokollen.
    - ``60000``

.. list-table:: Protokollierung
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - logging.app.packages
    - Anwendungspakete für die Protokollierung.
    - ``org.codelibs,org.dbflute,org.lastaflute``
  * - logging.search.docs.enabled
    - Gibt an, ob die Protokollierung von Suchdokumenten aktiviert werden soll.
    - ``true``
  * - logging.search.docs.fields
    - Felder, die für Suchdokumente protokolliert werden.
    - ``filetype,created,click_count,title,doc_id,url,score,site,filename,host,digest,boost,mimetype,favorite_count,_id,lang,last_modified,content_length,timestamp``
  * - logging.search.use.logfile
    - Gibt an, ob für die Suchprotokollierung eine Protokolldatei verwendet werden soll.
    - ``true``
  * - logging.search.max.queue.size
    - Maximale Warteschlangengröße für die Suchprotokollierung.
    - ``10000``
  * - logging.click.max.queue.size
    - Maximale Warteschlangengröße für die Klickprotokollierung.
    - ``10000``
  * - logging.chat.max.queue.size
    - Maximale Warteschlangengröße für die Chat-Nutzungsprotokollierung.
    - ``10000``
  * - search.history.enabled
    - Gibt an, ob die Suchbedingungen angemeldeter Benutzer für den Suchverlauf aufgezeichnet werden sollen.
    - ``true``
  * - search.history.size
    - Maximale Anzahl von Suchverlaufseinträgen, die pro Benutzer zurückgegeben werden.
    - ``10``
  * - user.tag.enabled
    - Gibt an, ob angemeldete Benutzer Dokumente taggen können. Jedes Tag gehört dem Benutzer, der es erstellt hat.
    - ``false``
  * - user.tag.name.max.length
    - Maximale Länge eines Tag-Namens in Codepoints.
    - ``50``
  * - user.tag.max.tags
    - Maximale Anzahl von Tags, die ein Benutzer besitzen kann.
    - ``1000``
  * - user.tag.max.paths
    - Maximale Anzahl von URLs, an denen ein Tag angebracht werden kann.
    - ``10000``
  * - user.tag.queue.max.size
    - Maximale Anzahl ausstehender Tag-Änderungen, die im Speicher gehalten werden, bis sie auf die Dokumente angewendet werden.
    - ``10000``
  * - user.tag.process.batch.size
    - Anzahl der pro Bulk-Anfrage aktualisierten URLs, wenn Tag-Änderungen auf die Dokumente angewendet werden.
    - ``100``
  * - user.tag.visible.max.size
    - Maximale Anzahl von Tags, die für einen Benutzer in einer Suche sichtbar sind.
    - ``1000``

Web
---

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - form.admin.max.input.size
    - Maximale Eingabegröße für Admin-Formulare.
    - ``10000``
  * - form.admin.label.in.config.enabled
    - Gibt an, ob Label in Admin-Konfigurationsformularen aktiviert werden soll.
    - ``false``
  * - form.admin.default.template.name
    - Standard-Vorlagenname für Admin-Formulare.
    - ``__TEMPLATE__``
  * - osdd.link.enabled
    - Gibt an, ob der OSDD-Link (OpenSearch Description Document) aktiviert werden soll.
    - ``auto``
  * - clipboard.copy.icon.enabled
    - Gibt an, ob das Symbol zum Kopieren in die Zwischenablage aktiviert werden soll.
    - ``true``
  * - authentication.admin.users
    - Administrator-Benutzernamen für die Authentifizierung.
    - ``admin``
  * - authentication.admin.users.ignore.case
    - Gibt an, ob authentication.admin.users ohne Beachtung der Groß-/Kleinschreibung abgeglichen wird: auto, true oder false. auto ignoriert die Groß-/Kleinschreibung, wenn ldap.provider.url gesetzt ist.
    - ``auto``
  * - authentication.admin.roles
    - Administrator-Rollennamen für die Authentifizierung.
    - ``admin``
  * - role.search.default.permissions
    - Standardberechtigungen für Suchrollen.
    - (empty)
  * - role.search.default.display.permissions
    - Standard-Anzeigeberechtigungen für Suchrollen.
    - ``{role}guest``
  * - role.search.guest.permissions
    - Halten Sie role.search.guest.permissions nicht leer. Es initialisiert die Gastrolle, die den anonymen Suchrollensatz nicht leer hält; ist der aufgelöste Rollensatz leer, wird der Rollenfilter übersprungen (Fail-Open), was die rollenbasierte Zugriffskontrolle deaktivieren und Dokumente für anonyme Benutzer offenlegen kann. Gastberechtigungen für Suchrollen.
    - ``{role}guest``
  * - role.search.user.prefix
    - Präfix für Benutzerrollen in der Suche.
    - ``1``
  * - role.search.group.prefix
    - Präfix für Gruppenrollen in der Suche.
    - ``2``
  * - role.search.role.prefix
    - Präfix für Rollen-Rollen in der Suche.
    - ``R``
  * - role.search.denied.prefix
    - Präfix für verweigerte Rollen in der Suche.
    - ``D``
  * - cookie.default.path
    - Der Standardpfad des Cookies (grundsätzlich '/', wenn kein Kontextpfad vorhanden ist)
    - ``/``
  * - cookie.default.expire
    - Die Standard-Ablaufzeit des Cookies in Sekunden z. B. 31556926: ein Jahr, 86400: ein Tag
    - ``3600``
  * - session.tracking.modes
    - Sitzungsverfolgungsmodi
    - ``cookie``
  * - session.cookie.secure
    - Gibt an, ob dem Sitzungs-Cookie (JSESSIONID) beim Start das Attribut Secure hinzugefügt wird. Bei leerem Wert (Standard) wird das automatische Verhalten von Tomcat verwendet (Secure wird nur bei HTTPS-Anfragen hinzugefügt). Setzen Sie ihn für HTTPS-Produktivumgebungen auf true, insbesondere wenn TLS an einem Reverse Proxy terminiert wird. Bei true wird das Cookie nicht über HTTP gesendet, sodass für reines HTTP keine Sitzungen aufgebaut werden; lassen Sie ihn für die Localhost-Entwicklung leer. Das Attribut Secure ist auch erforderlich, wenn SameSite=none verwendet wird. Eine Änderung dieses Werts erfordert einen Neustart.
    - (empty)
  * - cookie.search.parameter.keys
    - Kommagetrennte Liste von Anfrageparameter-Schlüsseln, die vor dem SSO-Login in Cookies gespeichert werden.
    - ``q,num,sort``
  * - cookie.search.parameter.required_keys
    - Kommagetrennte Liste erforderlicher Parameter-Schlüssel, die vorhanden sein müssen, um in Cookies gespeichert zu werden.
    - ``q``
  * - cookie.search.parameter.max.length
    - Maximale Länge der kodierten Suchparameter, die in Cookies gespeichert werden.
    - ``1000``
  * - cookie.search.parameter.max.decompressed.length
    - Maximale Größe in Bytes, auf die die gespeicherten Suchparameter dekomprimiert werden dürfen. Die obige Grenze gilt für das gzip-komprimierte Cookie, was keine Grenze für dessen entpackte Größe darstellt, und das Cookie stammt vom Client.
    - ``65536``
  * - cookie.search.parameter.max.restored.length
    - Maximale Länge des Query-Strings, der beim Wiederherstellen der gespeicherten Suchparameter nach der Anmeldung aufgebaut wird. Das Wiederherstellen ist eine Komfortfunktion, die Anmeldung dagegen nicht, daher wird ein längerer Query-String verworfen, anstatt in einen Location-Header geschrieben zu werden, den der Container ablehnen würde. Die Prozentkodierung vervielfacht eine CJK-Abfrage um das Neunfache, sodass dieser Wert weit kleiner ist, als die Abfrage selbst sein darf. Erhöhen Sie ihn zusammen mit tomcat.maxHttpHeaderSize in tomcat_config.properties, was die Antwort-Header begrenzt.
    - ``4096``
  * - cookie.search.parameter.name
    - Cookie-Name, der zum Speichern kodierter Suchparameter vor dem SSO-Login verwendet wird.
    - ``fsrp``
  * - cookie.search.parameter.http_only
    - Gibt an, ob das Attribut HttpOnly für das Suchparameter-Cookie gesetzt werden soll.
    - ``true``
  * - cookie.search.parameter.secure
    - Gibt an, ob das Attribut Secure für das Suchparameter-Cookie gesetzt werden soll. Sollte in Produktionsumgebungen mit HTTPS true sein.
    - (empty)
  * - cookie.search.parameter.max_age
    - Max-Age (in Sekunden) für das Suchparameter-Cookie. Verwenden Sie -1 für reine Sitzungs-Cookies.
    - ``60``
  * - cookie.search.parameter.domain
    - Domain-Attribut für das Suchparameter-Cookie. Legen Sie den Domain-Bereich fest, in dem das Cookie verfügbar sein soll (z. B. example.com).
    - (empty)
  * - cookie.search.parameter.path
    - Path-Attribut für das Suchparameter-Cookie. Wird typischerweise auf "/" oder den Kontextpfad der Anwendung gesetzt.
    - ``/``
  * - cookie.search.parameter.same_site
    - SameSite-Attribut für das Suchparameter-Cookie. Gültige Werte: Lax, Strict, None
    - ``Lax``
  * - paging.page.size
    - Die Größe einer Seite für die Paginierung
    - ``25``
  * - paging.page.range.size
    - Die Größe des Seitenbereichs für die Paginierung
    - ``5``
  * - paging.page.range.fill.limit
    - Die Option 'fillLimit' des Seitenbereichs für die Paginierung
    - ``true``

.. list-table:: Abrufgröße pro Seite
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - page.docboost.max.fetch.size
    - Maximale Anzahl von docboost-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.keymatch.max.fetch.size
    - Maximale Anzahl von keymatch-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.labeltype.max.fetch.size
    - Maximale Anzahl von labeltype-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.tagtype.max.fetch.size
    - Maximale Anzahl von tagtype-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.roletype.max.fetch.size
    - Maximale Anzahl von roletype-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.user.max.fetch.size
    - Maximale Anzahl von Benutzer-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.role.max.fetch.size
    - Maximale Anzahl von Rollen-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.group.max.fetch.size
    - Maximale Anzahl von Gruppen-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.crawling.info.param.max.fetch.size
    - Maximale Anzahl von Crawl-Info-Parametern, die pro Seite abgerufen werden.
    - ``100``
  * - page.crawling.info.max.fetch.size
    - Maximale Anzahl von Crawl-Info-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.data.config.max.fetch.size
    - Maximale Anzahl von Datenkonfigurations-Datensätzen, die pro Seite abgerufen werden.
    - ``100``
  * - page.web.config.max.fetch.size
    - Maximale Anzahl von Web-Konfigurations-Datensätzen, die pro Seite abgerufen werden.
    - ``100``
  * - page.file.config.max.fetch.size
    - Maximale Anzahl von Dateikonfigurations-Datensätzen, die pro Seite abgerufen werden.
    - ``100``
  * - page.duplicate.host.max.fetch.size
    - Maximale Anzahl von Duplikat-Host-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.failure.url.max.fetch.size
    - Maximale Anzahl von Fehler-URL-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.favorite.log.max.fetch.size
    - Maximale Anzahl von Favoritenprotokoll-Datensätzen, die pro Seite abgerufen werden.
    - ``100``
  * - page.file.auth.max.fetch.size
    - Maximale Anzahl von Datei-Authentifizierungs-Datensätzen, die pro Seite abgerufen werden.
    - ``100``
  * - page.web.auth.max.fetch.size
    - Maximale Anzahl von Web-Authentifizierungs-Datensätzen, die pro Seite abgerufen werden.
    - ``100``
  * - page.path.mapping.max.fetch.size
    - Maximale Anzahl von Pfad-Mapping-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.request.header.max.fetch.size
    - Maximale Anzahl von Anfrage-Header-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.scheduled.job.max.fetch.size
    - Maximale Anzahl von Datensätzen geplanter Jobs, die pro Seite abgerufen werden.
    - ``100``
  * - page.elevate.word.max.fetch.size
    - Maximale Anzahl von Datensätzen für zusätzliche Wörter, die pro Seite abgerufen werden.
    - ``1000``
  * - page.bad.word.max.fetch.size
    - Maximale Anzahl von Datensätzen für Ausschlusswörter, die pro Seite abgerufen werden.
    - ``1000``
  * - page.dictionary.max.fetch.size
    - Maximale Anzahl von Wörterbuch-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.relatedcontent.max.fetch.size
    - Maximale Anzahl von Datensätzen für verwandte Inhalte, die pro Seite abgerufen werden.
    - ``5000``
  * - page.relatedquery.max.fetch.size
    - Maximale Anzahl von Datensätzen für verwandte Abfragen, die pro Seite abgerufen werden.
    - ``5000``
  * - page.thumbnail.queue.max.fetch.size
    - Maximale Anzahl von Thumbnail-Warteschlangen-Datensätzen, die pro Seite abgerufen werden.
    - ``100``
  * - page.thumbnail.purge.max.fetch.size
    - Maximale Anzahl von Thumbnail-Bereinigungs-Datensätzen, die pro Seite abgerufen werden.
    - ``100``
  * - page.score.booster.max.fetch.size
    - Maximale Anzahl von Score-Booster-Datensätzen, die pro Seite abgerufen werden.
    - ``1000``
  * - page.searchlog.max.fetch.size
    - Maximale Anzahl von Suchprotokoll-Datensätzen, die pro Seite abgerufen werden.
    - ``10000``
  * - page.searchlist.track.total.hits
    - Gibt an, ob die Gesamttreffer auf der Suchlistenseite verfolgt werden sollen.
    - ``true``
  * - page.searchlist.content.max.length
    - Maximale Inhaltslänge (in Zeichen), die auf der Bearbeitungsseite der Suchliste dargestellt wird.
    - ``100000``

.. list-table:: Suchseite
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - paging.search.page.start
    - Standard-Startseite für Suchergebnisse.
    - ``0``
  * - paging.search.page.size
    - Standardgröße der Suchergebnisse pro Seite.
    - ``10``
  * - paging.search.page.max.size
    - Maximale Größe der Suchergebnisse pro Seite.
    - ``100``
  * - api.param.max.length
    - Maximale Länge eines String-Abfrageparameters der v2-API (q, sort, sdh). OWASP API4:2023.
    - ``1000``
  * - api.param.max.array.size
    - Maximale Anzahl von Werten für einen wiederholbaren Abfrageparameter der v2-API.
    - ``100``
  * - api.click.max.timestamp
    - Maximaler Klickprotokoll-Zeitstempel (rt, Epoch ms), der von der v2-Klick-API akzeptiert wird. OWASP API4:2023.
    - ``9999999999999``
  * - searchlog.agg.shard.size
    - searchlog
    - ``-1``
  * - searchlog.request.headers
    - Anfrage-Header, die in das Suchprotokoll aufgenommen werden.
    - (empty)
  * - searchlog.process.batch_size
    - Batchgröße für die Suchprotokollverarbeitung.
    - ``100``
  * - related_query.generate.days
    - Anzahl der Tage an Suchprotokollen, die beim Generieren verwandter Abfragen aus Suchprotokollen gelesen werden.
    - ``30``
  * - related_query.generate.term.size
    - Maximale Anzahl von Begriffen, die pro virtuellem Host generiert werden.
    - ``100``
  * - related_query.generate.query.size
    - Maximale Anzahl verwandter Abfragen, die pro Begriff generiert werden.
    - ``5``
  * - related_query.generate.min.sessions
    - Mindestanzahl unterschiedlicher Benutzersitzungen, die für einen Begriff und für jede seiner verwandten Abfragen erforderlich ist.
    - ``3``
  * - related_query.generate.session.interval
    - Intervall (Minuten) nach einer Suche, innerhalb dessen eine Folgesuche derselben Sitzung als Verfeinerung zählt.
    - ``10``
  * - related_query.generate.seed.log.size
    - Maximale Anzahl von Suchprotokollen eines Begriffs, die gelesen werden, um die Sitzungen zu finden, die danach gesucht haben.
    - ``1000``
  * - related_query.generate.seed.session.size
    - Maximale Anzahl von Sitzungen pro Begriff, deren Folgesuchen gelesen werden.
    - ``200``
  * - related_query.generate.log.fetch.size
    - Maximale Anzahl von Folgesuch-Protokollen, die pro Begriff gelesen werden.
    - ``2000``
  * - related_query.generate.query.min.length
    - Mindestlänge (in Zeichen) eines generierten Begriffs oder einer verwandten Abfrage.
    - ``2``
  * - related_query.generate.query.max.length
    - Maximale Länge (in Zeichen) eines generierten Begriffs oder einer verwandten Abfrage.
    - ``50``
  * - docreport.duplicate.group.size
    - docreport Maximale Anzahl von Duplikatgruppen, die die Dokumentbericht-Seite anzeigt, die größten zuerst.
    - ``100``
  * - docreport.duplicate.docs.size
    - Maximale Anzahl von Dokumenten, die die Dokumentbericht-Seite für jede Duplikatgruppe auflistet.
    - ``10``
  * - docreport.duplicate.export.page.size
    - Anzahl der Inhaltssignaturen, die pro Anfrage gelesen werden, wenn der Duplikatbericht als CSV heruntergeladen wird.
    - ``10000``
  * - docreport.dormant.days
    - Standardanzahl von Tagen seit der letzten Änderung, nach denen ein Dokument als inaktiv gilt.
    - ``365``
  * - thumbnail.html.image.min.width
    - Mindestbreite für HTML-Bilder in Thumbnails.
    - ``100``
  * - thumbnail.html.image.min.height
    - Mindesthöhe für HTML-Bilder in Thumbnails.
    - ``100``
  * - thumbnail.html.image.max.aspect.ratio
    - Maximales Seitenverhältnis für HTML-Bilder in Thumbnails.
    - ``3.0``
  * - thumbnail.html.image.thumbnail.width
    - Breite generierter Thumbnail-Bilder.
    - ``100``
  * - thumbnail.html.image.thumbnail.height
    - Höhe generierter Thumbnail-Bilder.
    - ``100``
  * - thumbnail.html.image.format
    - Format generierter Thumbnail-Bilder.
    - ``png``
  * - thumbnail.html.image.xpath
    - XPath zur Auswahl von Bildern für Thumbnails.
    - ``//IMG``
  * - thumbnail.html.image.exclude.extensions
    - Dateierweiterungen, die von der Thumbnail-Generierung ausgeschlossen werden.
    - ``svg,html,css,js``
  * - thumbnail.generator.interval
    - Intervall für den Thumbnail-Generator.
    - ``0``
  * - thumbnail.generator.targets
    - Ziele für den Thumbnail-Generator (z. B. all).
    - ``all``
  * - thumbnail.crawler.enabled
    - Gibt an, ob der Thumbnail-Crawler aktiviert ist.
    - ``true``
  * - thumbnail.system.monitor.interval
    - Intervall für die Systemüberwachung bei der Thumbnail-Verarbeitung.
    - ``60``

.. list-table:: Benutzer
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - user.code.request.parameter
    - Benutzercode-Einstellungen
    - ``userCode``
  * - user.code.min.length
    - Mindestlänge des Benutzercodes.
    - ``20``
  * - user.code.max.length
    - Maximale Länge des Benutzercodes.
    - ``100``
  * - user.code.pattern
    - Muster des Benutzercodes für die Validierung.
    - ``[a-zA-Z0-9_]+``
  * - mail.from.name
    - Name, der im Feld From von E-Mails angezeigt wird.
    - ``Administrator``
  * - mail.from.address
    - E-Mail-Adresse, die im Feld From verwendet wird.
    - ``root@localhost``
  * - mail.hostname
    - Hostname des Mailservers.
    - (empty)
  * - scheduler.target.name
    - Zielname für den Scheduler.
    - (empty)
  * - scheduler.job.class
    - Job-Klasse für den Scheduler.
    - ``org.codelibs.fess.app.job.ScriptExecutorJob``
  * - scheduler.concurrent.exec.mode
    - Modus für die gleichzeitige Ausführung im Scheduler.
    - ``QUIT``
  * - scheduler.monitor.interval
    - Intervall für die Scheduler-Überwachung.
    - ``30``
  * - coordinator.poll.interval
    - Intervall (Sekunden) für das Abfragen von Heartbeats und Ereignissen.
    - ``60``
  * - coordinator.heartbeat.ttl
    - Time-to-live (ms) für Instanz-Heartbeat-Dokumente.
    - ``180000``
  * - coordinator.operation.ttl
    - Time-to-live (ms) für Vorgangssperr-Dokumente.
    - ``7200000``
  * - coordinator.operation.retry
    - Maximale Anzahl von Wiederholungen beim Erwerb einer Vorgangssperre.
    - ``3``
  * - coordinator.event.ttl
    - Time-to-live (ms) für Ereignisbenachrichtigungs-Dokumente.
    - ``600000``
  * - online.help.base.link
    - Basis-Link für die Online-Hilfe.
    - ``https://fess.codelibs.org/{lang}/{version}/admin/``
  * - online.help.installation
    - Link zur Installationsanleitung für die Online-Hilfe.
    - ``https://fess.codelibs.org/{lang}/{version}/install/install.html``
  * - online.help.eol
    - Link zu den End-of-Life-Informationen für die Online-Hilfe.
    - ``https://fess.codelibs.org/{lang}/eol.html``
  * - online.help.name.failureurl
    - Online-Hilfe-Schlüssel für Fehler-URL.
    - ``failureurl``
  * - online.help.name.elevateword
    - Online-Hilfe-Schlüssel für Zusätzliches Wort.
    - ``elevateword``
  * - online.help.name.reqheader
    - Online-Hilfe-Schlüssel für Anfrage-Header.
    - ``reqheader``
  * - online.help.name.dict.synonym
    - Online-Hilfe-Schlüssel für Synonym-Wörterbuch.
    - ``synonym``
  * - online.help.name.dict
    - Online-Hilfe-Schlüssel für Wörterbuch.
    - ``dict``
  * - online.help.name.dict.kuromoji
    - Online-Hilfe-Schlüssel für Kuromoji-Wörterbuch.
    - ``kuromoji``
  * - online.help.name.dict.protwords
    - Online-Hilfe-Schlüssel für Protwords-Wörterbuch.
    - ``protwords``
  * - online.help.name.dict.stopwords
    - Online-Hilfe-Schlüssel für Stoppwort-Wörterbuch.
    - ``stopwords``
  * - online.help.name.dict.stemmeroverride
    - Online-Hilfe-Schlüssel für Stemmer-Überschreibungs-Wörterbuch.
    - ``stemmeroverride``
  * - online.help.name.dict.mapping
    - Online-Hilfe-Schlüssel für Mapping-Wörterbuch.
    - ``mapping``
  * - online.help.name.webconfig
    - Online-Hilfe-Schlüssel für Web-Konfiguration.
    - ``webconfig``
  * - online.help.name.searchlist
    - Online-Hilfe-Schlüssel für Suchliste.
    - ``searchlist``
  * - online.help.name.log
    - Online-Hilfe-Schlüssel für Protokolldatei.
    - ``log``
  * - online.help.name.general
    - Online-Hilfe-Schlüssel für Allgemeine Einstellungen.
    - ``general``
  * - online.help.name.role
    - Online-Hilfe-Schlüssel für Rolle.
    - ``role``
  * - online.help.name.joblog
    - Online-Hilfe-Schlüssel für Jobprotokoll.
    - ``joblog``
  * - online.help.name.keymatch
    - Online-Hilfe-Schlüssel für Schlüsselübereinstimmung.
    - ``keymatch``
  * - online.help.name.relatedquery
    - Online-Hilfe-Schlüssel für Verwandte Abfrage.
    - ``relatedquery``
  * - online.help.name.relatedcontent
    - Online-Hilfe-Schlüssel für Verwandter Inhalt.
    - ``relatedcontent``
  * - online.help.name.wizard
    - Online-Hilfe-Schlüssel für Konfigurations-Assistent.
    - ``wizard``
  * - online.help.name.badword
    - Online-Hilfe-Schlüssel für Ausschlusswort.
    - ``badword``
  * - online.help.name.pathmap
    - Online-Hilfe-Schlüssel für Pfad-Mapping.
    - ``pathmap``
  * - online.help.name.boostdoc
    - Online-Hilfe-Schlüssel für Dokument-Boosting.
    - ``boostdoc``
  * - online.help.name.dataconfig
    - Online-Hilfe-Schlüssel für Datenkonfiguration.
    - ``dataconfig``
  * - online.help.name.systeminfo
    - Online-Hilfe-Schlüssel für Systeminformationen.
    - ``systeminfo``
  * - online.help.name.user
    - Online-Hilfe-Schlüssel für Benutzer.
    - ``user``
  * - online.help.name.group
    - Online-Hilfe-Schlüssel für Gruppe.
    - ``group``
  * - online.help.name.dashboard
    - Online-Hilfe-Schlüssel für Dashboard.
    - ``dashboard``
  * - online.help.name.webauth
    - Online-Hilfe-Schlüssel für Web-Authentifizierung.
    - ``webauth``
  * - online.help.name.fileconfig
    - Online-Hilfe-Schlüssel für Dateikonfiguration.
    - ``fileconfig``
  * - online.help.name.fileauth
    - Online-Hilfe-Schlüssel für Datei-Authentifizierung.
    - ``fileauth``
  * - online.help.name.labeltype
    - Online-Hilfe-Schlüssel für Labeltyp.
    - ``labeltype``
  * - online.help.name.tagtype
    - Online-Hilfe-Schlüssel für Tag-Typ.
    - ``tagtype``
  * - online.help.name.duplicatehost
    - Online-Hilfe-Schlüssel für Duplikat-Host.
    - ``duplicatehost``
  * - online.help.name.scheduler
    - Online-Hilfe-Schlüssel für Scheduler.
    - ``scheduler``
  * - online.help.name.crawlinginfo
    - Online-Hilfe-Schlüssel für Crawl-Informationen.
    - ``crawlinginfo``
  * - online.help.name.backup
    - Online-Hilfe-Schlüssel für Sicherung.
    - ``backup``
  * - online.help.name.upgrade
    - Online-Hilfe-Schlüssel für Aktualisierung.
    - ``upgrade``
  * - online.help.name.sereq
    - Online-Hilfe-Schlüssel für Abfrageanforderung.
    - ``sereq``
  * - online.help.name.accesstoken
    - Online-Hilfe-Schlüssel für Zugriffstoken.
    - ``accesstoken``
  * - online.help.name.suggest
    - Online-Hilfe-Schlüssel für Vorschlag.
    - ``suggest``
  * - online.help.name.searchlog
    - Online-Hilfe-Schlüssel für Suchprotokoll.
    - ``searchlog``
  * - online.help.name.maintenance
    - Online-Hilfe-Schlüssel für Wartung.
    - ``maintenance``
  * - online.help.name.plugin
    - Online-Hilfe-Schlüssel für Plugin.
    - ``plugin``
  * - online.help.name.storage
    - Online-Hilfe-Schlüssel für Speicher.
    - ``storage``
  * - online.help.name.docreport
    - Online-Hilfe-Schlüssel für den Dokumentbericht.
    - ``docreport``
  * - online.help.supported.langs
    - Unterstützte Sprachen für die Online-Hilfe.
    - ``de,es,fr,ja,ko,zh-cn``
  * - forum.link
    - Forum-Link für den Benutzersupport.
    - ``https://discuss.codelibs.org/c/Fess{lang}/``
  * - forum.supported.langs
    - Unterstützte Sprachen für das Forum.
    - ``en,ja``
  * - suggest.popular.word.seed
    - Seed-Wert für Vorschläge beliebter Wörter.
    - ``0``
  * - suggest.popular.word.tags
    - Tags für Vorschläge beliebter Wörter.
    - (empty)
  * - suggest.popular.word.fields
    - Felder für Vorschläge beliebter Wörter.
    - (empty)
  * - suggest.popular.word.excludes
    - Ausgeschlossene Wörter für Vorschläge beliebter Wörter.
    - (empty)
  * - suggest.popular.word.size
    - Anzahl der vorzuschlagenden beliebten Wörter.
    - ``10``
  * - suggest.popular.word.window.size
    - Fenstergröße für Vorschläge beliebter Wörter.
    - ``30``
  * - suggest.popular.word.query.freq
    - Abfragehäufigkeit für Vorschläge beliebter Wörter.
    - ``10``
  * - suggest.min.hit.count
    - Minimale Trefferanzahl für Vorschläge.
    - ``1``
  * - suggest.field.contents
    - Feld für Vorschlagsinhalte.
    - ``_default``
  * - suggest.field.tags
    - Feld für Vorschlags-Tags.
    - ``label``
  * - suggest.field.roles
    - Feld für Vorschlagsrollen.
    - ``role``
  * - suggest.field.index.contents
    - Indexinhalte für Vorschläge.
    - ``content,title``
  * - suggest.update.request.interval
    - Intervall für Vorschlags-Aktualisierungsanfragen.
    - ``0``
  * - suggest.update.doc.per.request
    - Anzahl der Dokumente pro Vorschlags-Aktualisierungsanfrage.
    - ``2``
  * - suggest.update.contents.limit.num.percentage
    - Prozentuale Obergrenze für Vorschlags-Aktualisierungsinhalte.
    - ``50%``
  * - suggest.update.contents.limit.num
    - Maximale Anzahl von Vorschlags-Aktualisierungsinhalten.
    - ``10000``
  * - suggest.update.contents.limit.doc.size
    - Maximale Dokumentgröße für die Vorschlagsaktualisierung.
    - ``50000``
  * - suggest.source.reader.scroll.size
    - Scroll-Größe für den Vorschlags-Quellleser.
    - ``1``
  * - suggest.popular.word.cache.size
    - Cache-Größe für Vorschläge beliebter Wörter.
    - ``1000``
  * - suggest.popular.word.cache.expire
    - Cache-Ablauf (Sekunden) für Vorschläge beliebter Wörter.
    - ``60``
  * - suggest.search.log.permissions
    - Berechtigungen für das Vorschlags-Suchprotokoll.
    - ``{user}guest,{role}guest``
  * - suggest.system.monitor.interval
    - Intervall für die Systemüberwachung bei Vorschlägen.
    - ``60``
  * - ldap.admin.enabled
    - Gibt an, ob die LDAP-Administration aktiviert ist.
    - ``false``
  * - ldap.admin.user.filter
    - Benutzerfilter für die LDAP-Administration.
    - ``uid=%s``
  * - ldap.admin.user.base.dn
    - Base DN für den LDAP-Administrationsbenutzer.
    - ``ou=People,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.user.object.classes
    - Objektklassen für den LDAP-Administrationsbenutzer.
    - ``organizationalPerson,top,person,inetOrgPerson``
  * - ldap.admin.role.filter
    - Rollenfilter für die LDAP-Administration.
    - ``cn=%s``
  * - ldap.admin.role.base.dn
    - Base DN für die LDAP-Administrationsrolle.
    - ``ou=Role,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.role.object.classes
    - Objektklassen für die LDAP-Administrationsrolle.
    - ``groupOfNames``
  * - ldap.admin.group.filter
    - Gruppenfilter für die LDAP-Administration.
    - ``cn=%s``
  * - ldap.admin.group.base.dn
    - Base DN für die LDAP-Administrationsgruppe.
    - ``ou=Group,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.group.object.classes
    - Objektklassen für die LDAP-Administrationsgruppe.
    - ``groupOfNames``
  * - ldap.admin.sync.password
    - Gibt an, ob das Passwort für die LDAP-Administration synchronisiert werden soll.
    - ``true``
  * - ldap.auth.validation
    - Gibt an, ob die LDAP-Authentifizierung validiert werden soll.
    - ``true``
  * - ldap.connect.timeout
    - Timeout (Millisekunden) für den Aufbau einer LDAP-Verbindung. Dies begrenzt auch den TLS-Handshake und die erste Bind-Antwort. 0 oder weniger überlässt es dem Standard des JDK/OS.
    - ``10000``
  * - ldap.read.timeout
    - Timeout (Millisekunden) für das Warten auf eine LDAP-Antwort, nachdem die Verbindung gebunden wurde. 0 oder weniger wartet unbegrenzt.
    - ``30000``
  * - ldap.search.time.limit
    - Serverseitiges Zeitlimit (Millisekunden) für eine LDAP-Suche. 0 oder weniger bedeutet kein Limit.
    - ``60000``
  * - ldap.max.username.length
    - Maximale Benutzernamenlänge für LDAP.
    - ``-1``
  * - ldap.ignore.netbios.name
    - Gibt an, ob der NetBIOS-Name in LDAP ignoriert werden soll.
    - ``true``
  * - ldap.group.name.with.underscores
    - Gibt an, ob Unterstriche in LDAP-Gruppennamen zugelassen werden sollen.
    - ``false``
  * - ldap.lowercase.permission.name
    - Gibt an, ob für LDAP-Berechtigungsnamen Kleinbuchstaben verwendet werden sollen.
    - ``false``
  * - ldap.allow.empty.permission
    - Gibt an, ob leere Berechtigungen in LDAP zugelassen werden sollen.
    - ``true``
  * - ldap.samaccountname.group
    - Gibt an, ob samAccountName für die LDAP-Gruppe verwendet werden soll.
    - ``false``
  * - ldap.role.search.user.enabled
    - Gibt an, ob die LDAP-Rollensuche für Benutzer aktiviert ist.
    - ``true``
  * - ldap.role.search.group.enabled
    - Gibt an, ob die LDAP-Rollensuche für Gruppen aktiviert ist.
    - ``true``
  * - ldap.role.search.role.enabled
    - Gibt an, ob die LDAP-Rollensuche für Rollen aktiviert ist.
    - ``true``
  * - ldap.attr.surname
    - LDAP-Attribut für Nachname.
    - ``sn``
  * - ldap.attr.givenName
    - LDAP-Attribut für Vorname.
    - ``givenName``
  * - ldap.attr.employeeNumber
    - LDAP-Attribut für Mitarbeiternummer.
    - ``employeeNumber``
  * - ldap.attr.mail
    - LDAP-Attribut für E-Mail.
    - ``mail``
  * - ldap.attr.telephoneNumber
    - LDAP-Attribut für Telefonnummer.
    - ``telephoneNumber``
  * - ldap.attr.homePhone
    - LDAP-Attribut für Privattelefon.
    - ``homePhone``
  * - ldap.attr.homePostalAddress
    - LDAP-Attribut für private Postanschrift.
    - ``homePostalAddress``
  * - ldap.attr.labeledURI
    - LDAP-Attribut für Labeled URI.
    - ``labeledURI``
  * - ldap.attr.roomNumber
    - LDAP-Attribut für Raumnummer.
    - ``roomNumber``
  * - ldap.attr.description
    - LDAP-Attribut für Beschreibung.
    - ``description``
  * - ldap.attr.title
    - LDAP-Attribut für Titel.
    - ``title``
  * - ldap.attr.pager
    - LDAP-Attribut für Pager.
    - ``pager``
  * - ldap.attr.street
    - LDAP-Attribut für Straße.
    - ``street``
  * - ldap.attr.postalCode
    - LDAP-Attribut für Postleitzahl.
    - ``postalCode``
  * - ldap.attr.physicalDeliveryOfficeName
    - LDAP-Attribut für Name des physischen Zustellungsbüros.
    - ``physicalDeliveryOfficeName``
  * - ldap.attr.destinationIndicator
    - LDAP-Attribut für Zielindikator.
    - ``destinationIndicator``
  * - ldap.attr.internationaliSDNNumber
    - LDAP-Attribut für internationale ISDN-Nummer.
    - ``internationaliSDNNumber``
  * - ldap.attr.state
    - LDAP-Attribut für Bundesland.
    - ``st``
  * - ldap.attr.employeeType
    - LDAP-Attribut für Mitarbeitertyp.
    - ``employeeType``
  * - ldap.attr.facsimileTelephoneNumber
    - LDAP-Attribut für Faxnummer.
    - ``facsimileTelephoneNumber``
  * - ldap.attr.postOfficeBox
    - LDAP-Attribut für Postfach.
    - ``postOfficeBox``
  * - ldap.attr.initials
    - LDAP-Attribut für Initialen.
    - ``initials``
  * - ldap.attr.carLicense
    - LDAP-Attribut für Kfz-Kennzeichen.
    - ``carLicense``
  * - ldap.attr.mobile
    - LDAP-Attribut für Mobiltelefon.
    - ``mobile``
  * - ldap.attr.postalAddress
    - LDAP-Attribut für Postanschrift.
    - ``postalAddress``
  * - ldap.attr.city
    - LDAP-Attribut für Stadt.
    - ``l``
  * - ldap.attr.teletexTerminalIdentifier
    - LDAP-Attribut für Teletex-Terminalkennung.
    - ``teletexTerminalIdentifier``
  * - ldap.attr.x121Address
    - LDAP-Attribut für X.121-Adresse.
    - ``x121Address``
  * - ldap.attr.businessCategory
    - LDAP-Attribut für Geschäftskategorie.
    - ``businessCategory``
  * - ldap.attr.registeredAddress
    - LDAP-Attribut für registrierte Adresse.
    - ``registeredAddress``
  * - ldap.attr.displayName
    - LDAP-Attribut für Anzeigename.
    - ``displayName``
  * - ldap.attr.preferredLanguage
    - LDAP-Attribut für bevorzugte Sprache.
    - ``preferredLanguage``
  * - ldap.attr.departmentNumber
    - LDAP-Attribut für Abteilungsnummer.
    - ``departmentNumber``
  * - ldap.attr.uidNumber
    - LDAP-Attribut für UID-Nummer.
    - ``uidNumber``
  * - ldap.attr.gidNumber
    - LDAP-Attribut für GID-Nummer.
    - ``gidNumber``
  * - ldap.attr.homeDirectory
    - LDAP-Attribut für Home-Verzeichnis.
    - ``homeDirectory``
  * - plugin.repositories
    - Plugin-Repository-URLs.
    - ``https://maven.codelibs.org/release/org/codelibs/fess/,https://repo.maven.apache.org/maven2/org/codelibs/fess/,https://fess.codelibs.org/plugin/artifacts.yaml``
  * - plugin.version.filter
    - Versionsfilter für Plugins.
    - (empty)
  * - storage.max.items.in.page
    - Maximale Anzahl von Elementen pro Seite im Speicher.
    - ``1000``
  * - password.invalid.admin.passwords
    - Liste ungültiger Administratorpasswörter.
    - ``admin``
  * - password.min.length
    - Minimale Passwortlänge (0 zum Deaktivieren).
    - ``8``
  * - password.max.length
    - Maximale Länge eines Passwortfelds.
    - ``100``
  * - password.require.uppercase
    - Großbuchstaben im Passwort verlangen.
    - ``false``
  * - password.require.lowercase
    - Kleinbuchstaben im Passwort verlangen.
    - ``false``
  * - password.require.digit
    - Ziffern im Passwort verlangen.
    - ``false``
  * - password.require.special.char
    - Sonderzeichen im Passwort verlangen.
    - ``false``
  * - rag.chat.enabled
    - Gibt an, ob die RAG-Chat-Funktion aktiviert ist.
    - ``false``
  * - rag.chat.log.enabled
    - Gibt an, ob die Nutzung jeder RAG-Chat-Anfrage (Benutzer, Zeit, LLM-Aufrufe und Tokens) im Chat-Protokoll aufgezeichnet werden soll. Die Frage und die Antwort werden nie aufgezeichnet.
    - ``true``
  * - rag.chat.context.max.documents
    - Einstellungen zur Chat-Generierung.
    - ``5``
  * - rag.chat.query.regeneration.max.count
    - Maximale Anzahl, wie oft eine Chat-Anfrage ihre Suchabfrage neu generiert und erneut sucht, wenn die Suche keine Dokumente findet oder im Streaming-Chat keiner der Treffer als relevant beurteilt wird. Jede Neugenerierung führt einen LLM-Aufruf aus, plus einen Aufruf zur Relevanzbewertung, wenn die neue Suche Treffer hat (0 deaktiviert).
    - ``2``
  * - rag.chat.session.timeout.minutes
    - Sitzungseinstellungen.
    - ``30``
  * - rag.chat.session.max.size
    - Maximale Anzahl zwischengespeicherter Chat-Sitzungen; darüber hinaus werden die am längsten nicht abgerufenen verdrängt (0 oder weniger bedeutet 100).
    - ``10000``
  * - rag.chat.history.max.messages
    - Maximale Anzahl von Nachrichten, die in einer Chat-Sitzung gehalten werden; ältere Gesprächsrunden werden bei jeder neuen Nachricht gekürzt.
    - ``30``
  * - rag.chat.content.fields
    - Einstellungen für den erweiterten RAG-Ablauf. Felder, die für den vollständigen Dokumentinhalt abgerufen werden.
    - ``title,url,content,doc_id,content_title,content_description``
  * - rag.chat.highlight.fragment.size
    - Hervorhebungseinstellungen für die RAG-Suche.
    - ``500``
  * - rag.chat.highlight.number.of.fragments
    - Anzahl der Hervorhebungsfragmente pro Dokument in der Kontextsuche des RAG-Chats.
    - ``3``
  * - rag.chat.content.fulltext.max.length
    - Behandlung großer Dokumente bei der Antwortgenerierung. Dokumente, deren content_length diesen Wert überschreitet, verwenden im Antwortkontext hervorgehobene Passagen anstelle des vollständigen Inhalts.
    - ``3000``
  * - rag.chat.answer.highlight.fragment.size
    - Hervorhebungseinstellungen, die beim Extrahieren von Passagen aus großen Dokumenten für den Antwortkontext verwendet werden.
    - ``1000``
  * - rag.chat.answer.highlight.number.of.fragments
    - Anzahl der Hervorhebungsfragmente, die aus jedem übergroßen Dokument für den Antwortkontext entnommen werden.
    - ``5``
  * - rag.chat.history.assistant.content
    - Verlaufsinhaltsmodus für Assistenten-Nachrichten. smart_summary           - Assistenten-Text verwerfen, pro Gesprächsrunde nur vergangene Suchabfrage + referenzierte Titel behalten (Standard, empfohlen) full                    - gesamte Assistenten-Antwort senden source_titles           - Text + Suffix aus referenzierten Titeln source_titles_and_urls  - nur "[References: title (url), ...]" truncated               - Assistenten-Antwort bei history.assistant.max.chars abschneiden none                    - Assistenten-Gesprächsrunden aus dem Verlauf verwerfen
    - ``smart_summary``
  * - rag.chat.history.titles.max.count
    - Maximale Anzahl referenzierter Dokumenttitel, die pro Gesprächsrunde im Verlaufsmodus smart_summary enthalten sind.
    - ``5``
  * - rag.chat.document.max.parts
    - Maximale Anzahl von Teilen, in die ein Dokument aufgeteilt wird, wenn über ein einzelnes Dokument gechattet wird, das länger als das LLM-Kontextbudget ist. Jeder Teil wird separat zusammengefasst, und die Zusammenfassungen werden zur Antwort kombiniert; Teile über dieser Anzahl werden nicht verwendet. Eine Anfrage zu einem solchen Dokument führt in jeder Gesprächsrunde bis zu so viele LLM-Aufrufe plus einen für die Antwort aus.
    - ``10``
  * - rag.chat.response.language
    - Sprache, in der das LLM antworten soll. browser  - die Sprache des Browsers oder der UI-Locale des Benutzers; keine Anweisung für Englisch (Standard) none     - keine Sprachanweisung; das LLM antwortet normalerweise in der Sprache der Frage en, ja.. - immer in dieser Sprache antworten
    - ``browser``
  * - index.export.path
    - Index-Export
    - ``/var/lib/fess/export``
  * - index.export.exclude.fields
    - Kommagetrennte Dokumentfelder, die in den vom Index-Export-Job geschriebenen Dateien weggelassen werden.
    - ``cache,tag``
  * - index.export.scroll.size
    - Anzahl der Dokumente, die der Index-Export-Job pro Scroll-Anfrage abruft.
    - ``100``
  * - index.export.format
    - Ausgabeformat für exportierte Dokumente; nur html und json werden akzeptiert, alles andere lässt den Job fehlschlagen.
    - ``html``
  * - log.notification.flush.interval
    - Protokollbenachrichtigung Intervall (Sekunden) zum Leeren des Protokollbenachrichtigungspuffers in die Suchmaschine.
    - ``30``
  * - log.notification.max.details.length
    - Maximale Länge des Benachrichtigungs-Detailtexts.
    - ``3000``
  * - log.notification.max.display.events
    - Maximale Anzahl von Ereignissen, die in der Benachrichtigung angezeigt werden.
    - ``50``
  * - log.notification.max.message.length
    - Maximale Länge jeder Protokollmeldung in der Benachrichtigung.
    - ``200``
  * - log.notification.search.size
    - Maximale Anzahl von Ereignissen, die pro Benachrichtigungs-Job von der Suchmaschine abgerufen werden.
    - ``1000``
  * - log.notification.buffer.size
    - Maximale Anzahl von Ereignissen, die im Speicher gepuffert werden.
    - ``1000``
  * - log.notification.interval
    - Intervall (Sekunden) für den Zyklus des Benachrichtigungs-Jobs, das in Benachrichtigungsmeldungen verwendet wird.
    - ``300``
  * - theme.directory.path
    - Statisches Theme-System (siehe docs/superpowers/specs/2026-05-21-fess-static-theme-design.md)
    - ``themes``
  * - theme.upload.max.size
    - Maximale Größe (Bytes) eines hochgeladenen Theme-Archivs.
    - ``52428800``
  * - theme.upload.max.extracted.size
    - Maximale entpackte Gesamtgröße (Bytes); das Entpacken wird abgebrochen, sobald sie überschritten wird.
    - ``209715200``
  * - theme.upload.max.entries
    - Maximal zulässige Anzahl von Einträgen in einem hochgeladenen Theme-Archiv.
    - ``1000``
  * - theme.upload.max.compression.ratio
    - Maximales Verhältnis unkomprimiert/komprimiert für einen einzelnen Theme-Archiv-Eintrag.
    - ``100``
  * - theme.upload.zip.ratio.max
    - Maximales kumuliertes Verhältnis unkomprimiert/komprimiert für das gesamte Archiv (Zip-Bomb-Schutz).
    - ``50``
  * - theme.upload.zip.ratio.check.threshold.bytes
    - Gelesene komprimierte Bytes, bevor die Prüfung des kumulierten ZIP-Verhältnisses greift; kleinere Archive überspringen sie.
    - ``65536``
  * - theme.upload.attic.retention.days
    - Aufbewahrung (Tage) für ein ersetztes Theme-Verzeichnis, bevor der Bereinigungslauf es entfernt.
    - ``7``
  * - theme.repositories
    - Repository-URLs (kommagetrennt), von denen statische Themes heruntergeladen werden.
    - ``https://maven.codelibs.org/release/org/codelibs/fess/themes/``
  * - theme.index.frame.ancestors
    - Wert der Direktive frame-ancestors in der Content-Security-Policy der HTML-Seiten des statischen Themes: die Origins, die sie in einem Frame einbetten dürfen. Der Standardwert 'none' erlaubt keiner Seite, sie einzubetten. WebKit (Safari) wendet frame-ancestors auf die blob:-Frames an, die die Dateivorschau und die Cache-Ansicht eines Themes verwenden, und zeigt sie daher leer an, solange der Wert 'none' ist. Lassen Sie den Wert leer, um die Direktive wegzulassen; X-Frame-Options: DENY wird in jedem Fall gesendet und hält die Seiten dann in jedem Browser aus Frames fern (ein Browser, der frame-ancestors berücksichtigt, ignoriert diesen Header).
    - ``'none'``
  * - theme.api.csrf.server.origins
    - Optional: kanonische externe(r) Origin(s) dieser Fess-Instanz (durch Komma/Zeilenumbruch getrennt), z. B. https://fess.example.com. Wenn gesetzt, werden diese für die v2-CSRF-Origin-Prüfung als Same-Origin behandelt, OHNE weitergeleiteten Headern zu vertrauen. Empfohlen hinter Reverse Proxies, die nicht in rate.limit.trusted.proxies aufgeführt sind. Wenn leer, wird der Ziel-Origin aus den X-Forwarded-\*-Headern vertrauenswürdiger Proxies rekonstruiert, dann aus der Servlet-Anfrage.
    - (empty)
  * - theme.api.login.rate.limit.per.ip.per.minute
    - Zulässige Anmeldeversuche pro Client-IP und Minute; 0 oder weniger deaktiviert die Begrenzung.
    - ``10``
  * - theme.api.login.rate.limit.per.user.per.minute
    - Zulässige Anmeldeversuche pro Client-IP und Benutzername und Minute; begrenzt auch die Passwortänderung.
    - ``5``
  * - theme.api.login.lockout.seconds
    - Sperrzeit (Sekunden), die angewendet wird, sobald ein Login-Rate-Limit überschritten wird; 0 oder weniger deaktiviert die Sperre.
    - ``900``
  * - theme.api.login.rate.limit.max.entries
    - Maximale Anzahl von Login-Rate-Limit-Buckets im Speicher; inaktive Buckets werden bei Erreichen der Obergrenze verdrängt.
    - ``100000``
  * - api.chat.stream.keepalive.interval.ms
    - Intervall zwischen den SSE-Keep-alive-Pings, die von /api/v2/chat/stream ausgegeben werden. Der Ping ist eine reine Kommentarzeile (": keepalive\\n\\n"), die den Event-Stream nicht beeinflusst, aber Zwischeninstanzen umgeht (der nginx-Standardwert für proxy_read_timeout ist 60s), die inaktive Verbindungen während langer LLM-Phasen trennen. Setzen Sie <=0 zum Deaktivieren. Einheit: Millisekunden.
    - ``15000``
.. GENERATED-END: properties
