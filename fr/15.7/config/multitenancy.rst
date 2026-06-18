============================================
Configuration multi-locataire (multi-tenant)
============================================

Aperçu
======

La fonctionnalité multi-locataire de |Fess| permet d'exploiter plusieurs locataires
(organisations, départements, clients, etc.) de manière isolée avec une seule instance de |Fess|.

En utilisant la fonctionnalité d'hôte virtuel, vous pouvez fournir pour chaque locataire :

- Une interface de recherche indépendante
- Du contenu isolé
- Un design personnalisé

L'hôte virtuel courant se reflète dans les résultats de recherche, les labels, le contenu associé,
les requêtes associées, le design (thème), et les autres fonctionnalités de |Fess|.

Fonctionnalité d'hôte virtuel
==============================

L'hôte virtuel est une fonctionnalité qui fournit différents environnements de recherche
en fonction du nom d'hôte de la requête HTTP.

Fonctionnement
--------------

1. L'utilisateur accède à ``tenant1.example.com``
2. |Fess| identifie le nom d'hôte
3. Applique la configuration de l'hôte virtuel correspondant
4. Affiche le contenu et l'interface spécifiques au locataire

Configuration des en-têtes d'hôte virtuel
==========================================

Pour activer la fonctionnalité d'hôte virtuel, configurez la correspondance entre les en-têtes
de la requête HTTP et les clés d'hôte virtuel. Deux méthodes sont disponibles :

- **Écran d'administration (recommandé)** : Renseignez le champ « Hôte virtuel » dans « Système » → « Général ».
  Cette valeur est enregistrée comme paramètre système et conservée après redémarrage. Elle a priorité
  sur ``virtual.host.headers`` dans ``fess_config.properties``.
- **Fichier de configuration** : Définissez la propriété ``virtual.host.headers``
  dans ``fess_config.properties``.

Quelle que soit la méthode choisie, le format de la valeur est identique.

Format de configuration
-----------------------

Spécifiez chaque entrée au format ``NomEnTête:ValeurEnTête=CléHôteVirtuel``, une par ligne :

::

    # fess_config.properties
    virtual.host.headers=Host:tenant1.example.com=tenant1\n\
    Host:tenant2.example.com=tenant2

Pour plusieurs hôtes virtuels, séparez les entrées par des retours à la ligne.

Comportement de la correspondance
----------------------------------

À chaque requête reçue, |Fess| compare la valeur de l'en-tête dont le nom correspond à chaque
ligne configurée avec la valeur d'en-tête définie dans cette ligne.

- La comparaison des valeurs d'en-tête est insensible à la casse.
- Les lignes sont évaluées de haut en bas ; la clé d'hôte virtuel de la première ligne correspondante est appliquée.
- Si aucune ligne ne correspond, la requête est traitée sans hôte virtuel (environnement commun).
- Le résultat de l'évaluation est mis en cache par requête.

Restrictions des clés d'hôte virtuel
--------------------------------------

Les clés d'hôte virtuel ont les restrictions suivantes :

- Seuls les caractères alphanumériques et les underscores (``a-zA-Z0-9_``) sont autorisés. Les autres caractères sont automatiquement supprimés.
- Les noms de clés suivants sont réservés et ne peuvent pas être utilisés : ``admin``, ``common``, ``error``, ``login``, ``profile``

Configuration via l'écran d'administration
==========================================

Configuration du crawl
-----------------------

Vous pouvez isoler le contenu en spécifiant l'hôte virtuel dans la configuration du crawl Web :

1. Connectez-vous à l'écran d'administration
2. Créez une configuration de crawl dans « Crawler » → « Web »
3. Sélectionnez la clé d'hôte virtuel configurée dans le champ « Hôte virtuel » (sélection multiple possible)
4. Le contenu crawlé avec cette configuration ne sera recherchable que sur l'hôte virtuel spécifié

.. note::
   Le champ « Hôte virtuel » est disponible dans les configurations de crawl Web, système de fichiers
   et datastore. La clé d'hôte virtuel sélectionnée ici est associée à chaque document crawlé
   et est utilisée pour filtrer les résultats lors de la recherche selon l'hôte virtuel courant.

Contrôle d'accès
================

Combinaison d'hôte virtuel et de rôles
---------------------------------------

En combinant les hôtes virtuels avec le contrôle d'accès basé sur les rôles,
un contrôle d'accès plus granulaire est possible.

Configurez l'hôte virtuel et les permissions ensemble dans la configuration du crawl :

::

    # Hôte virtuel dans la configuration du crawl
    tenant1

    # Permissions dans la configuration du crawl
    {role}tenant1_user

