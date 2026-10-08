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

Cœur
----

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - domain.title
    - Titre du domaine pour la journalisation et l'affichage.
    - ``Fess``

.. list-table:: Moteur de recherche
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - search_engine.type
    - Type de backend du moteur de recherche. Valeurs valides : default (OpenSearch avec les plugins CodeLibs), vanilla (OpenSearch sans les plugins CodeLibs), aws (vanilla avec un traitement propre à AWS). cloud est un alias obsolète de vanilla.
    - ``default``
  * - search_engine.http.url
    - URL du point de terminaison HTTP du moteur de recherche. Pour les environnements IPv6, utilisez des crochets autour de l'adresse IPv6 (par exemple, http://[::1]:9200)
    - ``http://localhost:9200``
  * - search_engine.http.ssl.certificate_authorities
    - Chemin des autorités de certification SSL pour les connexions HTTP sécurisées.
    - (empty)
  * - search_engine.username
    - Nom d'utilisateur pour l'authentification auprès du moteur de recherche.
    - (empty)
  * - search_engine.password
    - Mot de passe pour l'authentification auprès du moteur de recherche.
    - (empty)
  * - search_engine.heartbeat_interval
    - Intervalle (ms) des vérifications de heartbeat auprès du moteur de recherche.
    - ``10000``
  * - app.cipher.algorithm
    - Algorithme de chiffrement utilisé pour le chiffrement.
    - ``aes``
  * - app.cipher.key
    - Clé secrète pour le chiffrement (modifiez cette valeur en production).
    - ``___change__me___``
  * - app.digest.algorithm
    - Algorithme pour le calcul du digest.
    - ``sha256``
  * - app.password.algorithm
    - Hachage des mots de passe (nouveau mécanisme, compatible Spring Security v5.8) Pris en charge : bcrypt (uniquement, pour l'instant)
    - ``bcrypt``
  * - app.password.bcrypt.cost
    - Coût BCrypt (log rounds). 10 correspond à la valeur par défaut de Spring Security v5.8. Plage : 4-31.
    - ``10``
  * - app.password.upgrade.enabled
    - Re-hachage différé lors d'une connexion réussie pour les hachages hérités.
    - ``true``
  * - app.encrypt.property.pattern
    - REMARQUE : app.digest.algorithm est conservé uniquement pour la vérification des mots de passe HÉRITÉS (hachages antérieurs à la mise à niveau qui n'ont pas de préfixe {id}). Ne pas l'utiliser pour les nouveaux mots de passe. Motif d'expression régulière des propriétés à chiffrer.
    - ``.*password|.*key|.*token|.*secret``
  * - app.log.sensitive.property.pattern
    - Motif d'expression régulière des valeurs sensibles à masquer dans les journaux de débogage (correspondance insensible à la casse avec les clés de propriété/d'environnement).
    - ``.*password.*|.*secret.*|.*key.*|.*token.*|.*credential.*|.*auth.*|.*private.*``
  * - app.extension.names
    - Noms d'extension pour la personnalisation de l'application.
    - (empty)
  * - app.audit.log.format
    - Format du journal d'audit.
    - (empty)
  * - script.audit.log.enabled
    - Paramètres du journal d'audit des scripts.
    - ``true``
  * - script.audit.log.max.length
    - Nombre maximum de caractères du texte de script conservés dans une entrée du journal d'audit des scripts ; un texte plus long est tronqué.
    - ``100``
  * - jvm.crawler.options
    - Options JVM pour le processus du crawler.
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
    - Options JVM (séparées par des sauts de ligne) transmises au processus enfant de création des suggestions.
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
    - Options JVM pour le processus d'indexation des vecteurs de chunks. Budget de heap. Cette JVM enfant n'est démarrée que pendant l'exécution du job "Content Chunk Vector Indexer", donc un -Xmx généreux ne coûte rien lorsque le découpage du contenu en chunks est désactivé. L'ensemble actif est dominé par les lots en cours de traitement, dont chacun conserve, par document, le _source complet, les chaînes de chunks du document et les vecteurs d'embedding du document : content_chunker.job.bulk_size (par défaut 20) x content_chunker.max_chunks_per_document (par défaut 1000) x content_chunker.embedding.dimension (par défaut 768) x 4 octets par float x content_chunker.job.concurrency (par défaut 2) = ~117 MB de vecteurs à eux seuls, avant les chaînes de chunks et les sources des documents. Avec les valeurs par défaut fournies, le pire cas représente environ 190-250 MB en mémoire active (et ~235 MB de vecteurs à eux seuls avec dimension=1536), ce qui ne tient pas dans un heap de 256 MB avec une marge suffisante pour le GC. Augmentez encore -Xmx si vous augmentez bulk_size, max_chunks_per_document, concurrency ou la dimension d'embedding.
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
    - Options JVM pour le processus de vignettes.
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
    - ID des jobs système pour les jobs planifiés.
    - ``default_crawler``
  * - job.template.title.web
    - Modèle de titre de job du crawler Web.
    - ``Web Crawler - {0}``
  * - job.template.title.file
    - Modèle de titre de job du crawler de fichiers.
    - ``File Crawler - {0}``
  * - job.template.title.data
    - Modèle de titre de job du crawler de données.
    - ``Data Crawler - {0}``
  * - job.template.script
    - Modèle de script pour l'exécution du job.
    - ``return container.getComponent("crawlJob").logLevel("info").webConfigIds([{0}]).fileConfigIds([{1}]).dataConfigIds([{2}]).jobExecutor(executor).execute();``
  * - job.max.crawler.processes
    - Nombre maximum de processus de crawler.
    - ``0``
  * - job.default.script
    - Langage de script par défaut pour les jobs.
    - ``javascript``
  * - job.system.property.filter.pattern
    - Motif de filtrage des propriétés système pour les jobs.
    - (empty)
  * - processors
    - Nombre de processeurs à utiliser.
    - ``0``
  * - java.command.path
    - Chemin de la commande Java.
    - ``java``
  * - python.command.path
    - Chemin de la commande Python.
    - ``python``
  * - path.encoding
    - Encodage des chemins de fichiers.
    - ``UTF-8``
  * - use.own.tmp.dir
    - Indique s'il faut utiliser un répertoire temporaire dédié.
    - ``true``
  * - max.log.output.length
    - Longueur maximale de la sortie du journal.
    - ``4000``
  * - adaptive.load.control
    - Valeur du contrôle de charge adaptatif.
    - ``50``
  * - web.load.control
    - Seuil CPU (%) pour le contrôle de charge des requêtes Web. Retourne 429 lorsque le CPU >= cette valeur. (100 : désactivé)
    - ``100``
  * - api.load.control
    - Seuil CPU (%) pour le contrôle de charge des requêtes API. Retourne 429 lorsque le CPU >= cette valeur. (100 : désactivé)
    - ``100``
  * - load.control.monitor.interval
    - Intervalle (secondes) de surveillance de la charge CPU d'OpenSearch.
    - ``1``
  * - supported.languages
    - Langues prises en charge.
    - ``ar,bg,bn,ca,ckb_IQ,cs,da,de,el,en_IE,en,es,et,eu,fa,fi,fr,gl,gu,he,hi,hr,hu,hy,id,it,ja,ko,lt,lv,mk,ml,nl,no,pa,pl,pt_BR,pt,ro,ru,si,sq,sv,ta,te,th,tl,tr,uk,ur,vi,zh_CN,zh_TW,zh``
  * - api.access.token.length
    - Longueur du jeton d'accès de l'API.
    - ``60``
  * - api.access.token.request.parameter
    - Paramètre de requête du jeton d'accès de l'API.
    - (empty)
  * - api.admin.access.permissions
    - Permissions pour l'accès administrateur de l'API.
    - ``Radmin-api``
  * - api.search.accept.referers
    - Referers acceptés pour la recherche de l'API.
    - (empty)
  * - api.search.scroll
    - Indique s'il faut activer le scroll pour la recherche de l'API.
    - ``false``
  * - api.search.export
    - Indique s'il faut activer l'exportation par l'utilisateur final des résultats de recherche (CSV/JSON) sur /api/v2/documents/export.
    - ``false``
  * - api.search.export.max.size
    - Nombre maximum de documents écrits par une exportation de résultats de recherche.
    - ``1000``
  * - api.search.export.fields
    - Champs écrits par l'exportation des résultats de recherche (séparés par des virgules). Un champ qui n'est pas un champ de réponse de l'API est ignoré.
    - ``title,url_link,last_modified,content_length,filetype``
  * - api.search.export.rate.limit.per.minute
    - Nombre maximum d'exportations de résultats de recherche par minute pour chaque utilisateur (chaque IP cliente pour un invité). 0 ou moins désactive la limite.
    - ``10``
  * - api.json.response.headers
    - En-têtes de la réponse JSON de l'API. Access-Control-\* et Timing-Allow-Origin sont ignorés ici (CORS est contrôlé par api.cors.\* / CorsFilter). Ne définissez pas Vary.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.json.response.exception.included
    - Indique s'il faut inclure les exceptions dans la réponse JSON de l'API.
    - ``false``
  * - api.gsa.response.headers
    - En-têtes de la réponse GSA de l'API. Access-Control-\* et Timing-Allow-Origin sont ignorés ici (CORS est contrôlé par api.cors.\* / CorsFilter). Ne définissez pas Vary.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.gsa.response.exception.included
    - Indique s'il faut inclure les exceptions dans la réponse GSA de l'API.
    - ``false``
  * - api.dashboard.response.headers
    - En-têtes de la réponse du tableau de bord de l'API. Access-Control-\* et Timing-Allow-Origin sont ignorés ici (CORS est contrôlé par api.cors.\* / CorsFilter). Ne définissez pas Vary.
    - ``Referrer-Policy:strict-origin-when-cross-origin``
  * - api.cors.allow.origin
    - Origines autorisées pour CORS. "\*" retourne un "\*" littéral (l'Origin de la requête n'est PAS reflétée) et désactive les identifiants. Définissez des origines explicites (séparées par des sauts de ligne ou des virgules) pour autoriser l'accès cross-origin avec identifiants.
    - ``*``
  * - api.cors.allow.methods
    - Méthodes HTTP autorisées pour CORS.
    - ``GET, POST, OPTIONS, DELETE, PUT``
  * - api.cors.max.age
    - Âge maximal des requêtes preflight CORS.
    - ``3600``
  * - api.cors.allow.headers
    - En-têtes de requête autorisés pour le preflight CORS. Une liste statique est retournée (Access-Control-Request-Headers n'est pas reflété). Inclut X-Fess-CSRF-Token pour les SPA cross-origin qui envoient le jeton CSRF.
    - ``Origin, Content-Type, Accept, Authorization, X-Requested-With, X-Fess-CSRF-Token``
  * - api.cors.allow.credentials
    - Indique s'il faut autoriser les identifiants pour CORS. Pris en compte uniquement pour une correspondance exacte avec une Origin explicite ; ignoré lorsque api.cors.allow.origin vaut "\*".
    - ``true``
  * - api.jsonp.enabled
    - Indique s'il faut activer JSONP pour l'API.
    - ``false``
  * - api.ping.search_engine.fields
    - Champs pour le ping de l'API vers le moteur de recherche.
    - ``status,timed_out``

Limitation de débit
-------------------

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rate.limit.enabled
    - Indique si la limitation de débit est activée.
    - ``false``
  * - rate.limit.requests.per.window
    - Nombre maximum de requêtes autorisées par fenêtre.
    - ``100``
  * - rate.limit.window.ms
    - Taille de la fenêtre en millisecondes.
    - ``60000``
  * - rate.limit.block.duration.ms
    - Durée en millisecondes de blocage de l'IP lorsque la limite est dépassée.
    - ``300000``
  * - rate.limit.retry.after.seconds
    - Valeur de l'en-tête Retry-After en secondes.
    - ``60``
  * - rate.limit.whitelist.ips
    - Liste séparée par des virgules des IP figurant dans la liste d'autorisation (par exemple, 127.0.0.1,::1).
    - ``127.0.0.1,::1``
  * - rate.limit.blocked.ips
    - Liste séparée par des virgules des IP bloquées.
    - (empty)
  * - rate.limit.trusted.proxies
    - Liste séparée par des virgules des IP de proxy de confiance. Ne faire confiance à X-Forwarded-For/X-Real-IP que s'ils proviennent de ces IP.
    - ``127.0.0.1,::1``
  * - rate.limit.cleanup.interval
    - Nombre de requêtes entre les opérations de nettoyage pour éviter les fuites de mémoire.
    - ``1000``
  * - virtual.host.headers
    - Hôte virtuel : Host:fess.codelibs.org=fess
    - (empty)
  * - http.proxy.host
    - Nom d'hôte du serveur proxy HTTP.
    - (empty)
  * - http.proxy.port
    - Numéro de port du serveur proxy HTTP (par exemple, 8080).
    - ``8080``
  * - http.proxy.username
    - Nom d'utilisateur pour l'authentification auprès du proxy HTTP.
    - (empty)
  * - http.proxy.password
    - Mot de passe pour l'authentification auprès du proxy HTTP.
    - (empty)
  * - http.fileupload.max.size
    - Taille maximale (octets) des téléversements de fichiers HTTP.
    - ``262144000``
  * - http.fileupload.threshold.size
    - Taille seuil (octets) pour la mise en tampon des téléversements de fichiers HTTP.
    - ``262144``
  * - http.fileupload.max.file.count
    - Nombre maximum de fichiers autorisés par téléversement HTTP.
    - ``10``

Index
-----

.. list-table:: Crawler commun
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.http.thread_pool.size
    - Nombre de threads pour le crawl HTTP.
    - ``0``
  * - crawler.data.serializer
    - Type de sérialiseur pour les données du crawler (par exemple, kryo).
    - ``kryo``
  * - crawler.document.max.site.length
    - Longueur maximale du nom de site dans les documents.
    - ``100``
  * - crawler.document.site.encoding
    - Encodage des noms de site dans les documents.
    - ``UTF-8``
  * - crawler.document.unknown.hostname
    - Nom d'hôte à utiliser lorsqu'il est inconnu dans les documents.
    - ``unknown``
  * - crawler.document.use.site.encoding.on.english
    - Indique s'il faut utiliser l'encodage du site pour les documents en anglais.
    - ``false``
  * - crawler.document.append.data
    - Indique s'il faut ajouter des données aux documents.
    - ``true``
  * - crawler.document.append.filename
    - Indique s'il faut ajouter le nom de fichier aux documents.
    - ``false``
  * - crawler.document.max.alphanum.term.size
    - Taille maximale des mots alphanumériques dans les documents.
    - ``20``
  * - crawler.document.max.symbol.term.size
    - Taille maximale des mots symboles dans les documents.
    - ``10``
  * - crawler.document.duplicate.term.removed
    - Indique s'il faut supprimer les mots en double dans les documents.
    - ``false``
  * - crawler.document.space.chars
    - Caractères d'espace Unicode pour l'analyse des documents.
    - ``u0009u000Au000Bu000Cu000Du001Cu001Du001Eu001Fu0020u00A0u1680u180Eu2000u2001u2002u2003u2004u2005u2006u2007u2008u2009u200Au200Bu200Cu202Fu205Fu3000uFEFFuFFFDu00B6``
  * - crawler.document.fullstop.chars
    - Caractères de point final Unicode pour l'analyse des documents.
    - ``u002eu06d4u2e3cu3002``
  * - crawler.crawling.data.encoding
    - Encodage des données de crawl.
    - ``UTF-8``
  * - crawler.web.protocols
    - Protocoles Web pris en charge pour le crawl.
    - ``http,https``
  * - crawler.file.protocols
    - Protocoles de fichiers pris en charge pour le crawl.
    - ``file,smb,smb1,ftp``
  * - crawler.data.env.param.key.pattern
    - Motif des clés de variables d'environnement dans les données de crawl.
    - ``^FESS_ENV_.*``
  * - crawler.ignore.robots.txt
    - Indique s'il faut ignorer robots.txt pendant le crawl.
    - ``false``
  * - crawler.ignore.robots.tags
    - Indique s'il faut ignorer les balises meta robots pendant le crawl.
    - ``false``
  * - crawler.ignore.content.exception
    - Indique s'il faut ignorer les exceptions de contenu pendant le crawl.
    - ``true``
  * - crawler.failure.url.status.codes
    - Codes d'état HTTP considérés comme des URL en échec.
    - ``404,403,410``
  * - crawler.system.monitor.interval
    - Intervalle (secondes) du moniteur système pendant le crawl.
    - ``60``
  * - crawler.hotthread.ignore_idle_threads
    - Indique s'il faut ignorer les threads inactifs dans la surveillance des hot threads.
    - ``true``
  * - crawler.hotthread.interval
    - Intervalle de la surveillance des hot threads (par exemple, 500ms).
    - ``500ms``
  * - crawler.hotthread.snapshots
    - Nombre de snapshots pour la surveillance des hot threads.
    - ``10``
  * - crawler.hotthread.threads
    - Nombre de threads pour la surveillance des hot threads.
    - ``3``
  * - crawler.hotthread.timeout
    - Délai d'expiration de la surveillance des hot threads (par exemple, 30s).
    - ``30s``
  * - crawler.hotthread.type
    - Type de surveillance des hot threads (par exemple, cpu).
    - ``cpu``
  * - crawler.metadata.content.excludes
    - Champs de métadonnées à exclure du contenu du document.
    - ``resourceName,X-Parsed-By,Content-Encoding.*,Content-Type.*,X-TIKA.*,X-FESS.*``
  * - crawler.metadata.name.mapping
    - Mappage des noms de métadonnées du document.
    - | ``title=title:string``
      | ``Title=title:string``
      | ``dc:title=title:string``
      | ``frontmatter.title=title:string``

.. list-table:: Crawler HTML
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.html.content.xpath
    - XPath pour extraire le contenu principal des documents HTML.
    - ``//BODY``
  * - crawler.document.html.lang.xpath
    - XPath pour extraire l'attribut de langue des documents HTML.
    - ``//HTML/@lang``
  * - crawler.document.html.digest.xpath
    - XPath pour extraire le digest (description) des documents HTML.
    - ``//META[@name='description']/@content``
  * - crawler.document.html.canonical.xpath
    - XPath pour extraire l'URL canonique des documents HTML.
    - ``//LINK[@rel='canonical'][1]/@href``
  * - crawler.document.html.pruned.tags
    - Balises HTML à élaguer (supprimer) pendant le traitement des documents.
    - ``noscript,script,style,header,footer,aside,nav,a[rel=nofollow]``
  * - crawler.document.html.max.digest.length
    - Longueur maximale du digest extrait des documents HTML.
    - ``120``
  * - crawler.document.html.default.lang
    - Langue par défaut des documents HTML.
    - (empty)
  * - crawler.document.html.default.include.index.patterns
    - Motifs à inclure pour le traitement d'indexation HTML.
    - (empty)
  * - crawler.document.html.default.exclude.index.patterns
    - Motifs à exclure pour le traitement d'indexation HTML.
    - ``(?i).*(css|js|jpeg|jpg|gif|png|bmp|wmv|xml|ico|exe)``
  * - crawler.document.html.default.include.search.patterns
    - Motifs à inclure pour le traitement de recherche HTML.
    - (empty)
  * - crawler.document.html.default.exclude.search.patterns
    - Motifs à exclure pour le traitement de recherche HTML.
    - (empty)

.. list-table:: Crawler de fichiers
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.file.name.encoding
    - Encodage des noms de fichiers dans les documents.
    - (empty)
  * - crawler.document.file.no.title.label
    - Libellé à utiliser lorsqu'un fichier n'a pas de titre.
    - ``No title.``
  * - crawler.document.file.ignore.empty.content
    - Indique s'il faut ignorer les fichiers dont le contenu est vide.
    - ``false``
  * - crawler.document.file.max.title.length
    - Longueur maximale du titre de fichier dans les documents.
    - ``100``
  * - crawler.document.file.max.digest.length
    - Longueur maximale du digest de fichier dans les documents.
    - ``200``
  * - crawler.document.file.append.meta.content
    - Indique s'il faut ajouter le contenu des métadonnées des fichiers.
    - ``true``
  * - crawler.document.file.append.body.content
    - Indique s'il faut ajouter le contenu du corps des fichiers.
    - ``true``
  * - crawler.document.file.default.lang
    - Langue par défaut des documents de fichiers.
    - (empty)
  * - crawler.document.file.default.include.index.patterns
    - Motifs à inclure pour le traitement d'indexation des fichiers.
    - (empty)
  * - crawler.document.file.default.exclude.index.patterns
    - Motifs à exclure pour le traitement d'indexation des fichiers.
    - (empty)
  * - crawler.document.file.default.include.search.patterns
    - Motifs à inclure pour le traitement de recherche des fichiers.
    - (empty)
  * - crawler.document.file.default.exclude.search.patterns
    - Motifs à exclure pour le traitement de recherche des fichiers.
    - (empty)
  * - crawler.document.file.owner.enabled
    - Indique s'il faut indexer le propriétaire des fichiers crawlés (SMB, système de fichiers local et FTP). Le paramètre de configuration de crawl config.owner.enabled prévaut sur cette valeur.
    - ``true``
  * - crawler.document.file.last.modifier.enabled
    - Indique s'il faut indexer le dernier modificateur des fichiers crawlés, lu dans les métadonnées du document avec repli sur le propriétaire du fichier. Le paramètre de configuration de crawl config.last.modifier.enabled prévaut sur cette valeur.
    - ``true``

.. list-table:: Cache du crawler
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - crawler.document.cache.enabled
    - Indique si le cache de documents est activé.
    - ``true``
  * - crawler.document.cache.max.size
    - Taille maximale (octets) du cache de documents.
    - ``2621440``
  * - crawler.document.cache.supported.mimetypes
    - Types MIME pris en charge pour le cache de documents.
    - ``text/html``
  * - crawler.document.cache.html.mimetypes
    - ,text/plain,application/xml,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-powerpoint,application/vnd.openxmlformats-officedocument.presentationml.presentation Types MIME pour le cache de documents HTML.
    - ``text/html``
  * - crawler.document.mimetype.extension.overrides
    - Mappages de remplacement extension vers type MIME pour la détection du type MIME (un par ligne : .ext=mime/type).
    - (empty)
  * - crawler.document.ocr.enabled
    - Indique s'il faut extraire le texte des images et des PDF numérisés avec Tesseract OCR (nécessite la commande tesseract).
    - ``false``
  * - crawler.document.ocr.language
    - Langues de Tesseract OCR, jointes par '+' (par exemple jpn+eng).
    - ``eng``
  * - crawler.document.ocr.timeout
    - Délai d'expiration en secondes pour une exécution de Tesseract OCR.
    - ``120``

.. list-table:: Indexeur
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - indexer.thread.dump.enabled
    - Indique s'il faut activer le vidage de threads pour l'indexeur.
    - ``true``
  * - indexer.unprocessed.document.size
    - Nombre maximum de documents non traités pour l'indexeur.
    - ``1000``
  * - indexer.click.count.enabled
    - Indique s'il faut activer le suivi du nombre de clics dans l'indexeur.
    - ``true``
  * - indexer.favorite.count.enabled
    - Indique s'il faut activer le suivi du nombre de favoris dans l'indexeur.
    - ``true``
  * - indexer.webfs.commit.margin.time
    - Marge de temps de commit (ms) pour webfs dans l'indexeur.
    - ``5000``
  * - indexer.webfs.max.empty.list.count
    - Nombre maximum de listes vides pour webfs dans l'indexeur.
    - ``3600``
  * - indexer.webfs.update.interval
    - Intervalle de mise à jour (ms) pour webfs dans l'indexeur.
    - ``10000``
  * - indexer.webfs.max.document.cache.size
    - Taille maximale du cache de documents pour webfs dans l'indexeur.
    - ``10``
  * - indexer.webfs.max.document.request.size
    - Taille maximale des requêtes de documents (octets) pour webfs dans l'indexeur.
    - ``1048576``
  * - indexer.data.max.document.cache.size
    - Taille maximale du cache de documents pour data dans l'indexeur.
    - ``10000``
  * - indexer.data.max.document.request.size
    - Taille maximale des requêtes de documents (octets) pour data dans l'indexeur.
    - ``1048576``
  * - indexer.data.max.delete.cache.size
    - Taille maximale du cache de suppression pour data dans l'indexeur.
    - ``100``
  * - indexer.data.max.redirect.count
    - Nombre maximum de redirections pour data dans l'indexeur.
    - ``10``
  * - indexer.language.fields
    - Champs utilisés pour la détection de langue dans l'indexeur.
    - ``content,important_content,title``
  * - indexer.language.detect.length
    - Longueur du texte pour la détection de langue dans l'indexeur.
    - ``1000``
  * - indexer.max.result.window.size
    - Taille maximale de la fenêtre de résultats pour l'indexeur.
    - ``10000``
  * - indexer.max.search.doc.size
    - Nombre maximum de documents de recherche pour l'indexeur.
    - ``50000``

.. list-table:: Paramètres de l'index
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.codec
    - Type de codec pour l'index.
    - ``default``
  * - index.number_of_shards
    - Nombre de shards primaires pour l'index.
    - ``5``
  * - index.auto_expand_replicas
    - Paramètre d'expansion automatique des répliques pour l'index.
    - ``0-1``
  * - index.id.digest.algorithm
    - Algorithme de digest pour les ID d'index.
    - ``SHA-512``
  * - index.user.initial_password
    - Mot de passe initial de l'utilisateur de l'index.
    - ``admin``

.. list-table:: Noms de champs
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.field.favorite_count
    - Nom du champ pour le nombre de favoris dans l'index.
    - ``favorite_count``
  * - index.field.click_count
    - Nom du champ pour le nombre de clics dans l'index.
    - ``click_count``
  * - index.field.config_id
    - Nom du champ pour l'ID de configuration dans l'index.
    - ``config_id``
  * - index.field.expires
    - Nom du champ pour la date d'expiration dans l'index.
    - ``expires``
  * - index.field.url
    - Nom du champ pour l'URL dans l'index.
    - ``url``
  * - index.field.doc_id
    - Nom du champ pour l'ID de document dans l'index.
    - ``doc_id``
  * - index.field.id
    - Nom du champ pour l'ID interne dans l'index.
    - ``_id``
  * - index.field.version
    - Nom du champ pour la version dans l'index.
    - ``_version``
  * - index.field.seq_no
    - Nom du champ pour le numéro de séquence dans l'index.
    - ``_seq_no``
  * - index.field.primary_term
    - Nom du champ pour le terme primaire dans l'index.
    - ``_primary_term``
  * - index.field.lang
    - Nom du champ pour la langue dans l'index.
    - ``lang``
  * - index.field.has_cache
    - Nom du champ pour le statut du cache dans l'index.
    - ``has_cache``
  * - index.field.last_modified
    - Nom du champ pour la date de dernière modification dans l'index.
    - ``last_modified``
  * - index.field.etag
    - Nom du champ pour l'en-tête de réponse ETag du document crawlé dans l'index.
    - ``etag``
  * - index.field.owner
    - Nom du champ pour le propriétaire du fichier crawlé dans l'index.
    - ``owner``
  * - index.field.last_modifier
    - Nom du champ pour le dernier modificateur du fichier crawlé dans l'index.
    - ``last_modifier``
  * - index.field.anchor
    - Nom du champ pour l'ancre dans l'index.
    - ``anchor``
  * - index.field.segment
    - Nom du champ pour le segment dans l'index.
    - ``segment``
  * - index.field.role
    - Nom du champ pour le rôle dans l'index.
    - ``role``
  * - index.field.boost
    - Nom du champ pour la valeur de boost dans l'index.
    - ``boost``
  * - index.field.created
    - Nom du champ pour la date de création dans l'index.
    - ``created``
  * - index.field.timestamp
    - Nom du champ pour l'horodatage dans l'index.
    - ``timestamp``
  * - index.field.label
    - Nom du champ pour l'étiquette dans l'index.
    - ``label``
  * - index.field.tag
    - Nom du champ pour les tags utilisateur du document dans l'index.
    - ``tag``
  * - index.field.mimetype
    - Nom du champ pour le type MIME dans l'index.
    - ``mimetype``
  * - index.field.parent_id
    - Nom du champ pour l'ID parent dans l'index.
    - ``parent_id``
  * - index.field.important_content
    - Nom du champ pour le contenu important dans l'index.
    - ``important_content``
  * - index.field.content
    - Nom du champ pour le contenu dans l'index.
    - ``content``
  * - index.field.content_minhash_bits
    - Nom du champ pour les bits minhash du contenu dans l'index.
    - ``content_minhash_bits``
  * - index.field.cache
    - Nom du champ pour le cache dans l'index.
    - ``cache``
  * - index.field.digest
    - Nom du champ pour le digest dans l'index.
    - ``digest``
  * - index.field.title
    - Nom du champ pour le titre dans l'index.
    - ``title``
  * - index.field.host
    - Nom du champ pour l'hôte dans l'index.
    - ``host``
  * - index.field.site
    - Nom du champ pour le site dans l'index.
    - ``site``
  * - index.field.content_length
    - Nom du champ pour la longueur du contenu dans l'index.
    - ``content_length``
  * - index.field.filetype
    - Nom du champ pour le type de fichier dans l'index.
    - ``filetype``
  * - index.field.filename
    - Nom du champ pour le nom de fichier dans l'index.
    - ``filename``
  * - index.field.thumbnail
    - Nom du champ pour la vignette dans l'index.
    - ``thumbnail``
  * - index.field.virtual_host
    - Nom du champ pour l'hôte virtuel dans l'index.
    - ``virtual_host``
  * - response.field.content_title
    - Nom du champ pour le titre du contenu dans la réponse.
    - ``content_title``
  * - response.field.content_description
    - Nom du champ pour la description du contenu dans la réponse.
    - ``content_description``
  * - response.field.url_link
    - Nom du champ pour le lien URL dans la réponse.
    - ``url_link``
  * - response.field.site_path
    - Nom du champ pour le chemin du site dans la réponse.
    - ``site_path``
  * - response.max.title.length
    - Longueur maximale du titre du contenu dans la réponse.
    - ``50``
  * - response.max.site.path.length
    - Longueur maximale du chemin du site dans la réponse.
    - ``100``
  * - response.highlight.content_title.enabled
    - Indique s'il faut activer le surlignage du titre du contenu dans la réponse.
    - ``true``
  * - response.inline.mimetypes
    - Types MIME inline pour la réponse.
    - ``application/pdf,text/plain``
  * - response.headers
    - En-têtes HTTP de la réponse. Access-Control-\* et Timing-Allow-Origin sont ignorés (CORS est contrôlé par api.cors.\* / CorsFilter). Ne définissez pas Vary ici.
    - | ``text/html=X-XSS-Protection: 1; mode=block``
      | ``text/html=X-Frame-Options: SAMEORIGIN``

.. list-table:: Index des documents
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.document.search.index
    - Nom de l'index pour les documents de recherche.
    - ``fess.search``
  * - index.document.update.index
    - Nom de l'index pour les documents de mise à jour.
    - ``fess.update``
  * - index.document.suggest.index
    - Nom de l'index pour les documents de suggestion.
    - ``fess``
  * - index.document.crawler.index
    - Nom de l'index pour les documents du crawler.
    - ``fess_crawler``
  * - index.document.crawler.queue.number_of_shards
    - Nombre de shards primaires pour l'index de file d'attente du crawler.
    - ``10``
  * - index.document.crawler.data.number_of_shards
    - Nombre de shards primaires pour l'index de données du crawler.
    - ``10``
  * - index.document.crawler.filter.number_of_shards
    - Nombre de shards primaires pour l'index de filtres du crawler.
    - ``10``
  * - index.document.crawler.queue.number_of_replicas
    - Nombre de répliques pour l'index de file d'attente du crawler.
    - ``1``
  * - index.document.crawler.data.number_of_replicas
    - Nombre de répliques pour l'index de données du crawler.
    - ``1``
  * - index.document.crawler.filter.number_of_replicas
    - Nombre de répliques pour l'index de filtres du crawler.
    - ``1``
  * - index.config.index
    - Nom de l'index pour les données de configuration.
    - ``fess_config``
  * - index.user.index
    - Nom de l'index pour les données utilisateur.
    - ``fess_user``
  * - index.log.index
    - Nom de l'index pour les données de journal.
    - ``fess_log``
  * - index.dictionary.prefix
    - Préfixe des noms d'index de dictionnaire.
    - (empty)

.. list-table:: Gestion des documents
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.admin.array.fields
    - Champs de type tableau pour l'administration dans l'index.
    - ``lang,role,label,anchor,virtual_host``
  * - index.admin.date.fields
    - Champs de type date pour l'administration dans l'index.
    - ``expires,created,timestamp,last_modified``
  * - index.admin.integer.fields
    - Champs de type entier pour l'administration dans l'index.
    - (empty)
  * - index.admin.long.fields
    - Champs de type long pour l'administration dans l'index.
    - ``content_length,favorite_count,click_count``
  * - index.admin.float.fields
    - Champs de type float pour l'administration dans l'index.
    - ``boost``
  * - index.admin.double.fields
    - Champs de type double pour l'administration dans l'index.
    - (empty)
  * - index.admin.required.fields
    - Champs obligatoires pour l'administration dans l'index.
    - ``url,title,role,boost``

.. list-table:: Délais d'expiration
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.search.timeout
    - Délai d'expiration des opérations de recherche dans l'index.
    - ``3m``
  * - index.scroll.search.timeout
    - Délai d'expiration des opérations de recherche scroll.
    - ``3m``
  * - index.index.timeout
    - Délai d'expiration des opérations sur l'index.
    - ``3m``
  * - index.bulk.timeout
    - Délai d'expiration des opérations d'indexation en bloc.
    - ``3m``
  * - index.delete.timeout
    - Délai d'expiration des opérations de suppression dans l'index.
    - ``3m``
  * - index.health.timeout
    - Délai d'expiration des contrôles de santé de l'index.
    - ``10m``
  * - index.indices.timeout
    - Délai d'expiration des opérations sur les indices de l'index.
    - ``1m``

.. list-table:: Types de fichiers
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.filetype
    - Mappage des types MIME vers les libellés de filetype pour l'indexation.
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
    - Nombre de documents à traiter par opération de réindexation.
    - ``100``
  * - index.reindex.body
    - Modèle de corps de requête pour les opérations de réindexation.
    - ``{"source":{"index":"__SOURCE_INDEX__","size":__SIZE__},"dest":{"index":"__DEST_INDEX__"},"script":{"source":"__SCRIPT_SOURCE__"}}``
  * - index.reindex.requests_per_second
    - Requêtes par seconde pour les opérations de réindexation ("adaptive" pour automatique).
    - ``adaptive``
  * - index.reindex.refresh
    - Indique s'il faut actualiser l'index après la réindexation.
    - ``false``
  * - index.reindex.timeout
    - Délai d'expiration des opérations de réindexation.
    - ``1m``
  * - index.reindex.scroll
    - Délai d'expiration du scroll pour les opérations de réindexation.
    - ``5m``
  * - index.reindex.max_docs
    - Nombre maximum de documents pour les opérations de réindexation.
    - (empty)

.. list-table:: Requête
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.max.length
    - Longueur maximale des requêtes de recherche.
    - ``1000``
  * - query.timeout
    - Délai d'expiration (ms) des requêtes de recherche.
    - ``10000``
  * - query.timeout.logging
    - Indique s'il faut consigner les recherches dont les résultats sont incomplets parce que la requête a expiré ou qu'un shard a échoué.
    - ``true``
  * - query.track.total.hits
    - Nombre maximum de hits totaux à suivre dans les requêtes. Seuls un nombre positif ou true sont pris en charge : false laisse la réponse sans nombre de hits, et une recherche qui le demande, ici ou comme paramètre de recherche, est refusée.
    - ``10000``
  * - query.geo.fields
    - Champs utilisés pour les requêtes de recherche géographique.
    - ``location``
  * - query.browser.lang.parameter.name
    - Nom du paramètre pour la langue du navigateur dans les requêtes.
    - ``browser_lang``
  * - query.replace.term.with.prefix.query
    - Indique s'il faut remplacer un terme par une requête de préfixe.
    - ``true``
  * - query.orsearch.min.hit.count
    - Nombre minimum de hits pour les requêtes de recherche OR.
    - ``-1``
  * - query.highlight.terminal.chars
    - Caractères terminaux Unicode pour le surlignage des requêtes.
    - ``u0021u002Cu002Eu003Fu0589u061Fu06D4u0700u0701u0702u0964u104Au104Bu1362u1367u1368u166Eu1803u1809u203Cu203Du2047u2048u2049u3002uFE52uFE57uFF01uFF0EuFF1FuFF61``
  * - query.highlight.fragment.size
    - Taille des fragments pour le surlignage des requêtes.
    - ``60``
  * - query.highlight.number.of.fragments
    - Nombre de fragments pour le surlignage des requêtes.
    - ``2``
  * - query.highlight.type
    - Type de surlignage des requêtes.
    - ``fvh``
  * - query.highlight.tag.pre
    - Balise à utiliser avant le texte surligné.
    - ``<strong>``
  * - query.highlight.tag.post
    - Balise à utiliser après le texte surligné.
    - ``</strong>``
  * - query.highlight.boundary.chars
    - Caractères de délimitation pour le surlignage des requêtes.
    - ``u0009u000Au0013u0020``
  * - query.highlight.boundary.max.scan
    - Balayage maximal pour les limites de surlignage des requêtes.
    - ``20``
  * - query.highlight.boundary.scanner
    - Type de scanner pour les limites de surlignage des requêtes.
    - ``chars``
  * - query.highlight.encoder
    - Type d'encodeur pour le surlignage des requêtes.
    - ``default``
  * - query.highlight.force.source
    - Indique s'il faut forcer la source pour le surlignage des requêtes.
    - ``false``
  * - query.highlight.fragmenter
    - Type de fragmenteur pour le surlignage des requêtes.
    - ``span``
  * - query.highlight.fragment.offset
    - Décalage des fragments de surlignage des requêtes.
    - ``-1``
  * - query.highlight.no.match.size
    - Taille du surlignage de requête sans correspondance.
    - ``0``
  * - query.highlight.order
    - Ordre des fragments de surlignage des requêtes.
    - ``score``
  * - query.highlight.phrase.limit
    - Limite de phrases pour le surlignage des requêtes.
    - ``256``
  * - query.highlight.content.description.fields
    - Champs pour la description du contenu dans le surlignage des requêtes.
    - ``hl_content,digest``
  * - query.highlight.boundary.position.detect
    - Indique s'il faut détecter la position de limite dans le surlignage des requêtes.
    - ``true``
  * - query.highlight.text.fragment.type
    - Type de fragment de texte dans le surlignage des requêtes.
    - ``query``
  * - query.highlight.text.fragment.size
    - Taille du fragment de texte dans le surlignage des requêtes.
    - ``3``
  * - query.highlight.text.fragment.prefix.length
    - Longueur du préfixe du fragment de texte dans le surlignage des requêtes.
    - ``5``
  * - query.highlight.text.fragment.suffix.length
    - Longueur du suffixe du fragment de texte dans le surlignage des requêtes.
    - ``5``
  * - query.max.search.result.offset
    - Décalage maximal des résultats de recherche pour les requêtes.
    - ``100000``
  * - query.additional.default.fields
    - Champs par défaut supplémentaires pour les requêtes.
    - (empty)
  * - query.additional.response.fields
    - Champs supplémentaires récupérés depuis l'index pour les résultats de recherche. L'API de recherche ne retourne un champ ajouté ici que s'il figure aussi dans query.additional.api.response.fields.
    - (empty)
  * - query.additional.api.response.fields
    - Champs de réponse API supplémentaires pour les requêtes. Cette clé ne fait qu'ajouter des champs à la liste d'autorisation de la réponse de l'API v2 (ajout uniquement) ; elle ne les récupère pas. Un champ doit aussi être récupéré : ajoutez-le à query.additional.response.fields pour l'API de recherche, ou à query.additional.scroll.response.fields pour l'API scroll. N'ajoutez pas de champs ACL ou internes (par exemple role, virtual_host) ; les ajouter exposerait des informations de contrôle d'accès dans la réponse de l'API de recherche.
    - (empty)
  * - query.additional.scroll.response.fields
    - Champs supplémentaires récupérés depuis l'index pour les résultats de recherche scroll. L'API scroll ne retourne un champ ajouté ici que s'il figure aussi dans query.additional.api.response.fields.
    - (empty)
  * - query.additional.cache.response.fields
    - Champs de réponse de cache supplémentaires pour les requêtes.
    - (empty)
  * - query.additional.highlighted.fields
    - Champs surlignés supplémentaires pour les requêtes.
    - (empty)
  * - query.additional.search.fields
    - Champs de recherche supplémentaires pour les requêtes.
    - (empty)
  * - query.additional.facet.fields
    - Champs de facette supplémentaires pour les requêtes.
    - (empty)
  * - query.additional.sort.fields
    - Champs de tri supplémentaires pour les requêtes.
    - (empty)
  * - query.additional.analyzed.fields
    - Champs analysés supplémentaires pour les requêtes.
    - (empty)
  * - query.additional.not.analyzed.fields
    - Champs non analysés supplémentaires pour les requêtes.
    - (empty)
  * - query.gsa.response.fields
    - Champs pour la réponse GSA dans les requêtes.
    - ``UE,U,T,RK,S,LANG``
  * - query.gsa.default.lang
    - Langue par défaut pour les requêtes GSA.
    - ``en``
  * - query.gsa.default.sort
    - Tri par défaut pour les requêtes GSA.
    - (empty)
  * - query.gsa.meta.prefix
    - Préfixe meta pour les requêtes GSA.
    - ``MT_``
  * - query.gsa.index.field.charset
    - Champ de jeu de caractères pour les requêtes d'index GSA.
    - ``charset``
  * - query.gsa.index.field.content_type.
    - Champ de type de contenu pour les requêtes d'index GSA.
    - ``content_type``
  * - query.collapse.max.concurrent.group.results
    - Nombre maximum de résultats de groupe simultanés pour les requêtes collapse.
    - ``4``
  * - query.collapse.inner.hits.name
    - Nom des inner hits pour les requêtes collapse.
    - ``similar_docs``
  * - query.collapse.inner.hits.size
    - Taille des inner hits pour les requêtes collapse.
    - ``0``
  * - query.collapse.inner.hits.sorts
    - Tris des inner hits dans les requêtes collapse.
    - (empty)
  * - query.default.languages
    - Langues par défaut pour les requêtes.
    - (empty)
  * - query.json.default.preference
    - Préférence par défaut pour les requêtes JSON.
    - ``_query``
  * - query.gsa.default.preference
    - Préférence par défaut pour les requêtes GSA.
    - ``_query``
  * - query.language.mapping
    - Mappage des langues pour les requêtes.
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
    - Valeur de boost du champ de titre dans les requêtes.
    - ``0.5``
  * - query.boost.title.lang
    - Valeur de boost du champ de titre avec langue dans les requêtes.
    - ``1.0``
  * - query.boost.content
    - Valeur de boost du champ de contenu dans les requêtes.
    - ``0.05``
  * - query.boost.content.lang
    - Valeur de boost du champ de contenu avec langue dans les requêtes.
    - ``0.1``
  * - query.boost.important_content
    - Valeur de boost du champ de contenu important dans les requêtes.
    - ``-1.0``
  * - query.boost.important_content.lang
    - Valeur de boost du champ de contenu important avec langue dans les requêtes.
    - ``-1.0``
  * - query.boost.fuzzy.min.length
    - Longueur minimale pour le boost flou dans les requêtes.
    - ``4``
  * - query.boost.fuzzy.title
    - Valeur de boost pour les requêtes floues sur le titre.
    - ``0.01``
  * - query.boost.fuzzy.title.fuzziness
    - Fuzziness pour les requêtes floues sur le titre.
    - ``AUTO``
  * - query.boost.fuzzy.title.expansions
    - Nombre d'expansions pour les requêtes floues sur le titre.
    - ``10``
  * - query.boost.fuzzy.title.prefix_length
    - Longueur du préfixe pour les requêtes floues sur le titre.
    - ``0``
  * - query.boost.fuzzy.title.transpositions
    - Indique s'il faut autoriser les transpositions dans les requêtes floues sur le titre.
    - ``true``
  * - query.boost.fuzzy.content
    - Valeur de boost pour les requêtes floues sur le contenu.
    - ``0.005``
  * - query.boost.fuzzy.content.fuzziness
    - Fuzziness pour les requêtes floues sur le contenu.
    - ``AUTO``
  * - query.boost.fuzzy.content.expansions
    - Nombre d'expansions pour les requêtes floues sur le contenu.
    - ``10``
  * - query.boost.fuzzy.content.prefix_length
    - Longueur du préfixe pour les requêtes floues sur le contenu.
    - ``0``
  * - query.boost.fuzzy.content.transpositions
    - Indique s'il faut autoriser les transpositions dans les requêtes floues sur le contenu.
    - ``true``
  * - query.default.query_type
    - Type de requête par défaut.
    - ``bool``
  * - query.dismax.tie_breaker
    - Valeur de tie breaker pour les requêtes dismax.
    - ``0.1``
  * - query.bool.minimum_should_match
    - Valeur de minimum should match pour les requêtes booléennes.
    - (empty)
  * - query.prefix.expansions
    - Nombre d'expansions pour les requêtes de préfixe.
    - ``50``
  * - query.prefix.slop
    - Valeur de slop pour les requêtes de préfixe.
    - ``0``
  * - query.fuzzy.prefix_length
    - Longueur du préfixe pour les requêtes floues.
    - ``0``
  * - query.fuzzy.expansions
    - Nombre d'expansions pour les requêtes floues.
    - ``50``
  * - query.fuzzy.transpositions
    - Indique s'il faut autoriser les transpositions dans les requêtes floues.
    - ``true``

.. list-table:: Facette
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - query.facet.fields
    - Champs pour les requêtes de facette.
    - ``label``
  * - query.facet.fields.size
    - Taille des champs de facette.
    - ``100``
  * - query.facet.fields.size.max
    - Borne supérieure de facet.size (appliquée au point de passage obligé de la recherche).
    - ``1000``
  * - query.facet.fields.min_doc_count
    - Nombre minimum de documents pour les champs de facette.
    - ``1``
  * - query.facet.fields.min_doc_count.max
    - Borne supérieure de facet.minDocCount (appliquée au point de passage obligé de la recherche).
    - ``2147483647``
  * - query.facet.fields.sort
    - Ordre de tri des champs de facette.
    - ``count.desc``
  * - query.facet.fields.missing
    - Valeur pour les champs de facette manquants.
    - (empty)
  * - query.facet.queries
    - Définition des requêtes de facette.
    - | ``labels.facet_timestamp_title:labels.facet_timestamp_1day=timestamp:[now/d-1d TO *]	labels.facet_timestamp_1week=timestamp:[now/d-7d TO *]	labels.facet_timestamp_1month=timestamp:[now/d-1M TO *]	labels.facet_timestamp_1year=timestamp:[now/d-1y TO *]``
      | ``labels.facet_contentLength_title:labels.facet_contentLength_10k=content_length:[0 TO 9999]	labels.facet_contentLength_10kto100k=content_length:[10000 TO 99999]	labels.facet_contentLength_100kto500k=content_length:[100000 TO 499999]	labels.facet_contentLength_500kto1m=content_length:[500000 TO 999999]	labels.facet_contentLength_1m=content_length:[1000000 TO *]``
      | ``labels.facet_filetype_title:labels.facet_filetype_html=filetype:html	labels.facet_filetype_word=filetype:word	labels.facet_filetype_excel=filetype:excel	labels.facet_filetype_powerpoint=filetype:powerpoint	labels.facet_filetype_odt=filetype:odt	labels.facet_filetype_ods=filetype:ods	labels.facet_filetype_odp=filetype:odp	labels.facet_filetype_pdf=filetype:pdf	labels.facet_filetype_txt=filetype:txt	labels.facet_filetype_others=filetype:others``

.. list-table:: Classement
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - rank.fusion.window_size
    - Taille de la fenêtre pour le rank fusion.
    - ``200``
  * - rank.fusion.rank_constant
    - Constante de rang pour le rank fusion.
    - ``20``
  * - rank.fusion.threads
    - Nombre de threads pour le rank fusion.
    - ``-1``
  * - rank.fusion.timeout
    - Durée maximale (millisecondes) d'attente des searchers autres que le searcher principal lorsque Fess fusionne lui-même leurs résultats (rank.fusion.engine.enabled=false). Un searcher qui n'a pas répondu d'ici là est exclu de cette recherche, et les résultats sont marqués comme partiels et expirés. Le searcher principal est toujours attendu. 0 ou moins attend sans limite.
    - ``10000``
  * - rank.fusion.score_field
    - Champ de score pour le rank fusion.
    - ``rf_score``
  * - rank.fusion.engine.enabled
    - Indique si le moteur de recherche effectue le rank fusion. Si true, les searchers pouvant y participer apportent leurs requêtes à une seule requête, de sorte que les facettes et le nombre total de hits décrivent l'ensemble de résultats fusionné. Si false, Fess fusionne lui-même les résultats des searchers.
    - ``false``
  * - rank.fusion.combination.technique
    - Manière dont le moteur de recherche combine les scores fusionnés : rrf, arithmetic_mean, geometric_mean ou harmonic_mean.
    - ``rrf``
  * - rank.fusion.normalization.technique
    - Manière dont les scores sont normalisés avant d'être combinés : min_max, l2 ou z_score. Ignorée par rrf. z_score ne peut être combiné qu'avec arithmetic_mean ; toute autre moyenne est refusée et Fess fusionne lui-même les résultats.
    - ``min_max``
  * - rank.fusion.combination.weights
    - Poids par searcher pour la fusion côté moteur, sous forme de paires name:weight, par exemple default:0.7,semantic_chunk:0.3. La somme des poids doit valoir 1.0 et chaque searcher participant doit être nommé. Si la valeur est vide, ils ont tous le même poids.
    - (empty)
  * - rank.fusion.pagination_depth
    - Nombre de résultats que chaque searcher fournit par shard à la fusion côté moteur. Cela borne à la fois la profondeur de pagination accessible à un client et l'ensemble des documents que le moteur classe : une recherche fusionnée parcourt au plus ce nombre de résultats, et jamais plus que indexer.max.result.window.size.
    - ``1000``

.. list-table:: ACL
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - smb.role.from.file
    - Indique s'il faut obtenir les rôles SMB à partir d'un fichier.
    - ``true``
  * - smb.available.sid.types
    - Types de SID disponibles pour SMB.
    - ``1,2,4:2,5:1``
  * - file.role.from.file
    - Indique s'il faut obtenir les rôles de fichiers à partir d'un fichier.
    - ``true``
  * - ftp.role.from.file
    - Indique s'il faut obtenir les rôles FTP à partir d'un fichier.
    - ``true``

.. list-table:: Sauvegarde
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - index.backup.targets
    - Fichiers cibles pour la sauvegarde de l'index.
    - ``fess_basic_config.bulk,fess_config.bulk,fess_user.bulk,system.properties,fess.json,doc.json``
  * - index.backup.log.targets
    - Fichiers de journal cibles pour la sauvegarde de l'index.
    - ``chat_log.ndjson,click_log.ndjson,favorite_log.ndjson,search_log.ndjson,user_info.ndjson``
  * - index.backup.log.load.timeout
    - Délai d'expiration du chargement des journaux de sauvegarde de l'index.
    - ``60000``

.. list-table:: Journalisation
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - logging.app.packages
    - Packages d'application pour la journalisation.
    - ``org.codelibs,org.dbflute,org.lastaflute``
  * - logging.search.docs.enabled
    - Indique s'il faut activer la journalisation des documents de recherche.
    - ``true``
  * - logging.search.docs.fields
    - Champs à consigner pour les documents de recherche.
    - ``filetype,created,click_count,title,doc_id,url,score,site,filename,host,digest,boost,mimetype,favorite_count,_id,lang,last_modified,content_length,timestamp``
  * - logging.search.use.logfile
    - Indique s'il faut utiliser un fichier journal pour la journalisation des recherches.
    - ``true``
  * - logging.search.max.queue.size
    - Taille maximale de la file d'attente pour la journalisation des recherches.
    - ``10000``
  * - logging.click.max.queue.size
    - Taille maximale de la file d'attente pour la journalisation des clics.
    - ``10000``
  * - logging.chat.max.queue.size
    - Taille maximale de la file d'attente pour la journalisation de l'utilisation du chat.
    - ``10000``
  * - search.history.enabled
    - Indique s'il faut enregistrer les conditions de recherche des utilisateurs connectés pour l'historique de recherche.
    - ``true``
  * - search.history.size
    - Nombre maximum d'entrées de l'historique de recherche retournées par utilisateur.
    - ``10``
  * - user.tag.enabled
    - Indique si les utilisateurs connectés peuvent poser des tags sur les documents. Chaque tag appartient à l'utilisateur qui l'a créé.
    - ``false``
  * - user.tag.name.max.length
    - Longueur maximale d'un nom de tag, en points de code.
    - ``50``
  * - user.tag.max.tags
    - Nombre maximum de tags qu'un utilisateur peut posséder.
    - ``1000``
  * - user.tag.max.paths
    - Nombre maximum d'URL sur lesquelles un tag peut être posé.
    - ``10000``
  * - user.tag.queue.max.size
    - Nombre maximum de modifications de tags en attente gardées en mémoire jusqu'à leur application aux documents.
    - ``10000``
  * - user.tag.process.batch.size
    - Nombre d'URL mises à jour par requête en bloc lors de l'application des modifications de tags aux documents.
    - ``100``
  * - user.tag.visible.max.size
    - Nombre maximum de tags visibles par un utilisateur dans une recherche.
    - ``1000``

Web
---

.. list-table::
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - form.admin.max.input.size
    - Taille maximale de saisie pour les formulaires d'administration.
    - ``10000``
  * - form.admin.label.in.config.enabled
    - Indique s'il faut activer les étiquettes dans les formulaires de configuration d'administration.
    - ``false``
  * - form.admin.default.template.name
    - Nom de modèle par défaut pour les formulaires d'administration.
    - ``__TEMPLATE__``
  * - osdd.link.enabled
    - Indique s'il faut activer le lien OSDD (OpenSearch Description Document).
    - ``auto``
  * - clipboard.copy.icon.enabled
    - Indique s'il faut activer l'icône de copie dans le presse-papiers.
    - ``true``
  * - authentication.admin.users
    - Noms des utilisateurs administrateurs pour l'authentification.
    - ``admin``
  * - authentication.admin.users.ignore.case
    - Indique s'il faut comparer authentication.admin.users sans tenir compte de la casse : auto, true ou false. auto ignore la casse lorsque ldap.provider.url est défini.
    - ``auto``
  * - authentication.admin.roles
    - Noms des rôles administrateurs pour l'authentification.
    - ``admin``
  * - role.search.default.permissions
    - Permissions par défaut pour les rôles de recherche.
    - (empty)
  * - role.search.default.display.permissions
    - Permissions d'affichage par défaut pour les rôles de recherche.
    - ``{role}guest``
  * - role.search.guest.permissions
    - Conservez role.search.guest.permissions non vide. Elle initialise le rôle invité qui maintient non vide l'ensemble des rôles de recherche anonymes ; si l'ensemble de rôles résolu est vide, le filtre de rôles est ignoré (fail-open), ce qui peut désactiver le contrôle d'accès basé sur les rôles et exposer des documents aux utilisateurs anonymes. Permissions invité pour les rôles de recherche.
    - ``{role}guest``
  * - role.search.user.prefix
    - Préfixe des rôles utilisateur dans la recherche.
    - ``1``
  * - role.search.group.prefix
    - Préfixe des rôles de groupe dans la recherche.
    - ``2``
  * - role.search.role.prefix
    - Préfixe des rôles de rôle dans la recherche.
    - ``R``
  * - role.search.denied.prefix
    - Préfixe des rôles refusés dans la recherche.
    - ``D``
  * - cookie.default.path
    - Chemin par défaut du cookie (en principe '/' s'il n'y a pas de chemin de contexte)
    - ``/``
  * - cookie.default.expire
    - Expiration par défaut du cookie en secondes, par exemple 31556926 : un an, 86400 : un jour
    - ``3600``
  * - session.tracking.modes
    - Modes de suivi de session
    - ``cookie``
  * - session.cookie.secure
    - Indique s'il faut ajouter l'attribut Secure au cookie de session (JSESSIONID) au démarrage. Lorsqu'il est vide (par défaut), le comportement automatique de Tomcat est utilisé (Secure n'est ajouté que pour les requêtes HTTPS). Définissez-le à true pour les déploiements HTTPS en production, en particulier lorsque TLS est terminé au niveau d'un reverse proxy. Lorsqu'il vaut true, le cookie n'est pas envoyé via HTTP, de sorte que les sessions ne seront pas établies en HTTP simple ; laissez-le vide pour le développement en localhost. L'attribut Secure est aussi requis lorsque SameSite=none est utilisé. La modification de cette valeur nécessite un redémarrage.
    - (empty)
  * - cookie.search.parameter.keys
    - Liste séparée par des virgules des clés de paramètres de requête à stocker dans des cookies avant la connexion SSO.
    - ``q,num,sort``
  * - cookie.search.parameter.required_keys
    - Liste séparée par des virgules des clés de paramètres requis qui doivent être présents pour être stockés dans des cookies.
    - ``q``
  * - cookie.search.parameter.max.length
    - Longueur maximale des paramètres de recherche encodés stockés dans des cookies.
    - ``1000``
  * - cookie.search.parameter.max.decompressed.length
    - Taille maximale en octets à laquelle les paramètres de recherche stockés peuvent être décompressés. La limite ci-dessus s'applique au cookie compressé en gzip, ce qui ne borne pas sa taille une fois décompressé, et le cookie provient du client.
    - ``65536``
  * - cookie.search.parameter.max.restored.length
    - Longueur maximale de la chaîne de requête construite lors de la restauration des paramètres de recherche stockés après la connexion. La restauration est un confort, la connexion n'en est pas un : une chaîne plus longue est donc abandonnée plutôt qu'écrite dans un en-tête Location que le conteneur refuserait. L'encodage en pourcentage multiplie par neuf une requête CJK, cette valeur est donc bien inférieure à ce que la requête elle-même peut atteindre. Augmentez-la en même temps que tomcat.maxHttpHeaderSize dans tomcat_config.properties, qui borne les en-têtes de réponse.
    - ``4096``
  * - cookie.search.parameter.name
    - Nom du cookie utilisé pour stocker les paramètres de recherche encodés avant la connexion SSO.
    - ``fsrp``
  * - cookie.search.parameter.http_only
    - Indique s'il faut définir l'attribut HttpOnly sur le cookie des paramètres de recherche.
    - ``true``
  * - cookie.search.parameter.secure
    - Indique s'il faut définir l'attribut Secure sur le cookie des paramètres de recherche. Devrait valoir true dans les environnements de production utilisant HTTPS.
    - (empty)
  * - cookie.search.parameter.max_age
    - Max-Age (en secondes) du cookie des paramètres de recherche. Utilisez -1 pour des cookies valables uniquement pour la session.
    - ``60``
  * - cookie.search.parameter.domain
    - Attribut Domain du cookie des paramètres de recherche. Définissez la portée de domaine sur laquelle le cookie doit être disponible (par exemple, example.com).
    - (empty)
  * - cookie.search.parameter.path
    - Attribut Path du cookie des paramètres de recherche. Généralement défini sur "/" ou sur le chemin de contexte de l'application.
    - ``/``
  * - cookie.search.parameter.same_site
    - Attribut SameSite du cookie des paramètres de recherche. Valeurs valides : Lax, Strict, None
    - ``Lax``
  * - paging.page.size
    - Taille d'une page pour la pagination
    - ``25``
  * - paging.page.range.size
    - Taille de la plage de pages pour la pagination
    - ``5``
  * - paging.page.range.fill.limit
    - L'option 'fillLimit' de la plage de pages pour la pagination
    - ``true``

.. list-table:: Taille de page de récupération
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - page.docboost.max.fetch.size
    - Nombre maximum d'enregistrements docboost à récupérer par page.
    - ``1000``
  * - page.keymatch.max.fetch.size
    - Nombre maximum d'enregistrements keymatch à récupérer par page.
    - ``1000``
  * - page.labeltype.max.fetch.size
    - Nombre maximum d'enregistrements labeltype à récupérer par page.
    - ``1000``
  * - page.tagtype.max.fetch.size
    - Nombre maximum d'enregistrements tagtype à récupérer par page.
    - ``1000``
  * - page.roletype.max.fetch.size
    - Nombre maximum d'enregistrements roletype à récupérer par page.
    - ``1000``
  * - page.user.max.fetch.size
    - Nombre maximum d'enregistrements d'utilisateurs à récupérer par page.
    - ``1000``
  * - page.role.max.fetch.size
    - Nombre maximum d'enregistrements de rôles à récupérer par page.
    - ``1000``
  * - page.group.max.fetch.size
    - Nombre maximum d'enregistrements de groupes à récupérer par page.
    - ``1000``
  * - page.crawling.info.param.max.fetch.size
    - Nombre maximum de paramètres d'informations de crawl à récupérer par page.
    - ``100``
  * - page.crawling.info.max.fetch.size
    - Nombre maximum d'enregistrements d'informations de crawl à récupérer par page.
    - ``1000``
  * - page.data.config.max.fetch.size
    - Nombre maximum d'enregistrements de configuration de magasin de données à récupérer par page.
    - ``100``
  * - page.web.config.max.fetch.size
    - Nombre maximum d'enregistrements de configuration Web à récupérer par page.
    - ``100``
  * - page.file.config.max.fetch.size
    - Nombre maximum d'enregistrements de configuration de fichiers à récupérer par page.
    - ``100``
  * - page.duplicate.host.max.fetch.size
    - Nombre maximum d'enregistrements d'hôtes en double à récupérer par page.
    - ``1000``
  * - page.failure.url.max.fetch.size
    - Nombre maximum d'enregistrements d'URL en échec à récupérer par page.
    - ``1000``
  * - page.favorite.log.max.fetch.size
    - Nombre maximum d'enregistrements du journal des favoris à récupérer par page.
    - ``100``
  * - page.file.auth.max.fetch.size
    - Nombre maximum d'enregistrements d'authentification de fichier à récupérer par page.
    - ``100``
  * - page.web.auth.max.fetch.size
    - Nombre maximum d'enregistrements d'authentification Web à récupérer par page.
    - ``100``
  * - page.path.mapping.max.fetch.size
    - Nombre maximum d'enregistrements de mappage de chemin à récupérer par page.
    - ``1000``
  * - page.request.header.max.fetch.size
    - Nombre maximum d'enregistrements d'en-têtes de requête à récupérer par page.
    - ``1000``
  * - page.scheduled.job.max.fetch.size
    - Nombre maximum d'enregistrements de jobs planifiés à récupérer par page.
    - ``100``
  * - page.elevate.word.max.fetch.size
    - Nombre maximum d'enregistrements de mots ajoutés à récupérer par page.
    - ``1000``
  * - page.bad.word.max.fetch.size
    - Nombre maximum d'enregistrements de mots exclus à récupérer par page.
    - ``1000``
  * - page.dictionary.max.fetch.size
    - Nombre maximum d'enregistrements de dictionnaires à récupérer par page.
    - ``1000``
  * - page.relatedcontent.max.fetch.size
    - Nombre maximum d'enregistrements de contenu associé à récupérer par page.
    - ``5000``
  * - page.relatedquery.max.fetch.size
    - Nombre maximum d'enregistrements de requêtes associées à récupérer par page.
    - ``5000``
  * - page.thumbnail.queue.max.fetch.size
    - Nombre maximum d'enregistrements de la file d'attente de vignettes à récupérer par page.
    - ``100``
  * - page.thumbnail.purge.max.fetch.size
    - Nombre maximum d'enregistrements de purge de vignettes à récupérer par page.
    - ``100``
  * - page.score.booster.max.fetch.size
    - Nombre maximum d'enregistrements de booster de score à récupérer par page.
    - ``1000``
  * - page.searchlog.max.fetch.size
    - Nombre maximum d'enregistrements du journal de recherche à récupérer par page.
    - ``10000``
  * - page.searchlist.track.total.hits
    - Indique s'il faut suivre le nombre total de hits dans la page de liste de recherche.
    - ``true``
  * - page.searchlist.content.max.length
    - Longueur maximale du contenu (en caractères) affichée sur la page d'édition de la liste de recherche.
    - ``100000``

.. list-table:: Page de recherche
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - paging.search.page.start
    - Page de départ par défaut des résultats de recherche.
    - ``0``
  * - paging.search.page.size
    - Taille par défaut des résultats de recherche par page.
    - ``10``
  * - paging.search.page.max.size
    - Taille maximale des résultats de recherche par page.
    - ``100``
  * - api.param.max.length
    - Longueur maximale d'un paramètre de requête de type chaîne de l'API v2 (q, sort, sdh). OWASP API4:2023.
    - ``1000``
  * - api.param.max.array.size
    - Nombre maximum de valeurs d'un paramètre de requête répétable de l'API v2.
    - ``100``
  * - api.click.max.timestamp
    - Horodatage maximal du journal de clics (rt, epoch ms) accepté par l'API de clics v2. OWASP API4:2023.
    - ``9999999999999``
  * - searchlog.agg.shard.size
    - searchlog
    - ``-1``
  * - searchlog.request.headers
    - En-têtes de requête à inclure dans le journal de recherche.
    - (empty)
  * - searchlog.process.batch_size
    - Taille de lot pour le traitement du journal de recherche.
    - ``100``
  * - related_query.generate.days
    - Nombre de jours de journaux de recherche lus lors de la génération de requêtes associées à partir des journaux de recherche.
    - ``30``
  * - related_query.generate.term.size
    - Nombre maximum de termes générés par hôte virtuel.
    - ``100``
  * - related_query.generate.query.size
    - Nombre maximum de requêtes associées générées par terme.
    - ``5``
  * - related_query.generate.min.sessions
    - Nombre minimum de sessions utilisateur distinctes requis pour un terme et pour chacune de ses requêtes associées.
    - ``3``
  * - related_query.generate.session.interval
    - Intervalle (minutes) après une recherche dans lequel une recherche suivante de la même session compte comme une reformulation.
    - ``10``
  * - related_query.generate.seed.log.size
    - Nombre maximum de journaux de recherche d'un terme lus pour trouver les sessions qui l'ont recherché.
    - ``1000``
  * - related_query.generate.seed.session.size
    - Nombre maximum de sessions par terme dont les recherches suivantes sont lues.
    - ``200``
  * - related_query.generate.log.fetch.size
    - Nombre maximum de journaux des recherches suivantes lus par terme.
    - ``2000``
  * - related_query.generate.query.min.length
    - Longueur minimale (en caractères) d'un terme ou d'une requête associée générés.
    - ``2``
  * - related_query.generate.query.max.length
    - Longueur maximale (en caractères) d'un terme ou d'une requête associée générés.
    - ``50``
  * - docreport.duplicate.group.size
    - docreport Nombre maximum de groupes de doublons affichés par l'écran de rapport de documents, les plus grands en premier.
    - ``100``
  * - docreport.duplicate.docs.size
    - Nombre maximum de documents que l'écran de rapport de documents liste pour chaque groupe de doublons.
    - ``10``
  * - docreport.duplicate.export.page.size
    - Nombre de signatures de contenu lues par requête lors du téléchargement du rapport de doublons au format CSV.
    - ``10000``
  * - docreport.dormant.days
    - Nombre de jours par défaut depuis la dernière modification au-delà duquel un document est considéré comme inactif.
    - ``365``
  * - thumbnail.html.image.min.width
    - Largeur minimale des images HTML dans les vignettes.
    - ``100``
  * - thumbnail.html.image.min.height
    - Hauteur minimale des images HTML dans les vignettes.
    - ``100``
  * - thumbnail.html.image.max.aspect.ratio
    - Rapport d'aspect maximal des images HTML dans les vignettes.
    - ``3.0``
  * - thumbnail.html.image.thumbnail.width
    - Largeur des images de vignette générées.
    - ``100``
  * - thumbnail.html.image.thumbnail.height
    - Hauteur des images de vignette générées.
    - ``100``
  * - thumbnail.html.image.format
    - Format des images de vignette générées.
    - ``png``
  * - thumbnail.html.image.xpath
    - XPath pour sélectionner les images pour les vignettes.
    - ``//IMG``
  * - thumbnail.html.image.exclude.extensions
    - Extensions de fichier à exclure de la génération de vignettes.
    - ``svg,html,css,js``
  * - thumbnail.generator.interval
    - Intervalle du générateur de vignettes.
    - ``0``
  * - thumbnail.generator.targets
    - Cibles du générateur de vignettes (par exemple, all).
    - ``all``
  * - thumbnail.crawler.enabled
    - Indique si le crawler de vignettes est activé.
    - ``true``
  * - thumbnail.system.monitor.interval
    - Intervalle du moniteur système dans le traitement des vignettes.
    - ``60``

.. list-table:: Utilisateur
  :header-rows: 1

  * - Name
    - Description
    - Default
  * - user.code.request.parameter
    - Paramètres du code utilisateur
    - ``userCode``
  * - user.code.min.length
    - Longueur minimale du code utilisateur.
    - ``20``
  * - user.code.max.length
    - Longueur maximale du code utilisateur.
    - ``100``
  * - user.code.pattern
    - Motif du code utilisateur pour la validation.
    - ``[a-zA-Z0-9_]+``
  * - mail.from.name
    - Nom à afficher dans le champ From des e-mails.
    - ``Administrator``
  * - mail.from.address
    - Adresse e-mail à utiliser dans le champ From.
    - ``root@localhost``
  * - mail.hostname
    - Nom d'hôte du serveur de messagerie.
    - (empty)
  * - scheduler.target.name
    - Nom de la cible pour le planificateur.
    - (empty)
  * - scheduler.job.class
    - Classe de job pour le planificateur.
    - ``org.codelibs.fess.app.job.ScriptExecutorJob``
  * - scheduler.concurrent.exec.mode
    - Mode d'exécution concurrente dans le planificateur.
    - ``QUIT``
  * - scheduler.monitor.interval
    - Intervalle de surveillance du planificateur.
    - ``30``
  * - coordinator.poll.interval
    - Intervalle (secondes) d'interrogation des heartbeats et des événements.
    - ``60``
  * - coordinator.heartbeat.ttl
    - Durée de vie (ms) des documents heartbeat d'instance.
    - ``180000``
  * - coordinator.operation.ttl
    - Durée de vie (ms) des documents de verrou d'opération.
    - ``7200000``
  * - coordinator.operation.retry
    - Nombre maximum de tentatives d'acquisition d'un verrou d'opération.
    - ``3``
  * - coordinator.event.ttl
    - Durée de vie (ms) des documents de notification d'événement.
    - ``600000``
  * - online.help.base.link
    - Lien de base de l'aide en ligne.
    - ``https://fess.codelibs.org/{lang}/{version}/admin/``
  * - online.help.installation
    - Lien du guide d'installation pour l'aide en ligne.
    - ``https://fess.codelibs.org/{lang}/{version}/install/install.html``
  * - online.help.eol
    - Lien des informations de fin de vie pour l'aide en ligne.
    - ``https://fess.codelibs.org/{lang}/eol.html``
  * - online.help.name.failureurl
    - Clé de l'aide en ligne pour l'URL en échec.
    - ``failureurl``
  * - online.help.name.elevateword
    - Clé de l'aide en ligne pour le mot ajouté.
    - ``elevateword``
  * - online.help.name.reqheader
    - Clé de l'aide en ligne pour l'en-tête de requête.
    - ``reqheader``
  * - online.help.name.dict.synonym
    - Clé de l'aide en ligne pour le dictionnaire de synonymes.
    - ``synonym``
  * - online.help.name.dict
    - Clé de l'aide en ligne pour le dictionnaire.
    - ``dict``
  * - online.help.name.dict.kuromoji
    - Clé de l'aide en ligne pour le dictionnaire Kuromoji.
    - ``kuromoji``
  * - online.help.name.dict.protwords
    - Clé de l'aide en ligne pour le dictionnaire de mots protégés.
    - ``protwords``
  * - online.help.name.dict.stopwords
    - Clé de l'aide en ligne pour le dictionnaire de mots vides.
    - ``stopwords``
  * - online.help.name.dict.stemmeroverride
    - Clé de l'aide en ligne pour le dictionnaire de remplacement de stemmer.
    - ``stemmeroverride``
  * - online.help.name.dict.mapping
    - Clé de l'aide en ligne pour le dictionnaire de mappage.
    - ``mapping``
  * - online.help.name.webconfig
    - Clé de l'aide en ligne pour la configuration Web.
    - ``webconfig``
  * - online.help.name.searchlist
    - Clé de l'aide en ligne pour la liste de recherche.
    - ``searchlist``
  * - online.help.name.log
    - Clé de l'aide en ligne pour le journal.
    - ``log``
  * - online.help.name.general
    - Clé de l'aide en ligne pour les paramètres généraux.
    - ``general``
  * - online.help.name.role
    - Clé de l'aide en ligne pour le rôle.
    - ``role``
  * - online.help.name.joblog
    - Clé de l'aide en ligne pour le journal des jobs.
    - ``joblog``
  * - online.help.name.keymatch
    - Clé de l'aide en ligne pour keymatch.
    - ``keymatch``
  * - online.help.name.relatedquery
    - Clé de l'aide en ligne pour la requête associée.
    - ``relatedquery``
  * - online.help.name.relatedcontent
    - Clé de l'aide en ligne pour le contenu associé.
    - ``relatedcontent``
  * - online.help.name.wizard
    - Clé de l'aide en ligne pour l'assistant.
    - ``wizard``
  * - online.help.name.badword
    - Clé de l'aide en ligne pour le mot exclu.
    - ``badword``
  * - online.help.name.pathmap
    - Clé de l'aide en ligne pour le mappage de chemin.
    - ``pathmap``
  * - online.help.name.boostdoc
    - Clé de l'aide en ligne pour le boost de document.
    - ``boostdoc``
  * - online.help.name.dataconfig
    - Clé de l'aide en ligne pour la configuration de magasin de données.
    - ``dataconfig``
  * - online.help.name.systeminfo
    - Clé de l'aide en ligne pour les informations système.
    - ``systeminfo``
  * - online.help.name.user
    - Clé de l'aide en ligne pour l'utilisateur.
    - ``user``
  * - online.help.name.group
    - Clé de l'aide en ligne pour le groupe.
    - ``group``
  * - online.help.name.dashboard
    - Clé de l'aide en ligne pour le tableau de bord.
    - ``dashboard``
  * - online.help.name.webauth
    - Clé de l'aide en ligne pour l'authentification Web.
    - ``webauth``
  * - online.help.name.fileconfig
    - Clé de l'aide en ligne pour la configuration de fichiers.
    - ``fileconfig``
  * - online.help.name.fileauth
    - Clé de l'aide en ligne pour l'authentification de fichier.
    - ``fileauth``
  * - online.help.name.labeltype
    - Clé de l'aide en ligne pour le type d'étiquette.
    - ``labeltype``
  * - online.help.name.tagtype
    - Clé de l'aide en ligne pour le type de tag.
    - ``tagtype``
  * - online.help.name.duplicatehost
    - Clé de l'aide en ligne pour l'hôte en double.
    - ``duplicatehost``
  * - online.help.name.scheduler
    - Clé de l'aide en ligne pour le planificateur.
    - ``scheduler``
  * - online.help.name.crawlinginfo
    - Clé de l'aide en ligne pour les informations de crawl.
    - ``crawlinginfo``
  * - online.help.name.backup
    - Clé de l'aide en ligne pour la sauvegarde.
    - ``backup``
  * - online.help.name.upgrade
    - Clé de l'aide en ligne pour la mise à niveau.
    - ``upgrade``
  * - online.help.name.sereq
    - Clé de l'aide en ligne pour la requête de recherche.
    - ``sereq``
  * - online.help.name.accesstoken
    - Clé de l'aide en ligne pour le jeton d'accès.
    - ``accesstoken``
  * - online.help.name.suggest
    - Clé de l'aide en ligne pour la suggestion.
    - ``suggest``
  * - online.help.name.searchlog
    - Clé de l'aide en ligne pour le journal de recherche.
    - ``searchlog``
  * - online.help.name.maintenance
    - Clé de l'aide en ligne pour la maintenance.
    - ``maintenance``
  * - online.help.name.plugin
    - Clé de l'aide en ligne pour le plugin.
    - ``plugin``
  * - online.help.name.storage
    - Clé de l'aide en ligne pour le stockage.
    - ``storage``
  * - online.help.name.docreport
    - Clé de l'aide en ligne pour le rapport de documents.
    - ``docreport``
  * - online.help.supported.langs
    - Langues prises en charge pour l'aide en ligne.
    - ``de,es,fr,ja,ko,zh-cn``
  * - forum.link
    - Lien du forum pour l'assistance aux utilisateurs.
    - ``https://discuss.codelibs.org/c/Fess{lang}/``
  * - forum.supported.langs
    - Langues prises en charge pour le forum.
    - ``en,ja``
  * - suggest.popular.word.seed
    - Valeur de seed pour la suggestion de mots populaires.
    - ``0``
  * - suggest.popular.word.tags
    - Tags pour la suggestion de mots populaires.
    - (empty)
  * - suggest.popular.word.fields
    - Champs pour la suggestion de mots populaires.
    - (empty)
  * - suggest.popular.word.excludes
    - Mots exclus pour la suggestion de mots populaires.
    - (empty)
  * - suggest.popular.word.size
    - Nombre de mots populaires à suggérer.
    - ``10``
  * - suggest.popular.word.window.size
    - Taille de la fenêtre pour la suggestion de mots populaires.
    - ``30``
  * - suggest.popular.word.query.freq
    - Fréquence des requêtes pour la suggestion de mots populaires.
    - ``10``
  * - suggest.min.hit.count
    - Nombre minimum de hits pour la suggestion.
    - ``1``
  * - suggest.field.contents
    - Champ pour le contenu des suggestions.
    - ``_default``
  * - suggest.field.tags
    - Champ pour les tags des suggestions.
    - ``label``
  * - suggest.field.roles
    - Champ pour les rôles des suggestions.
    - ``role``
  * - suggest.field.index.contents
    - Contenus de l'index pour la suggestion.
    - ``content,title``
  * - suggest.update.request.interval
    - Intervalle des requêtes de mise à jour des suggestions.
    - ``0``
  * - suggest.update.doc.per.request
    - Nombre de documents par requête de mise à jour des suggestions.
    - ``2``
  * - suggest.update.contents.limit.num.percentage
    - Limite en pourcentage pour le contenu de la mise à jour des suggestions.
    - ``50%``
  * - suggest.update.contents.limit.num
    - Nombre maximum de contenus de mise à jour des suggestions.
    - ``10000``
  * - suggest.update.contents.limit.doc.size
    - Taille maximale des documents pour la mise à jour des suggestions.
    - ``50000``
  * - suggest.source.reader.scroll.size
    - Taille de scroll pour le lecteur de source des suggestions.
    - ``1``
  * - suggest.popular.word.cache.size
    - Taille du cache pour la suggestion de mots populaires.
    - ``1000``
  * - suggest.popular.word.cache.expire
    - Expiration du cache (secondes) pour la suggestion de mots populaires.
    - ``60``
  * - suggest.search.log.permissions
    - Permissions pour le journal de recherche des suggestions.
    - ``{user}guest,{role}guest``
  * - suggest.system.monitor.interval
    - Intervalle du moniteur système dans la suggestion.
    - ``60``
  * - ldap.admin.enabled
    - Indique si l'administration LDAP est activée.
    - ``false``
  * - ldap.admin.user.filter
    - Filtre utilisateur pour l'administration LDAP.
    - ``uid=%s``
  * - ldap.admin.user.base.dn
    - Base DN pour l'utilisateur de l'administration LDAP.
    - ``ou=People,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.user.object.classes
    - Classes d'objets pour l'utilisateur de l'administration LDAP.
    - ``organizationalPerson,top,person,inetOrgPerson``
  * - ldap.admin.role.filter
    - Filtre de rôle pour l'administration LDAP.
    - ``cn=%s``
  * - ldap.admin.role.base.dn
    - Base DN pour le rôle de l'administration LDAP.
    - ``ou=Role,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.role.object.classes
    - Classes d'objets pour le rôle de l'administration LDAP.
    - ``groupOfNames``
  * - ldap.admin.group.filter
    - Filtre de groupe pour l'administration LDAP.
    - ``cn=%s``
  * - ldap.admin.group.base.dn
    - Base DN pour le groupe de l'administration LDAP.
    - ``ou=Group,dc=fess,dc=codelibs,dc=org``
  * - ldap.admin.group.object.classes
    - Classes d'objets pour le groupe de l'administration LDAP.
    - ``groupOfNames``
  * - ldap.admin.sync.password
    - Indique s'il faut synchroniser le mot de passe pour l'administration LDAP.
    - ``true``
  * - ldap.auth.validation
    - Indique s'il faut valider l'authentification LDAP.
    - ``true``
  * - ldap.connect.timeout
    - Délai d'expiration (millisecondes) pour établir une connexion LDAP. Il borne aussi le handshake TLS et la réponse initiale du bind. 0 ou moins laisse la valeur par défaut du JDK/de l'OS.
    - ``10000``
  * - ldap.read.timeout
    - Délai d'expiration (millisecondes) d'attente d'une réponse LDAP une fois la connexion liée. 0 ou moins attend indéfiniment.
    - ``30000``
  * - ldap.search.time.limit
    - Limite de temps côté serveur (millisecondes) pour une recherche LDAP. 0 ou moins signifie aucune limite.
    - ``60000``
  * - ldap.max.username.length
    - Longueur maximale du nom d'utilisateur pour LDAP.
    - ``-1``
  * - ldap.ignore.netbios.name
    - Indique s'il faut ignorer le nom NetBIOS dans LDAP.
    - ``true``
  * - ldap.group.name.with.underscores
    - Indique s'il faut autoriser les traits de soulignement dans les noms de groupes LDAP.
    - ``false``
  * - ldap.lowercase.permission.name
    - Indique s'il faut utiliser des minuscules pour les noms de permissions LDAP.
    - ``false``
  * - ldap.allow.empty.permission
    - Indique s'il faut autoriser les permissions vides dans LDAP.
    - ``true``
  * - ldap.samaccountname.group
    - Indique s'il faut utiliser samAccountName pour le groupe LDAP.
    - ``false``
  * - ldap.role.search.user.enabled
    - Indique si la recherche de rôles LDAP pour l'utilisateur est activée.
    - ``true``
  * - ldap.role.search.group.enabled
    - Indique si la recherche de rôles LDAP pour le groupe est activée.
    - ``true``
  * - ldap.role.search.role.enabled
    - Indique si la recherche de rôles LDAP pour le rôle est activée.
    - ``true``
  * - ldap.attr.surname
    - Attribut LDAP pour le nom de famille.
    - ``sn``
  * - ldap.attr.givenName
    - Attribut LDAP pour le prénom.
    - ``givenName``
  * - ldap.attr.employeeNumber
    - Attribut LDAP pour le numéro d'employé.
    - ``employeeNumber``
  * - ldap.attr.mail
    - Attribut LDAP pour l'e-mail.
    - ``mail``
  * - ldap.attr.telephoneNumber
    - Attribut LDAP pour le numéro de téléphone.
    - ``telephoneNumber``
  * - ldap.attr.homePhone
    - Attribut LDAP pour le téléphone personnel.
    - ``homePhone``
  * - ldap.attr.homePostalAddress
    - Attribut LDAP pour l'adresse postale personnelle.
    - ``homePostalAddress``
  * - ldap.attr.labeledURI
    - Attribut LDAP pour l'URI étiquetée.
    - ``labeledURI``
  * - ldap.attr.roomNumber
    - Attribut LDAP pour le numéro de salle.
    - ``roomNumber``
  * - ldap.attr.description
    - Attribut LDAP pour la description.
    - ``description``
  * - ldap.attr.title
    - Attribut LDAP pour le titre.
    - ``title``
  * - ldap.attr.pager
    - Attribut LDAP pour le bipeur.
    - ``pager``
  * - ldap.attr.street
    - Attribut LDAP pour la rue.
    - ``street``
  * - ldap.attr.postalCode
    - Attribut LDAP pour le code postal.
    - ``postalCode``
  * - ldap.attr.physicalDeliveryOfficeName
    - Attribut LDAP pour le nom du bureau de livraison physique.
    - ``physicalDeliveryOfficeName``
  * - ldap.attr.destinationIndicator
    - Attribut LDAP pour l'indicateur de destination.
    - ``destinationIndicator``
  * - ldap.attr.internationaliSDNNumber
    - Attribut LDAP pour le numéro ISDN international.
    - ``internationaliSDNNumber``
  * - ldap.attr.state
    - Attribut LDAP pour l'état.
    - ``st``
  * - ldap.attr.employeeType
    - Attribut LDAP pour le type d'employé.
    - ``employeeType``
  * - ldap.attr.facsimileTelephoneNumber
    - Attribut LDAP pour le numéro de téléphone de télécopie.
    - ``facsimileTelephoneNumber``
  * - ldap.attr.postOfficeBox
    - Attribut LDAP pour la boîte postale.
    - ``postOfficeBox``
  * - ldap.attr.initials
    - Attribut LDAP pour les initiales.
    - ``initials``
  * - ldap.attr.carLicense
    - Attribut LDAP pour l'immatriculation de voiture.
    - ``carLicense``
  * - ldap.attr.mobile
    - Attribut LDAP pour le mobile.
    - ``mobile``
  * - ldap.attr.postalAddress
    - Attribut LDAP pour l'adresse postale.
    - ``postalAddress``
  * - ldap.attr.city
    - Attribut LDAP pour la ville.
    - ``l``
  * - ldap.attr.teletexTerminalIdentifier
    - Attribut LDAP pour l'identifiant de terminal télétex.
    - ``teletexTerminalIdentifier``
  * - ldap.attr.x121Address
    - Attribut LDAP pour l'adresse X.121.
    - ``x121Address``
  * - ldap.attr.businessCategory
    - Attribut LDAP pour la catégorie professionnelle.
    - ``businessCategory``
  * - ldap.attr.registeredAddress
    - Attribut LDAP pour l'adresse enregistrée.
    - ``registeredAddress``
  * - ldap.attr.displayName
    - Attribut LDAP pour le nom d'affichage.
    - ``displayName``
  * - ldap.attr.preferredLanguage
    - Attribut LDAP pour la langue préférée.
    - ``preferredLanguage``
  * - ldap.attr.departmentNumber
    - Attribut LDAP pour le numéro de département.
    - ``departmentNumber``
  * - ldap.attr.uidNumber
    - Attribut LDAP pour le numéro UID.
    - ``uidNumber``
  * - ldap.attr.gidNumber
    - Attribut LDAP pour le numéro GID.
    - ``gidNumber``
  * - ldap.attr.homeDirectory
    - Attribut LDAP pour le répertoire personnel.
    - ``homeDirectory``
  * - plugin.repositories
    - URL des dépôts de plugins.
    - ``https://maven.codelibs.org/release/org/codelibs/fess/,https://repo.maven.apache.org/maven2/org/codelibs/fess/,https://fess.codelibs.org/plugin/artifacts.yaml``
  * - plugin.version.filter
    - Filtre de version pour les plugins.
    - (empty)
  * - storage.max.items.in.page
    - Nombre maximum d'éléments par page dans le stockage.
    - ``1000``
  * - password.invalid.admin.passwords
    - Liste des mots de passe administrateur invalides.
    - ``admin``
  * - password.min.length
    - Longueur minimale du mot de passe (0 pour désactiver).
    - ``8``
  * - password.max.length
    - Longueur maximale d'un champ de mot de passe.
    - ``100``
  * - password.require.uppercase
    - Exiger des lettres majuscules dans le mot de passe.
    - ``false``
  * - password.require.lowercase
    - Exiger des lettres minuscules dans le mot de passe.
    - ``false``
  * - password.require.digit
    - Exiger des chiffres dans le mot de passe.
    - ``false``
  * - password.require.special.char
    - Exiger des caractères spéciaux dans le mot de passe.
    - ``false``
  * - rag.chat.enabled
    - Indique si la fonctionnalité de chat RAG est activée.
    - ``false``
  * - rag.chat.log.enabled
    - Indique s'il faut enregistrer l'utilisation de chaque requête de chat RAG (utilisateur, heure, appels au LLM et tokens) dans le journal de chat. La question et la réponse ne sont jamais enregistrées.
    - ``true``
  * - rag.chat.context.max.documents
    - Paramètres de génération du chat.
    - ``5``
  * - rag.chat.query.regeneration.max.count
    - Nombre maximum de fois qu'une requête de chat régénère sa requête de recherche et relance la recherche lorsque celle-ci ne trouve aucun document ou, dans le chat en streaming, qu'aucun des hits n'est jugé pertinent. Chaque régénération effectue un appel au LLM, plus un appel d'évaluation de pertinence lorsque la nouvelle recherche a des hits (0 désactive).
    - ``2``
  * - rag.chat.session.timeout.minutes
    - Paramètres de session.
    - ``30``
  * - rag.chat.session.max.size
    - Nombre maximum de sessions de chat en cache ; les moins récemment consultées sont évincées au-delà (0 ou moins signifie 100).
    - ``10000``
  * - rag.chat.history.max.messages
    - Nombre maximum de messages conservés dans une session de chat ; les tours plus anciens sont supprimés à chaque nouveau message.
    - ``30``
  * - rag.chat.content.fields
    - Paramètres du flux RAG amélioré. Champs à récupérer pour le contenu complet du document.
    - ``title,url,content,doc_id,content_title,content_description``
  * - rag.chat.highlight.fragment.size
    - Paramètres de surlignage pour la recherche RAG.
    - ``500``
  * - rag.chat.highlight.number.of.fragments
    - Nombre de fragments de surlignage par document dans la recherche de contexte du chat RAG.
    - ``3``
  * - rag.chat.content.fulltext.max.length
    - Gestion des documents volumineux pour la génération de réponses. Les documents dont content_length dépasse cette valeur utilisent des passages surlignés au lieu du contenu complet dans le contexte de réponse.
    - ``3000``
  * - rag.chat.answer.highlight.fragment.size
    - Paramètres de surlignage utilisés lors de l'extraction de passages de documents volumineux pour le contexte de réponse.
    - ``1000``
  * - rag.chat.answer.highlight.number.of.fragments
    - Nombre de fragments de surlignage extraits de chaque document surdimensionné pour le contexte de réponse.
    - ``5``
  * - rag.chat.history.assistant.content
    - Mode de contenu de l'historique pour les messages de l'assistant. smart_summary - supprime le corps de la réponse de l'assistant, ne conserve que la requête de recherche passée + les titres référencés par tour (par défaut, recommandé) full - envoie la réponse complète de l'assistant source_titles - corps + suffixe des titres référencés source_titles_and_urls - uniquement "[References: title (url), ...]" truncated - tronque la réponse de l'assistant à history.assistant.max.chars none - supprime les tours de l'assistant de l'historique
    - ``smart_summary``
  * - rag.chat.history.titles.max.count
    - Nombre maximum de titres de documents référencés inclus par tour en mode d'historique smart_summary.
    - ``5``
  * - rag.chat.document.max.parts
    - Nombre maximum de parties en lesquelles un document est découpé lors d'un chat portant sur un seul document plus long que le budget de contexte du LLM. Chaque partie est résumée séparément et les résumés sont combinés dans la réponse ; les parties au-delà de ce nombre ne sont pas utilisées. Une requête portant sur un tel document effectue jusqu'à ce nombre d'appels au LLM, plus un pour la réponse, à chaque tour.
    - ``10``
  * - rag.chat.response.language
    - Langue dans laquelle le LLM doit répondre. browser - la langue du navigateur de l'utilisateur ou de la locale de l'UI ; aucune instruction pour l'anglais (par défaut) none - aucune instruction de langue ; le LLM répond généralement dans la langue de la question en, ja.. - répondre toujours dans cette langue
    - ``browser``
  * - index.export.path
    - Exportation d'index
    - ``/var/lib/fess/export``
  * - index.export.exclude.fields
    - Champs de document séparés par des virgules omis des fichiers écrits par le job d'exportation d'index.
    - ``cache,tag``
  * - index.export.scroll.size
    - Nombre de documents récupérés par requête scroll par le job d'exportation d'index.
    - ``100``
  * - index.export.format
    - Format de sortie des documents exportés ; seuls html et json sont acceptés, toute autre valeur fait échouer le job.
    - ``html``
  * - log.notification.flush.interval
    - Notification des journaux Intervalle (secondes) de vidage du tampon de notification des journaux vers le moteur de recherche.
    - ``30``
  * - log.notification.max.details.length
    - Longueur maximale du texte des détails de notification.
    - ``3000``
  * - log.notification.max.display.events
    - Nombre maximum d'événements à afficher dans la notification.
    - ``50``
  * - log.notification.max.message.length
    - Longueur maximale de chaque message de journal dans la notification.
    - ``200``
  * - log.notification.search.size
    - Nombre maximum d'événements à récupérer depuis le moteur de recherche par job de notification.
    - ``1000``
  * - log.notification.buffer.size
    - Nombre maximum d'événements à mettre en tampon en mémoire.
    - ``1000``
  * - log.notification.interval
    - Intervalle (secondes) du cycle du job de notification, utilisé dans les messages de notification.
    - ``300``
  * - theme.directory.path
    - Système de thèmes statiques (voir docs/superpowers/specs/2026-05-21-fess-static-theme-design.md)
    - ``themes``
  * - theme.upload.max.size
    - Taille maximale (octets) d'une archive de thème téléversée.
    - ``52428800``
  * - theme.upload.max.extracted.size
    - Taille totale extraite maximale (octets) ; l'extraction est interrompue dès qu'elle est dépassée.
    - ``209715200``
  * - theme.upload.max.entries
    - Nombre maximum d'entrées autorisées dans une archive de thème téléversée.
    - ``1000``
  * - theme.upload.max.compression.ratio
    - Rapport maximal décompressé/compressé pour une seule entrée d'archive de thème.
    - ``100``
  * - theme.upload.zip.ratio.max
    - Rapport cumulé maximal décompressé/compressé pour l'ensemble de l'archive (protection contre les zip bombs).
    - ``50``
  * - theme.upload.zip.ratio.check.threshold.bytes
    - Octets compressés lus avant que la vérification du rapport zip cumulé ne s'applique ; les archives plus petites l'ignorent.
    - ``65536``
  * - theme.upload.attic.retention.days
    - Durée de conservation (jours) d'un répertoire de thème remplacé avant que le nettoyage ne le supprime.
    - ``7``
  * - theme.repositories
    - URL de dépôts (séparées par des virgules) depuis lesquels les thèmes statiques sont téléchargés.
    - ``https://maven.codelibs.org/release/org/codelibs/fess/themes/``
  * - theme.index.frame.ancestors
    - Valeur de la directive frame-ancestors dans le Content-Security-Policy des pages HTML du thème statique : les origines qui peuvent les intégrer dans un frame. La valeur par défaut 'none' empêche toute page de les intégrer. WebKit (Safari) applique frame-ancestors aux frames blob: qu'utilisent l'aperçu de fichier et l'affichage du cache d'un thème, et les affiche donc vides tant que la valeur est 'none'. Laissez la valeur vide pour supprimer la directive ; X-Frame-Options: DENY est envoyé dans tous les cas et garde alors les pages hors des frames dans tous les navigateurs (un navigateur qui respecte frame-ancestors ignore cet en-tête).
    - ``'none'``
  * - theme.api.csrf.server.origins
    - Facultatif : origine(s) externe(s) canonique(s) de cette instance Fess (séparées par des virgules ou des sauts de ligne), par exemple https://fess.example.com. Lorsqu'elles sont définies, elles sont traitées comme de même origine pour la vérification CSRF Origin de l'API v2 SANS faire confiance aux en-têtes transmis (forwarded). Recommandé derrière des reverse proxies qui ne figurent pas dans rate.limit.trusted.proxies. Lorsque la valeur est vide, l'origine cible est reconstruite à partir des en-têtes X-Forwarded-\* du proxy de confiance, puis à partir de la requête servlet.
    - (empty)
  * - theme.api.login.rate.limit.per.ip.per.minute
    - Tentatives de connexion autorisées par IP cliente et par minute ; 0 ou moins désactive ce contrôle.
    - ``10``
  * - theme.api.login.rate.limit.per.user.per.minute
    - Tentatives de connexion autorisées par IP cliente et par nom d'utilisateur et par minute ; limite aussi le changement de mot de passe.
    - ``5``
  * - theme.api.login.lockout.seconds
    - Verrouillage (secondes) appliqué une fois qu'une limite de débit de connexion est dépassée ; 0 ou moins désactive le verrouillage.
    - ``900``
  * - theme.api.login.rate.limit.max.entries
    - Nombre maximum de buckets de limitation de débit de connexion conservés en mémoire ; les buckets inactifs sont évincés lorsque le plafond est atteint.
    - ``100000``
  * - api.chat.stream.keepalive.interval.ms
    - Intervalle entre les pings keep-alive SSE émis par /api/v2/chat/stream. Le ping est une ligne de commentaire uniquement (": keepalive\\n\\n") qui n'affecte pas le flux d'événements mais contourne les intermédiaires (le proxy_read_timeout par défaut de nginx est de 60s) qui coupent les connexions inactives pendant les longues phases LLM. Définissez <=0 pour désactiver. Unité : millisecondes.
    - ``15000``
.. GENERATED-END: properties
