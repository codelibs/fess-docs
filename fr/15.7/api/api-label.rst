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

Paramètres de requête
---------------------

Aucun paramètre de requête n'est disponible.

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
     - Nombre d'étiquettes enregistrées (entier).
   * - ``labels``
     - Tableau des étiquettes.
   * - ``label``
     - Nom de l'étiquette.
   * - ``value``
     - Valeur de l'étiquette.

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
     - La méthode HTTP n'est pas autorisée.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Tableau : Réponses d'erreur
