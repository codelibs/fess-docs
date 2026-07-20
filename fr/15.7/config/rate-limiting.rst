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
- Les requêtes provenant d'IP figurant dans la liste de blocage retournent HTTP 403 (Forbidden)
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
     - IP de proxies de confiance (pour obtenir l'IP client via X-Forwarded-For/X-Real-IP)
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

Surveillance et alertes
==============

Configuration pour surveiller l'état de la limitation de débit :

Sortie de logs
--------

Lorsque la limitation de débit est appliquée, elle est enregistrée dans les logs :

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

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
