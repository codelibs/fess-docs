==================
API des étiquettes
==================

Ce document décrit l'API des étiquettes v2 de |Fess|.
Pour l'enveloppe de réponse commune et le modèle d'erreur, voir :doc:`api-overview`.

L'URL de base est ``http://<Server Name>/api/v2/`` (exemple en environnement local : ``http://localhost:8080/api/v2``).

Récupération des étiquettes
===========================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/labels``
====================  ====================================================

Récupère la liste des étiquettes configurées dans |Fess|, encapsulée dans l'enveloppe commune.

La liste des étiquettes retournées est filtrée en fonction de l'utilisateur et du contenu de la requête, comme suit.

- **Filtrage par permissions** : les étiquettes sont filtrées selon les droits d'accès qui leur sont associés et les rôles de l'utilisateur. L'API v2 utilisant une authentification basée sur les sessions, les utilisateurs connectés ne récupèrent que les étiquettes auxquelles leurs rôles donnent accès. Les étiquettes dont les droits d'accès ne correspondent pas sont exclues de la liste.
- **Filtrage par locale** : les étiquettes peuvent être enregistrées par locale. Les étiquettes enregistrées avec une locale correspondant à l'en-tête de requête ``Accept-Language``, ainsi que les étiquettes enregistrées sans locale spécifique, sont retournées.
- **Filtrage par hôte virtuel** : lorsque des hôtes virtuels sont utilisés, seules les étiquettes assignées à l'hôte virtuel concerné sont retournées.

Paramètres de requête
---------------------

Aucun paramètre de requête n'est disponible. Le filtrage des étiquettes retournées s'effectue, comme indiqué ci-dessus, en fonction des permissions de l'utilisateur authentifié et de l'en-tête de requête ``Accept-Language``.

Réponse
-------

En cas de succès (200), les champs suivants sont retournés directement sous ``response`` dans l'enveloppe commune.

::

    {
      "response": {
        "status": 0,
        "record_count": 2,
        "labels": [
          {
            "label": "AWS",
            "value": "aws"
          },
          {
            "label": "Azure",
            "value": "azure"
          }
        ]
      }
    }

Les détails de chaque champ sont les suivants.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Champs de réponse

   * - ``record_count``
     - Nombre d'étiquettes retournées (entier).
   * - ``labels``
     - Tableau des étiquettes.
   * - ``label``
     - Nom d'affichage de l'étiquette (nom de l'étiquette).
   * - ``value``
     - Valeur de l'étiquette. En spécifiant cette valeur dans le paramètre ``fields.label`` de l'API :doc:`api-search`, il est possible de filtrer les résultats de recherche par l'étiquette concernée.

Tableau : Champs de réponse

Exemple d'utilisation
=====================

Exemple de requête avec la commande curl :

::

    curl "http://localhost:8080/api/v2/labels"

Réponse d'erreur
================

Pour le détail du modèle d'erreur, voir :doc:`api-overview`. Les statuts HTTP retournés par ce point de terminaison sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 405 Method Not Allowed
     - Une méthode HTTP autre que GET a été spécifiée. ``error.code`` vaut ``method_not_allowed`` et l'en-tête ``Allow: GET`` est ajouté à la réponse.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur. ``error.code`` vaut ``internal_error``.

Tableau : Réponses d'erreur
