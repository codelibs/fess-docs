==================================
Configuration de la limitation de débit
==================================

Aperçu
====

|Fess| dispose d'une fonctionnalité de limitation de débit pour maintenir la stabilité et les performances du système.
Cette fonctionnalité protège le système contre les requêtes excessives et permet une allocation équitable des ressources.

La limitation de débit s'applique dans les situations suivantes :

- Toutes les requêtes HTTP, y compris l'API de recherche, l'API de mode de recherche IA et les pages d'administration (``RateLimitFilter``)
- Requêtes du crawler (contrôlées par la configuration du crawl)

Limitation de débit des requêtes HTTP
======================================

Vous pouvez limiter le nombre de requêtes HTTP vers |Fess| par adresse IP.
Cette limitation s'applique à toutes les requêtes HTTP, y compris l'API de recherche, l'API de mode de recherche IA, les pages d'administration, etc.

Configuration
----

``app/WEB-INF/classes/fess_config.properties`` :

::

    # Activer la limitation de debit (defaut: false)
    rate.limit.enabled=true

    # Nombre maximum de requetes par fenetre par adresse IP (defaut: 100)
    rate.limit.requests.per.window=100

    # Taille de la fenetre de limitation de debit (millisecondes) (defaut: 60000)
    rate.limit.window.ms=60000

Comportement
----

- Les requêtes dépassant la limite de débit retournent HTTP 429 (Too Many Requests)
- Les requêtes provenant d'IP bloquées pour dépassement de la limite ou figurant dans la liste de blocage retournent HTTP 403 (Forbidden)
- Le corps de la réponse est du JSON (429 : ``{"error":"rate_limit_exceeded",...,"retry_after":60}`` ; 403 : ``{"error":"ip_blocked",...}``). La réponse 429 comporte l'en-tête ``Retry-After``
- Les limites sont appliquées par adresse IP
- Pour chaque IP, la fenêtre commence au premier requête et le compteur est réinitialisé après l'expiration de la période de la fenêtre (méthode de fenêtre fixe)
- Le dépassement de la limite entraîne le blocage de l'IP pendant la durée ``rate.limit.block.duration.ms``

Limitation de débit du mode de recherche IA
====================

La fonctionnalité de mode de recherche IA dispose d'une limitation de débit pour contrôler les coûts de l'API LLM et la consommation de ressources.
Le mode de recherche IA est soumis à la limitation de débit des requêtes HTTP décrite ci-dessus, et dispose également de paramètres de limitation de débit spécifiques au mode de recherche IA.

Pour la configuration spécifique de la limitation de débit du mode de recherche IA, consultez :doc:`rag-chat`.

.. note::
   La limitation de débit du mode de recherche IA s'applique séparément de la limitation de débit côté fournisseur LLM.
   Configurez en tenant compte des deux limites.

Limitation de débit du crawler
======================

Vous pouvez configurer l'intervalle entre les requêtes pour éviter que le crawler ne surcharge les sites cibles.

Configuration du crawl Web
---------------

Configurez les éléments suivants dans l'écran d'administration "Crawler" -> "Web" :

- **Intervalle de requêtes** : Temps d'attente entre les requêtes (millisecondes)
- **Nombre de threads** : Nombre de threads de crawl parallèles

Configuration recommandée :

::

    # Sites generaux
    intervalTime=1000
    numOfThread=1

    # Sites a grande echelle (avec autorisation)
    intervalTime=500
    numOfThread=3

Respect de robots.txt
----------------

|Fess| respecte par défaut la directive Crawl-delay de robots.txt.

::

    # Exemple de robots.txt
    User-agent: *
    Crawl-delay: 10

Le traitement de robots.txt est contrôlé par ``crawler.ignore.robots.txt`` dans
``app/WEB-INF/classes/fess_config.properties`` (défaut : ``false``).
En le définissant sur ``true``, le traitement de robots.txt, y compris Crawl-delay, est désactivé.

::

    # Ignorer robots.txt (defaut : false)
    crawler.ignore.robots.txt=false

Crawl-delay s'applique par origine et est plafonné à 60 secondes. Il espace les URL, pas les
requêtes : lors d'un crawl incrémental, le HEAD et le GET d'une même URL partent donc l'un après
l'autre. L'intervalle d'une configuration de crawl agit toujours séparément, comme attente avant
l'URL suivante.

