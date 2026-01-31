==========================
API Documents
==========================

Vue d'ensemble
==============

L'API Documents permet de gerer les documents dans l'index de |Fess|.
Vous pouvez effectuer des operations telles que la suppression en masse, la mise a jour et la recherche de documents.

URL de base
===========

::

    /api/admin/documents

Liste des endpoints
===================

.. list-table::
   :header-rows: 1
   :widths: 15 35 50

   * - Methode
     - Chemin
     - Description
   * - DELETE
     - /
     - Suppression de documents (par requete)
   * - DELETE
     - /{id}
     - Suppression de documents (par ID)

Suppression de documents par requete
====================================

Supprime en masse les documents correspondant a une requete de recherche.

Requete
-------

::

    DELETE /api/admin/documents

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``q``
     - String
     - Oui
     - Requete de recherche pour les documents a supprimer

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0,
        "deleted": 150
      }
    }

Exemples d'utilisation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Supprimer les documents d'un site specifique
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=url:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Supprimer les anciens documents
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO 2023-01-01]" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Supprimer les documents par label
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=label:old_label" \
         -H "Authorization: Bearer YOUR_TOKEN"

Suppression de documents par ID
===============================

Supprime un document en specifiant son ID.

Requete
-------

::

    DELETE /api/admin/documents/{id}

Parametres
~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 15 15 50

   * - Parametre
     - Type
     - Requis
     - Description
   * - ``id``
     - String
     - Oui
     - ID du document (parametre de chemin)

Reponse
-------

.. code-block:: json

    {
      "response": {
        "status": 0
      }
    }

Exemples d'utilisation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    curl -X DELETE "http://localhost:8080/api/admin/documents/doc_id_12345" \
         -H "Authorization: Bearer YOUR_TOKEN"

Syntaxe des requetes
====================

Les requetes de suppression peuvent utiliser la syntaxe de recherche standard de |Fess|.

Requetes de base
----------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Exemple de requete
     - Description
   * - ``url:example.com``
     - Documents contenant "example.com" dans l'URL
   * - ``url:https://example.com/*``
     - URLs avec un prefixe specifique
   * - ``host:example.com``
     - Documents d'un hote specifique
   * - ``title:keyword``
     - Documents contenant un mot-cle dans le titre
   * - ``content:keyword``
     - Documents contenant un mot-cle dans le contenu
   * - ``label:mylabel``
     - Documents avec un label specifique

Requetes sur les plages de dates
--------------------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Exemple de requete
     - Description
   * - ``lastModified:[2023-01-01 TO 2023-12-31]``
     - Documents mis a jour dans la periode specifiee
   * - ``lastModified:[* TO 2023-01-01]``
     - Documents mis a jour avant la date specifiee
   * - ``created:[2024-01-01 TO *]``
     - Documents crees apres la date specifiee

Requetes composees
------------------

.. list-table::
   :header-rows: 1
   :widths: 40 60

   * - Exemple de requete
     - Description
   * - ``url:example.com AND label:blog``
     - Condition AND
   * - ``url:example.com OR url:sample.com``
     - Condition OR
   * - ``NOT url:example.com``
     - Condition NOT
   * - ``(url:example.com OR url:sample.com) AND label:news``
     - Regroupement

Notes importantes
=================

Precautions concernant les suppressions
---------------------------------------

.. warning::
   Les operations de suppression sont irreversibles. Testez toujours dans un environnement de test avant de les executer en production.

- La suppression d'un grand nombre de documents peut prendre du temps
- Les performances de l'index peuvent etre affectees pendant la suppression
- Les resultats de recherche peuvent prendre un moment pour refleter les suppressions

Bonnes pratiques
----------------

1. **Verification avant suppression**: Utilisez l'API de recherche avec la meme requete pour verifier les documents cibles
2. **Suppression par etapes**: Effectuez les suppressions massives en plusieurs operations
3. **Sauvegarde**: Sauvegardez les donnees importantes avant la suppression

Exemples d'utilisation
======================

Preparation pour un nouveau crawl complet d'un site
---------------------------------------------------

.. code-block:: bash

    # Supprimer les anciens documents du site
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=host:example.com" \
         -H "Authorization: Bearer YOUR_TOKEN"

    # Demarrer la tache de crawl
    curl -X PUT "http://localhost:8080/api/admin/scheduler/{job_id}/start" \
         -H "Authorization: Bearer YOUR_TOKEN"

Nettoyage des anciens documents
-------------------------------

.. code-block:: bash

    # Supprimer les documents non mis a jour depuis plus d'un an
    curl -X DELETE "http://localhost:8080/api/admin/documents?q=lastModified:[* TO now-1y]" \
         -H "Authorization: Bearer YOUR_TOKEN"

Informations complementaires
============================

- :doc:`api-admin-overview` - Vue d'ensemble de l'API Admin
- :doc:`api-admin-crawlinginfo` - API des informations de crawl
- :doc:`../../admin/searchlist-guide` - Guide de gestion de la liste de recherche
