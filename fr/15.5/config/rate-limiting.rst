==================================
Configuration de la limitation de debit
==================================

Apercu
====

|Fess| dispose d'une fonctionnalite de limitation de debit pour maintenir la stabilite et les performances du systeme.
Cette fonctionnalite protege le systeme contre les requetes excessives et permet une allocation equitable des ressources.

La limitation de debit s'applique dans les situations suivantes :

- API de recherche
- API de chat RAG
- Requetes du crawler

Limitation de debit de l'API de recherche
===================

Vous pouvez limiter le nombre de requetes vers l'API de recherche.

Configuration
----

``app/WEB-INF/conf/system.properties`` :

::

    # Activer la limitation de debit
    api.rate.limit.enabled=true

    # Nombre maximum de requetes par minute par adresse IP
    api.rate.limit.requests.per.minute=60

    # Taille de la fenetre de limitation de debit (secondes)
    api.rate.limit.window.seconds=60

Comportement
----

- Les requetes depassant la limite de debit retournent HTTP 429 (Too Many Requests)
- Les limites sont appliquees par adresse IP
- Les valeurs limites sont comptees avec une methode de fenetre glissante

Limitation de debit du chat RAG
=======================

La fonctionnalite de chat RAG dispose d'une limitation de debit pour controler les couts de l'API LLM et la consommation de ressources.

Configuration
----

``app/WEB-INF/conf/system.properties`` :

::

    # Activer la limitation de debit du chat
    rag.chat.rate.limit.enabled=true

    # Nombre maximum de requetes par minute
    rag.chat.rate.limit.requests.per.minute=10

.. note::
   La limitation de debit du chat RAG s'applique separement de la limitation de debit cote fournisseur LLM.
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

Configuration avancee de limitation de debit
====================

Limitation de debit personnalisee
------------------

Pour appliquer des limites differentes pour des utilisateurs ou roles specifiques,
une implementation de composant personnalise est necessaire.

::

    // Exemple de personnalisation de RateLimitHelper
    public class CustomRateLimitHelper extends RateLimitHelper {
        @Override
        public boolean isAllowed(String key) {
            // Logique personnalisee
        }
    }

Limitation de rafale
------------

Configuration pour tolerer les pics de requetes a court terme tout en empechant une charge elevee continue :

::

    # Capacite de rafale autorisee
    api.rate.limit.burst.size=20

    # Limite soutenue
    api.rate.limit.sustained.requests.per.second=1

Configuration d'exclusion
========

Vous pouvez exclure certaines adresses IP ou utilisateurs de la limitation de debit.

::

    # Adresses IP exclues (separees par des virgules)
    api.rate.limit.excluded.ips=192.168.1.100,10.0.0.0/8

    # Roles exclus
    api.rate.limit.excluded.roles=admin

Surveillance et alertes
==============

Configuration pour surveiller l'etat de la limitation de debit :

Sortie de logs
--------

Lorsque la limitation de debit est appliquee, elle est enregistree dans les logs :

::

    <Logger name="org.codelibs.fess.helper.RateLimitHelper" level="INFO"/>

Metriques
----------

Les metriques de limitation de debit peuvent etre obtenues via l'API de statistiques systeme :

::

    GET /api/admin/stats

Depannage
======================

Les requetes legitimes sont bloquees
--------------------------------

**Cause** : Les valeurs limites sont trop strictes

**Solution** :

1. Augmenter ``requests.per.minute``
2. Ajouter des IP specifiques a la liste d'exclusion
3. Ajuster la taille de la fenetre

La limitation de debit ne fonctionne pas
--------------------

**Cause** : La configuration n'est pas correctement appliquee

**Points a verifier** :

1. Verifier si ``api.rate.limit.enabled=true`` est configure
2. Verifier si le fichier de configuration est correctement lu
3. Verifier si |Fess| a ete redemarre

Impact sur les performances
----------------------

Si la verification de la limitation de debit affecte les performances :

1. Changer le stockage de limitation de debit vers Redis ou similaire
2. Ajuster la frequence des verifications

Informations de reference
========

- :doc:`rag-chat` - Configuration de la fonctionnalite de chat RAG
- :doc:`../admin/webconfig-guide` - Guide de configuration du crawl Web
- :doc:`../api/api-overview` - Apercu des API
