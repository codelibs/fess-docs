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

Configuration des en-tetes d'hote virtuel
==========================================

Pour activer la fonctionnalite d'hote virtuel, configurez la propriete ``virtual.host.headers``.
Cette propriete est definie dans ``fess_config.properties``.

Format de configuration
-----------------------

Specifiez chaque entree au format ``NomEnTete:ValeurEnTete=CleHoteVirtuel``, une par ligne :

::

    # fess_config.properties
    virtual.host.headers=Host:tenant1.example.com=tenant1\n\
    Host:tenant2.example.com=tenant2

Pour plusieurs hotes virtuels, separez les entrees par des retours a la ligne.

Restrictions des cles d'hote virtuel
-------------------------------------

Les cles d'hote virtuel ont les restrictions suivantes :

- Seuls les caracteres alphanumeriques et les underscores (``a-zA-Z0-9_``) sont autorises. Les autres caracteres sont automatiquement supprimes.
- Les noms de cles suivants sont reserves et ne peuvent pas etre utilises : ``admin``, ``common``, ``error``, ``login``, ``profile``

Configuration via l'ecran d'administration
==========================================

Configuration du crawl
----------------------

Vous pouvez isoler le contenu en specifiant l'hote virtuel dans la configuration du crawl Web :

1. Connectez-vous a l'ecran d'administration
2. Creez une configuration de crawl dans "Crawler" -> "Web"
3. Selectionnez une cle d'hote virtuel definie dans ``virtual.host.headers`` dans le champ "Hote virtuel"
4. Le contenu crawle avec cette configuration ne sera recherchable que sur l'hote virtuel specifie

Controle d'acces
============

Combinaison d'hote virtuel et de roles
------------------------------

En combinant les hotes virtuels avec le controle d'acces base sur les roles,
un controle d'acces plus granulaire est possible :

Configurez l'hote virtuel et les permissions ensemble dans la configuration du crawl :

::

    # Hote virtuel dans la configuration du crawl
    tenant1

    # Permissions dans la configuration du crawl
    {role}tenant1_user

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

Pour appliquer un CSS personnalise par hote virtuel, editez les fichiers CSS dans l'ecran d'administration sous "Systeme" -> "Design". Vous pouvez egalement placer des templates personnalises dans le repertoire de vue correspondant a la cle de l'hote virtuel.

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

Utiliser des instances et des index |Fess| separes pour chaque tenant :

::

    # Instance Fess du tenant 1 (fess_config.properties)
    index.document.search.index=fess_tenant1.search

    # Instance Fess du tenant 2 (fess_config.properties)
    index.document.search.index=fess_tenant2.search

.. note::
   ``index.document.search.index`` ne peut etre defini qu'a une seule valeur par instance.
   Pour une isolation complete au niveau de l'index, vous devez executer des instances |Fess| separees par tenant
   ou implementer du code personnalise. Pour un multi-tenant classique, l'isolation logique via la fonctionnalite d'hote virtuel est suffisante.

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
