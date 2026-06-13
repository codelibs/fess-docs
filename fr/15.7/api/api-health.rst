==========
Health API
==========

Ce document décrit l'API Health v2 de |Fess|.
Pour l'enveloppe de réponse commune et le modèle d'erreur, voir :doc:`api-overview`.

L'URL de base est ``http://<Server Name>/api/v2/`` (exemple en environnement local : ``http://localhost:8080/api/v2``).

Récupération de l'état
======================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/health``
====================  ====================================================

Retourne un instantané de l'état du cluster du moteur de recherche (tag ``monitor``).
Le statut HTTP est 200 si l'état du cluster est ``green`` ou ``yellow``, et 503 si l'état est ``red``.

Ce point de terminaison respecte l'invariant de l'enveloppe : « ``status >= 1`` ⟺ statut HTTP ``>= 400`` ».

- En cas d'état ``green`` ou ``yellow`` : retourne l'enveloppe de succès (``status: 0``) avec ``engine``.
- En cas d'état ``red`` : retourne l'enveloppe d'erreur (``status: 9``, ``error.code: service_unavailable``) et intègre l'instantané du moteur sous ``error.details.engine`` (pour permettre aux outils de supervision d'analyser les métadonnées du cluster).

Les champs de ``engine`` sont les suivants.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Champs de engine

   * - ``cluster_name``
     - Nom du cluster (str).
   * - ``status``
     - État du cluster. L'une des valeurs ``green`` / ``yellow`` / ``red``.
   * - ``ping_status``
     - Statut du ping (int).

Tableau : Champs de engine

Paramètres de requête
---------------------

Aucun paramètre de requête n'est disponible.

Réponse
-------

Lorsque le cluster est ``green`` ou ``yellow`` (200), l'enveloppe de succès est retournée avec ``engine``.

::

    {
      "response": {
        "status": 0,
        "engine": {
          "cluster_name": "fess-es",
          "status": "green",
          "ping_status": 0
        }
      }
    }

Lorsque le cluster est ``red`` (503), l'enveloppe d'erreur est retournée, avec l'instantané du moteur intégré sous ``error.details.engine``.

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "search engine cluster is red",
          "details": {
            "engine": {
              "cluster_name": "fess-es",
              "status": "red",
              "ping_status": 2
            }
          }
        }
      }
    }

Exemple d'utilisation
=====================

Exemple de requête avec la commande curl :

::

    curl "http://localhost:8080/api/v2/health"

Réponse et réponse d'erreur
============================

Pour le détail du modèle d'erreur, voir :doc:`api-overview`. Les statuts HTTP retournés par ce point de terminaison sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Liste des réponses

   * - Code de statut
     - Description
   * - 200 OK
     - Le cluster est ``green`` ou ``yellow`` et joignable. L'enveloppe de succès contient ``engine``.
   * - 405 Method Not Allowed
     - La méthode HTTP n'est pas autorisée.
   * - 503 Service Unavailable
     - Le cluster est ``red``. L'enveloppe d'erreur (``error.code: service_unavailable``) contient l'instantané du moteur sous ``error.details.engine``.

Tableau : Liste des réponses
