==============
API d'étiquettes
==============

Obtention des étiquettes
=========================

Requête
-------

==================  ====================================================
Méthode HTTP        GET
Point de terminaison ``/api/v1/labels``
==================  ====================================================

En envoyant une requête à |Fess| de type ``http://<Nom du serveur>/api/v1/labels``, vous pouvez recevoir la liste des étiquettes enregistrées dans |Fess| au format JSON.

Paramètres de requête
---------------------

Aucun paramètre de requête n'est disponible.


Réponse
-------

Une réponse comme celle-ci est retournée.

::

    {
      "record_count": 9,
      "data": [
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

Les éléments sont les suivants :

.. tabularcolumns:: |p{3cm}|p{12cm}|

.. list-table::

   * - record_count
     - Nombre d'étiquettes enregistrées.
   * - data
     - Élément parent des résultats de recherche.
   * - label
     - Nom de l'étiquette.
   * - value
     - Valeur de l'étiquette.

Tableau : Informations de réponse

Exemples d'utilisation
=======================

Exemple de requête avec la commande curl :

::

    curl "http://localhost:8080/api/v1/labels"

Exemple de requête en JavaScript :

::

    fetch('http://localhost:8080/api/v1/labels')
      .then(response => response.json())
      .then(data => {
        console.log('Liste des étiquettes:', data.data);
      });

Réponse d'erreur
================

Lorsque l'API d'étiquettes échoue, une réponse d'erreur comme celle-ci est retournée.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponse d'erreur

   * - Code de statut
     - Description
   * - 500 Internal Server Error
     - Lorsqu'une erreur interne du serveur s'est produite