robots.txt est interprété selon la RFC 9309. Entre ``Allow:`` et ``Disallow:``, la règle
correspondante la plus longue l'emporte, et les URL de départ sont elles aussi vérifiées. Une URL
interdite par robots.txt est journalisée au niveau INFO dans ``fess-crawler.log`` et n'est pas
enregistrée comme URL en échec.

Request-rate
------------

Depuis la version 15.10, |Fess| respecte aussi les lignes ``Request-rate`` et ``Visit-time`` de robots.txt (elles étaient ignorées jusqu'à la 15.9). Ni l'une ni l'autre ne fait partie de la RFC 9309 : toutes deux viennent de la `proposition étendue d'exclusion des robots <https://www.conman.org/people/spc/robots2.html>`__. SeznamBot utilise aussi Request-rate (`documentation de Seznam <https://www.napoveda.seznam.cz/en/crawling-control>`__). Comme Crawl-delay, elles ne s'appliquent que lorsque le traitement de robots.txt est activé : ``crawler.ignore.robots.txt=true`` désactive les trois, et il n'existe pas de réglage pour n'en désactiver qu'une seule. Ce ne sont pas des règles ``Allow:`` ou ``Disallow:`` : elles ne terminent jamais un groupe ``User-agent`` et ne changent jamais les URL interdites.

``Request-rate: <documents>/<durée>[ unité]`` demande à un robot de ne pas récupérer plus de documents que ce nombre pendant cette durée. L'unité de la durée est ``s`` (secondes, par défaut), ``m``, ``h`` ou ``d``. Exemples :

- ``1/10`` : une page toutes les 10 secondes
- ``10/10m`` : dix pages toutes les 10 minutes
- ``20/1h`` : vingt pages par heure
- ``100/15 m`` : cent pages toutes les 15 minutes

|Fess| convertit le débit en intervalle entre deux URL (``1/10`` vaut 10 secondes, ``5/1m`` vaut 12 secondes) et, pour chaque origine, attend avant l'URL suivante le plus long des intervalles de Crawl-delay et de Request-rate. La limite de 60 secondes s'applique aussi à cette attente : un débit plus lent, comme ``1/1h``, est ramené à 60 secondes. Request-rate espace les URL ; ce n'est pas un budget de rafale. Comme pour Crawl-delay, la première URL d'une origine n'est pas espacée, car robots.txt est lu pendant qu'elle est récupérée, et lors d'un crawl incrémental le HEAD et le GET d'une même URL partent l'un après l'autre.

Une plage horaire peut suivre le débit. Le débit ne s'applique alors que pendant cette plage ; en dehors, Request-rate n'impose aucune limite (Crawl-delay continue de s'appliquer) :

::

    User-agent: *
    Request-rate: 1/10 s 1800-1900

Les heures sont en UT/GMT (UTC), de 00:00 à 23:59, écrites ``HHMM-HHMM`` ou ``HH:MM-HH:MM``, bornes comprises. Une plage peut franchir minuit (``2300-0100``). Quand il y a plusieurs lignes Request-rate, toutes sont prises en compte et c'est la plus lente parmi celles qui sont actives à cet instant qui s'applique. Un débit ou une plage horaire mal formé (par exemple une heure supérieure à 23 ou une minute supérieure à 59) est ignoré.

Visit-time
----------

``Visit-time: HH:MM-HH:MM`` (``HHMM-HHMM`` est accepté aussi) demande à un robot de ne visiter le site que pendant cette plage horaire, en UTC, bornes comprises. Plusieurs lignes sont possibles ; la plage autorisée est alors leur union.

::

    User-agent: *
    Visit-time: 02:00-06:00

|Fess| n'attend pas l'ouverture de la plage, car cela immobiliserait un thread de crawl pendant des heures. Une URL de cette origine retirée de la file en dehors de la plage est ignorée, comme une URL interdite par ``Disallow:`` : elle est journalisée au niveau INFO une fois par origine, elle n'est pas remise dans la file (elle n'est pas réessayée plus tard dans le même crawl) et elle n'est pas comptée comme un échec. Le crawl doit donc démarrer dans la plage. Une URL de départ retirée de la file avant l'ouverture de la plage est perdue pour ce crawl, même si le crawl tourne encore quand la plage s'ouvre. Une ligne Visit-time mal formée est ignorée, ce qui équivaut à aucune restriction.

Si la tâche de crawl d'un site qui déclare Visit-time ne s'exécute jamais dans la plage, le site n'est pas crawlé et ses documents déjà indexés ne sont pas actualisés. Avec le réglage par défaut « Supprimer les anciens documents » (``day.for.cleanup``, 3 jours), ils expirent environ 3 jours après le dernier crawl qui les a atteints, comme lorsqu'un site est indisponible. Planifiez la tâche de crawl dans la plage.

Attente après les réponses 429/503
----------------------------------

Quand un serveur répond ``429 Too Many Requests`` ou ``503 Service Unavailable``, |Fess| suspend
les requêtes vers cette origine et réessaie l'URL jusqu'à trois fois. L'attente est la valeur de
l'en-tête ``Retry-After`` s'il est présent, sinon une attente exponentielle qui commence à
10 secondes (5 minutes au plus). Si la dernière tentative échoue aussi, un WARN est écrit dans
``fess-crawler.log``.

Quand robots.txt ne peut pas être récupéré
------------------------------------------

Quand la récupération de robots.txt échoue avec un 5xx, un 429 ou un délai dépassé, les URL de cette
origine sont remises dans la file jusqu'à la fin de l'attente. Si trois nouvelles tentatives
échouent après le premier échec, aucune URL de cette origine n'est crawlée jusqu'à la fin du crawl,
et un seul WARN est écrit dans ``fess-crawler.log``. Jusqu'à la version 15.8, un robots.txt
impossible à récupérer valait « tout autoriser ». Pour retrouver ce comportement, indiquez ceci dans
les « Paramètres de configuration » de la configuration de crawl web :

::

    client.robotsTxtAllowOnUnavailable=true

Pour désactiver entièrement le traitement de robots.txt, utilisez ``client.robotsTxtEnabled=false``
(par configuration de crawl) ou ``crawler.ignore.robots.txt=true``.

Liste complète des propriétés de limitation de débit
======================

Toutes les propriétés configurables dans ``app/WEB-INF/classes/fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriété
     - Description
     - Valeur par défaut
   * - ``rate.limit.enabled``
     - Activer la limitation de débit
     - ``false``
   * - ``rate.limit.requests.per.window``
     - Nombre maximum de requêtes par fenêtre
     - ``100``
   * - ``rate.limit.window.ms``
     - Taille de la fenêtre (millisecondes)
     - ``60000``
   * - ``rate.limit.block.duration.ms``
     - Durée de blocage de l'IP en cas de dépassement (millisecondes)
     - ``300000``
   * - ``rate.limit.retry.after.seconds``
     - Valeur de l'en-tête Retry-After (secondes)
     - ``60``
   * - ``rate.limit.whitelist.ips``
     - Adresses IP exclues de la limitation de débit (séparées par des virgules)
     - ``127.0.0.1,::1``
   * - ``rate.limit.blocked.ips``
     - Adresses IP à bloquer (séparées par des virgules)
     - (vide)
   * - ``rate.limit.trusted.proxies``
     - IP de proxies de confiance (pour obtenir l'IP client via X-Forwarded-For/X-Real-IP ; également utilisées pour l'IP client du journal d'audit et du journal de recherche)
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - Intervalle de nettoyage (nombre de requêtes, réservé)
     - ``1000``

.. note::
   ``rate.limit.cleanup.interval`` est un paramètre réservé pour une utilisation future.
   Dans l'implémentation actuelle, les compteurs de requêtes et les informations sur les IP bloquées
   sont nettoyés automatiquement en fonction de l'expiration du cache interne
   (``rate.limit.window.ms`` et ``rate.limit.block.duration.ms``),
   de sorte que cette valeur n'est pas utilisée.

Limitation des tentatives de connexion
======================================

La connexion dispose de sa propre limitation, distincte de la précédente et configurée avec ``theme.api.login.*``.
Depuis la 15.10, ``/api/v2/auth/login`` et le formulaire de connexion de l'écran de connexion (``/login/``) partagent la même limite et le même verrouillage.
Chaque tentative consomme une place du quota par minute de l'IP client (valeur par défaut ``10``), et cette place est restituée lorsque la connexion réussit.
Lorsque les tentatives d'une même adresse IP dépassent la limite, cette adresse IP est verrouillée pendant ``theme.api.login.lockout.seconds`` (valeur par défaut ``900``) secondes, et même des identifiants corrects ne permettent pas de se connecter pendant ce temps.
Par conséquent, si une même adresse IP effectue plus de tentatives que la limite (par exemple des connexions simultanées) avant qu'une seule réussisse, cette adresse est verrouillée.
La limite par utilisateur (``theme.api.login.rate.limit.per.user.per.minute``) est comptée pour chaque couple adresse IP du client et nom d'utilisateur. Les noms d'utilisateur sont comparés sans tenir compte de la casse : ``alice`` et ``Alice`` partagent donc un seul compteur. Le nom d'utilisateur utilisé pour l'authentification et écrit dans les journaux reste celui qui a été saisi.
Voir :doc:`../api/api-auth` pour plus de détails.

Configuration avancée de limitation de débit
====================

Limitation de débit personnalisée
------------------

Pour appliquer des limites différentes selon des conditions spécifiques,
une implémentation de composant personnalisé est nécessaire.

::

    // Exemple de personnalisation de RateLimitHelper
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean allowRequest(String ip) {
            // Logique personnalisee
        }
    }

Configuration d'exclusion
========

Vous pouvez exclure certaines adresses IP de la limitation de débit ou les bloquer.

::

    # IP en liste blanche (exclues de la limitation de debit, separees par des virgules)
    rate.limit.whitelist.ips=127.0.0.1,::1,192.168.1.100

    # IP bloquees (toujours bloquees, separees par des virgules)
    rate.limit.blocked.ips=203.0.113.50

    # IP de proxies de confiance (separees par des virgules)
    rate.limit.trusted.proxies=127.0.0.1,::1

.. note::
   Si vous utilisez un reverse proxy, configurez l'adresse IP du proxy dans ``rate.limit.trusted.proxies``.
   Seules les requêtes provenant de proxies de confiance permettent d'obtenir l'IP client
   via les en-têtes X-Forwarded-For et X-Real-IP.
   Lorsque X-Forwarded-For est réparti sur plusieurs lignes d'en-tête (par exemple lorsqu'un proxy ajoute sa
   propre ligne, comme le fait ``option forwardfor`` de HAProxy), la version 15.10 et les suivantes joignent
   toutes les lignes dans l'ordre de réception, lisent la chaîne de droite à gauche et utilisent comme IP du
   client la première adresse qui n'est pas un proxy de confiance. Jusqu'à la version 15.9, seule la première
   ligne, celle envoyée par le client, était lue.

