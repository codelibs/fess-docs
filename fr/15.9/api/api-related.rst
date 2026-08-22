======================================
API des requêtes et contenus associés
======================================

Cette page décrit les deux points de terminaison permettant de récupérer des informations associées à une requête.

- ``GET /related-queries`` — Récupère les suggestions de requêtes associées à une requête.
- ``GET /related-content`` — Récupère le contenu HTML associé à une requête.

Les deux résultats sont basés sur les paramètres de requêtes associées et de contenu associé enregistrés au préalable par l'administrateur. Un résultat vide est retourné lorsqu'aucune correspondance n'est trouvée.

Pour l'enveloppe de réponse commune et le modèle d'erreur, voir :doc:`api-overview`.

Récupération des requêtes associées
====================================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/related-queries``
====================  ====================================================

En envoyant une requête à |Fess| de type ``http://<Server Name>/api/v2/related-queries?q=fess``, vous pouvez recevoir au format JSON la liste des requêtes associées à la requête spécifiée.

Le terme de recherche demandé est comparé aux paramètres de requêtes associées enregistrés sans distinction de casse.
Même si ``q`` est vide ou non spécifié, aucune erreur n'est retournée : un tableau ``queries`` vide est renvoyé. La réponse est toujours une enveloppe de succès.

Paramètres de requête
---------------------

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Paramètres de requête

   * - q
     - Terme de recherche pour lequel récupérer les requêtes associées. (Ex.) ``q=fess``

Réponse
-------

En cas de succès, une réponse au format d'enveloppe commune est retournée.

::

    {
      "response": {
        "status": 0,
        "queries": [
          "fess search",
          "fess install"
        ]
      }
    }

Les détails de chaque élément de ``response`` sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Informations de réponse

   * - queries
     - Tableau des requêtes associées (tableau de chaînes de caractères). Un tableau vide est également retourné si ``q`` est vide ou non spécifié, ou si aucun paramètre correspondant n'est trouvé.

Exemple d'utilisation
---------------------

Exemple de requête avec la commande curl :

::

    curl "http://localhost:8080/api/v2/related-queries?q=fess"

Réponse d'erreur
----------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 405 Method Not Allowed
     - Une méthode HTTP non prise en charge a été spécifiée. L'en-tête ``Allow`` indique ``GET``.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.

Récupération du contenu associé
================================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/related-content``
====================  ====================================================

En envoyant une requête à |Fess| de type ``http://<Server Name>/api/v2/related-content?q=fess``, vous pouvez recevoir au format JSON le contenu HTML associé à la requête spécifiée.

Le terme de recherche demandé est comparé aux paramètres de contenu associé enregistrés. Lorsque plusieurs éléments de contenu correspondent, ils sont concaténés avec des sauts de ligne.
Même si ``q`` est vide ou non spécifié, aucune erreur n'est retournée : un ``content`` vide (chaîne vide) est renvoyé. La réponse est toujours une enveloppe de succès.

Paramètres de requête
---------------------

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Paramètres de requête

   * - q
     - Terme de recherche pour lequel récupérer le contenu associé. (Ex.) ``q=fess``

Réponse
-------

En cas de succès, une réponse au format d'enveloppe commune est retournée.

::

    {
      "response": {
        "status": 0,
        "content": "<div>...contenu HTML associé...</div>",
        "content_type": "html"
      }
    }

Les détails de chaque élément de ``response`` sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Informations de réponse

   * - content
     - Contenu HTML associé (chaîne de caractères). Si plusieurs éléments correspondent, ils sont concaténés avec des sauts de ligne. Une chaîne vide est également retournée si ``q`` est vide ou non spécifié, ou si aucun paramètre correspondant n'est trouvé.
   * - content_type
     - Type de contenu. La valeur est toujours ``html``.

Exemple d'utilisation
---------------------

Exemple de requête avec la commande curl :

::

    curl "http://localhost:8080/api/v2/related-content?q=fess"

Réponse d'erreur
----------------

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 405 Method Not Allowed
     - Une méthode HTTP non prise en charge a été spécifiée. L'en-tête ``Allow`` indique ``GET``.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.
