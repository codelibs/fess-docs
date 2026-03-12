==================================
Configuration de la limitation de debit
==================================

Apercu
====

|Fess| dispose d'une fonctionnalite de limitation de debit pour maintenir la stabilite et les performances du systeme.
Cette fonctionnalite protege le systeme contre les requetes excessives et permet une allocation equitable des ressources.

La limitation de debit s'applique dans les situations suivantes :

- Toutes les requetes HTTP, y compris l'API de recherche, l'API de mode IA et les pages d'administration (``RateLimitFilter``)
- Requetes du crawler (controlees par la configuration du crawl)

Limitation de debit des requetes HTTP
======================================

Vous pouvez limiter le nombre de requetes HTTP vers |Fess| par adresse IP.
Cette limitation s'applique a toutes les requetes HTTP, y compris l'API de recherche, l'API de mode IA, les pages d'administration, etc.

Configuration
----

``app/WEB-INF/conf/fess_config.properties`` :

::

    # Activer la limitation de debit (defaut: false)
    rate.limit.enabled=true

    # Nombre maximum de requetes par fenetre par adresse IP (defaut: 100)
    rate.limit.requests.per.window=100

    # Taille de la fenetre de limitation de debit (millisecondes) (defaut: 60000)
    rate.limit.window.ms=60000

Comportement
----

- Les requetes depassant la limite de debit retournent HTTP 429 (Too Many Requests)
- Les requetes provenant d'IP figurant dans la liste de blocage retournent HTTP 403 (Forbidden)
- Les limites sont appliquees par adresse IP
- Pour chaque IP, la fenetre commence au premier requete et le compteur est reinitialise apres l'expiration de la periode de la fenetre (methode de fenetre fixe)
- Le depassement de la limite entraine le blocage de l'IP pendant la duree ``rate.limit.block.duration.ms``

Limitation de debit du mode IA
====================

La fonctionnalite de mode IA dispose d'une limitation de debit pour controler les couts de l'API LLM et la consommation de ressources.
Le mode IA est soumis a la limitation de debit des requetes HTTP decrite ci-dessus, et dispose egalement de parametres de limitation de debit specifiques au mode IA.

Pour la configuration specifique de la limitation de debit du mode IA, consultez :doc:`rag-chat`.

.. note::
   La limitation de debit du mode IA s'applique separement de la limitation de debit cote fournisseur LLM.
   Configurez en tenant compte des deux limites.

Limitation de debit du crawler
======================

Vous pouvez configurer l'intervalle entre les requetes pour eviter que le crawler ne surcharge les sites cibles.

Configuration du crawl Web
---------------

Configurez les elements suivants dans l'ecran d'administration "Crawler" -> "Web" :

- **Intervalle de requetes** : Temps d'attente entre les requetes (millisecondes)
- **Nombre de threads** : Nombre de threads de crawl paralleles

Configuration recommandee :

::

    # Sites generaux
    intervalTime=1000
    numOfThread=1

    # Sites a grande echelle (avec autorisation)
    intervalTime=500
    numOfThread=3

Respect de robots.txt
----------------

|Fess| respecte par defaut la directive Crawl-delay de robots.txt.

::

    # Exemple de robots.txt
    User-agent: *
    Crawl-delay: 10

Liste complete des proprietes de limitation de debit
======================

Toutes les proprietes configurables dans ``app/WEB-INF/conf/fess_config.properties``.

.. list-table::
   :header-rows: 1
   :widths: 35 45 20

   * - Propriete
     - Description
     - Valeur par defaut
   * - ``rate.limit.enabled``
     - Activer la limitation de debit
     - ``false``
   * - ``rate.limit.requests.per.window``
     - Nombre maximum de requetes par fenetre
     - ``100``
   * - ``rate.limit.window.ms``
     - Taille de la fenetre (millisecondes)
     - ``60000``
   * - ``rate.limit.block.duration.ms``
     - Duree de blocage de l'IP en cas de depassement (millisecondes)
     - ``300000``
   * - ``rate.limit.retry.after.seconds``
     - Valeur de l'en-tete Retry-After (secondes)
     - ``60``
   * - ``rate.limit.whitelist.ips``
     - Adresses IP exclues de la limitation de debit (separees par des virgules)
     - ``127.0.0.1,::1``
   * - ``rate.limit.blocked.ips``
     - Adresses IP a bloquer (separees par des virgules)
     - (vide)
   * - ``rate.limit.trusted.proxies``
     - IP de proxies de confiance (pour obtenir l'IP client via X-Forwarded-For/X-Real-IP)
     - ``127.0.0.1,::1``
   * - ``rate.limit.cleanup.interval``
     - Intervalle de nettoyage pour prevenir les fuites memoire (nombre de requetes)
     - ``1000``

Configuration avancee de limitation de debit
====================

Limitation de debit personnalisee
------------------

Pour appliquer des limites differentes selon des conditions specifiques,
une implementation de composant personnalise est necessaire.

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

Vous pouvez exclure certaines adresses IP de la limitation de debit ou les bloquer.

::

    # IP en liste blanche (exclues de la limitation de debit, separees par des virgules)
    rate.limit.whitelist.ips=127.0.0.1,::1,192.168.1.100

    # IP bloquees (toujours bloquees, separees par des virgules)
    rate.limit.blocked.ips=203.0.113.50

    # IP de proxies de confiance (separees par des virgules)
    rate.limit.trusted.proxies=127.0.0.1,::1

.. note::
   Si vous utilisez un reverse proxy, configurez l'adresse IP du proxy dans ``rate.limit.trusted.proxies``.
   Seules les requetes provenant de proxies de confiance permettent d'obtenir l'IP client
   via les en-tetes X-Forwarded-For et X-Real-IP.

Surveillance et alertes
==============

Configuration pour surveiller l'etat de la limitation de debit :

Sortie de logs
--------

Lorsque la limitation de debit est appliquee, elle est enregistree dans les logs :

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

Depannage
======================

Les requetes legitimes sont bloquees
--------------------------------

**Cause** : Les valeurs limites sont trop strictes

**Solution** :

1. Augmenter ``rate.limit.requests.per.window``
2. Ajouter des IP specifiques a la liste blanche (``rate.limit.whitelist.ips``)
3. Ajuster la taille de la fenetre (``rate.limit.window.ms``)

La limitation de debit ne fonctionne pas
--------------------

**Cause** : La configuration n'est pas correctement appliquee

**Points a verifier** :

1. Verifier si ``rate.limit.enabled=true`` est configure
2. Verifier si le fichier de configuration est correctement lu
3. Verifier si |Fess| a ete redemarre

Impact sur les performances
----------------------

Si la verification de la limitation de debit affecte les performances :

1. Utiliser la liste blanche pour ignorer les verifications sur les IP de confiance
2. Desactiver la limitation de debit (``rate.limit.enabled=false``)

Informations de reference
========

- :doc:`rag-chat` - Configuration de la fonctionnalite de mode IA
- :doc:`../admin/webconfig-guide` - Guide de configuration du crawl Web
- :doc:`../api/api-overview` - Apercu des API
