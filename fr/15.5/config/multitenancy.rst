==================================
Configuration multi-tenant
==================================

Apercu
====

La fonctionnalite multi-tenant de |Fess| permet d'exploiter plusieurs tenants
(organisations, departements, clients, etc.) de maniere isolee avec une seule instance de |Fess|.

En utilisant la fonctionnalite d'hote virtuel, vous pouvez fournir pour chaque tenant :

- Une interface de recherche independante
- Du contenu isole
- Un design personnalise

Fonctionnalite d'hote virtuel
==============

L'hote virtuel est une fonctionnalite qui fournit differents environnements de recherche bases sur le nom d'hote de la requete HTTP.

Fonctionnement
------

1. L'utilisateur accede a ``tenant1.example.com``
2. |Fess| identifie le nom d'hote
3. Applique la configuration de l'hote virtuel correspondant
4. Affiche le contenu et l'interface specifiques au tenant

Configuration de l'hote virtuel
================

Configuration via l'ecran d'administration
----------------

1. Connectez-vous a l'ecran d'administration
2. Allez dans "Crawler" -> "Hotes virtuels"
3. Cliquez sur "Nouveau"
4. Configurez les elements suivants :

   - **Nom d'hote** : ``tenant1.example.com``
   - **Chemin** : ``/tenant1`` (optionnel)

Integration avec la configuration du crawl
--------------------

Vous pouvez isoler le contenu en specifiant l'hote virtuel dans la configuration du crawl Web :

1. Creez une configuration de crawl dans "Crawler" -> "Web"
2. Selectionnez l'hote virtuel cible dans le champ "Hote virtuel"
3. Le contenu crawle avec cette configuration ne sera recherchable que sur l'hote virtuel specifie

Controle d'acces
============

Combinaison d'hote virtuel et de roles
------------------------------

En combinant les hotes virtuels avec le controle d'acces base sur les roles,
un controle d'acces plus granulaire est possible :

::

    # Exemple de configuration
    virtual.host=tenant1.example.com
    permissions=role_tenant1_user

Recherche basee sur les roles
----------------

Pour plus de details, consultez :doc:`security-role`.

Personnalisation de l'interface
==============

Vous pouvez personnaliser l'interface pour chaque hote virtuel.

Application de themes
------------

Appliquer differents themes par hote virtuel :

1. Configurez le theme dans "Systeme" -> "Design"
2. Specifiez le theme dans la configuration de l'hote virtuel

CSS personnalise
-----------

Appliquer un CSS personnalise par hote virtuel :

::

    # Fichier CSS specifique a l'hote virtuel
    /webapp/WEB-INF/view/tenant1/css/custom.css

Configuration des labels
----------

Limiter les labels affiches par hote virtuel :

1. Specifiez l'hote virtuel dans la configuration du type de label
2. Le label ne sera affiche que sur l'hote virtuel specifie

Authentification API
=======

Controler l'acces API par hote virtuel :

Jetons d'acces
----------------

Emettre des jetons d'acces lies a un hote virtuel :

1. Creez un jeton dans "Systeme" -> "Jetons d'acces"
2. Associez le jeton a l'hote virtuel

Requete API
-------------

::

    curl -H "Authorization: Bearer TENANT_TOKEN" \
         "https://tenant1.example.com/api/v1/search?q=keyword"

Configuration DNS
=======

Exemple de configuration DNS pour realiser le multi-tenant :

Sous-domaines vers le meme serveur
----------------------------

::

    # Configuration DNS
    tenant1.example.com    A    192.168.1.100
    tenant2.example.com    A    192.168.1.100

    # Ou avec un joker
    *.example.com          A    192.168.1.100

Configuration de reverse proxy
--------------------

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

Isolation des donnees
==========

Si une isolation complete des donnees est necessaire, considerez les approches suivantes :

Isolation au niveau de l'index
------------------------

Utiliser des index separes pour chaque tenant :

::

    # Index pour le tenant 1
    index.document.search.index=fess_tenant1.search

    # Index pour le tenant 2
    index.document.search.index=fess_tenant2.search

.. note::
   L'isolation au niveau de l'index peut necessiter une implementation personnalisee.

Bonnes pratiques
==================

1. **Convention de nommage claire** : Utiliser une convention de nommage coherente pour les hotes virtuels et les roles
2. **Tests** : Tester suffisamment le fonctionnement de chaque tenant
3. **Surveillance** : Surveiller l'utilisation des ressources par tenant
4. **Documentation** : Documenter la configuration des tenants

Limitations
========

- L'ecran d'administration est partage entre tous les tenants
- Les parametres systeme affectent tous les tenants
- Certaines fonctionnalites peuvent ne pas etre compatibles avec les hotes virtuels

Informations de reference
========

- :doc:`security-role` - Controle d'acces base sur les roles
- :doc:`security-virtual-host` - Details de la configuration des hotes virtuels
- :doc:`../admin/design-guide` - Personnalisation du design
