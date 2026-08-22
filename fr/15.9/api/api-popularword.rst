=======================
API des mots populaires
=======================

Obtention de la liste des mots populaires
==========================================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/popular-words``
====================  ====================================================

En envoyant une requête à |Fess| de type ``http://<Server Name>/api/v2/popular-words?seed=123``, vous pouvez recevoir au format JSON la liste des mots de recherche populaires.

Lorsque ``web.api.popularword=false``, cette API retourne ``invalid_request`` (HTTP 400) (comportement équivalent à « unsupported operation » en v1).

Pour l'enveloppe de réponse commune et le modèle d'erreur, voir :doc:`api-overview`.

Paramètres de requête
---------------------

Les paramètres de requête disponibles sont les suivants.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Paramètres de requête

   * - seed
     - Graine (seed) pour la récupération des mots populaires (chaîne de caractères). Cette valeur permet d'obtenir différents ensembles de mots. (Ex.) ``seed=123``
   * - label
     - Nom d'étiquette à filtrer. Peut être répété pour être traité comme un tableau. (Ex.) ``label=java``
   * - field
     - Nom de champ pour générer les mots populaires. Peut être répété pour être traité comme un tableau. (Ex.) ``field=label``

Réponse
-------

En cas de succès, une réponse au format d'enveloppe commune est retournée.

::

    {
      "response": {
        "status": 0,
        "record_count": 3,
        "popular_words": [
          "python",
          "java",
          "javascript"
        ]
      }
    }

Les détails de chaque élément de ``response`` sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Informations de réponse

   * - record_count
     - Nombre de mots populaires (entier).
   * - popular_words
     - Tableau des mots populaires (tableau de chaînes de caractères).

.. note::

   En v2, les mots populaires sont retournés sous la forme ``popular_words`` (tableau de chaînes de caractères), et non ``data`` comme en v1.

Exemple d'utilisation
=====================

Exemple de requête avec la commande curl :

::

    curl "http://localhost:8080/api/v2/popular-words?seed=123"

Réponse d'erreur
================

En cas d'échec de l'API des mots populaires, l'enveloppe d'erreur commune est retournée. Pour le détail du modèle d'erreur, voir :doc:`api-overview`.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 400 Bad Request
     - La requête est incorrecte (y compris lorsque la fonctionnalité est désactivée via ``web.api.popularword=false``). ``error.code`` vaut ``invalid_request``.
   * - 405 Method Not Allowed
     - Une méthode HTTP non prise en charge a été spécifiée.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.