Surveillance et alertes
==============

Configuration pour surveiller l'état de la limitation de débit :

Sortie de logs
--------

Lorsque la limitation de débit est appliquée, elle est enregistrée dans les logs :

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

Le message est enregistré au niveau INFO ; il n'est donc pas écrit avec le niveau de log par défaut (``warn``). Ajoutez le ``Logger`` ci-dessus à ``log4j2.xml`` (emplacement : voir :doc:`admin-logging`) ou définissez ``FESS_LOG_LEVEL`` à ``info``.

Dépannage
======================

Les requêtes légitimes sont bloquées
--------------------------------

**Cause** : Les valeurs limites sont trop strictes

**Solution** :

1. Augmenter ``rate.limit.requests.per.window``
2. Ajouter des IP spécifiques à la liste blanche (``rate.limit.whitelist.ips``)
3. Ajuster la taille de la fenêtre (``rate.limit.window.ms``)

La limitation de débit ne fonctionne pas
--------------------

**Cause** : La configuration n'est pas correctement appliquée

**Points à vérifier** :

1. Vérifier si ``rate.limit.enabled=true`` est configuré
2. Vérifier si le fichier de configuration est correctement lu
3. Vérifier si |Fess| a été redémarré

Impact sur les performances
----------------------

Si la vérification de la limitation de débit affecte les performances :

1. Utiliser la liste blanche pour ignorer les vérifications sur les IP de confiance
2. Désactiver la limitation de débit (``rate.limit.enabled=false``)

Informations de référence
========

- :doc:`rag-chat` - Configuration de la fonctionnalité de mode de recherche IA
- :doc:`../admin/webconfig-guide` - Guide de configuration du crawl Web
- :doc:`../api/api-overview` - Aperçu des API