Recherche basée sur les rôles
------------------------------

Pour plus de détails, consultez :doc:`security-role`.

Personnalisation de l'interface
================================

Vous pouvez personnaliser l'interface pour chaque hôte virtuel.

Application de thèmes
----------------------

Appliquer différents thèmes par hôte virtuel :

1. Configurez le thème dans « Système » → « Design »
2. Spécifiez le thème dans la configuration de l'hôte virtuel

CSS personnalisé
----------------

Pour appliquer un CSS personnalisé par hôte virtuel, éditez les fichiers CSS dans l'écran
d'administration sous « Système » → « Design ». Vous pouvez également placer des templates
personnalisés dans le répertoire de vue correspondant à la clé de l'hôte virtuel.

Configuration des labels
-------------------------

Limiter les labels affichés par hôte virtuel :

1. Spécifiez l'hôte virtuel dans la configuration du type de label
2. Le label ne sera affiché que sur l'hôte virtuel spécifié

Accès via l'API
===============

Les requêtes à l'API de recherche voient également leur hôte virtuel déterminé par le nom d'hôte
de la requête (l'en-tête configuré, généralement l'en-tête ``Host``), de la même façon que
pour l'interface utilisateur. Par exemple, une requête destinée à ``tenant1.example.com`` est
automatiquement limitée à l'hôte virtuel ``tenant1``, et seul le contenu de cet hôte virtuel
est inclus dans les résultats de recherche.

Requête API
-----------

::

    curl "https://tenant1.example.com/api/v2/search?q=keyword"

Pour s'authentifier avec un jeton d'accès, spécifiez-le dans l'en-tête ``Authorization``
au format ``Bearer`` :

::

    curl -H "Authorization: Bearer YOUR_TOKEN" \
         "https://tenant1.example.com/api/v2/search?q=keyword"

.. note::
   Les jetons d'accès ne sont pas liés à un hôte virtuel particulier. Un jeton est valide
   pour tous les hôtes virtuels ; l'hôte virtuel ciblé est déterminé par le nom d'hôte de
   destination de la requête. Envoyer le même jeton vers un nom d'hôte différent le rattache
   à un autre hôte virtuel. Si vous souhaitez contrôler la portée d'accès indépendamment
   de l'hôte virtuel, combinez cette fonctionnalité avec le contrôle d'accès basé sur les
   rôles (:doc:`security-role`).

Configuration DNS
=================

Exemple de configuration DNS pour réaliser le multi-locataire :

Sous-domaines vers le même serveur
------------------------------------

::

    # Configuration DNS
    tenant1.example.com    A    192.168.1.100
    tenant2.example.com    A    192.168.1.100

    # Ou avec un joker
    *.example.com          A    192.168.1.100

Configuration de reverse proxy
--------------------------------

Exemple de configuration de reverse proxy avec Nginx :

::

    server {
        server_name tenant1.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

    server {
        server_name tenant2.example.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

Isolation des données
=====================

Si une isolation complète des données est nécessaire, envisagez les approches suivantes :

Isolation au niveau de l'index
--------------------------------

Utiliser des instances et des index |Fess| séparés pour chaque locataire :

::

    # Instance Fess du locataire 1 (fess_config.properties)
    index.document.search.index=fess_tenant1.search

    # Instance Fess du locataire 2 (fess_config.properties)
    index.document.search.index=fess_tenant2.search

.. note::
   ``index.document.search.index`` ne peut être défini qu'à une seule valeur par instance.
   Pour une isolation complète au niveau de l'index, vous devez exécuter des instances |Fess| séparées
   par locataire ou implémenter du code personnalisé. Pour un multi-locataire classique,
   l'isolation logique via la fonctionnalité d'hôte virtuel est suffisante.

Bonnes pratiques
================

1. **Convention de nommage claire** : Utiliser une convention de nommage cohérente pour les hôtes virtuels et les rôles
2. **Tests** : Tester suffisamment le fonctionnement de chaque locataire
3. **Surveillance** : Surveiller l'utilisation des ressources par locataire
4. **Documentation** : Documenter la configuration des locataires

Limitations
===========

- L'écran d'administration est partagé entre tous les locataires
- Les paramètres système affectent tous les locataires
- Certaines fonctionnalités peuvent ne pas être compatibles avec les hôtes virtuels

Informations de référence
==========================

- :doc:`security-role` - Contrôle d'accès basé sur les rôles
- :doc:`security-virtual-host` - Détails de la configuration des hôtes virtuels
- :doc:`../admin/design-guide` - Personnalisation du design
