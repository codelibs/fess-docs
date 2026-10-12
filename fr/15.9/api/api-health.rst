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
Le statut HTTP est 200 si l'état du cluster est ``GREEN`` ou ``YELLOW``, et 503 si l'état est ``RED`` ou si le moteur de recherche est injoignable.

Ce point de terminaison respecte l'invariant de l'enveloppe : « ``status >= 1`` ⟺ statut HTTP ``>= 400`` ».

- En cas d'état ``GREEN`` ou ``YELLOW`` : retourne l'enveloppe de succès (``status: 0``) avec ``engine``.
- En cas d'état ``RED`` : retourne l'enveloppe d'erreur (``status: 9``, ``error.code: service_unavailable``) et intègre l'instantané du moteur sous ``error.details.engine`` (pour permettre aux outils de supervision d'analyser les métadonnées du cluster).
- Si le moteur de recherche est injoignable : retourne, comme pour ``RED``, l'enveloppe d'erreur (``error.code: service_unavailable``, ``error.message: search engine is not reachable``) ; ``error.details.engine`` contient ``status: UNAVAILABLE`` et ``ping_status: 1``.

Les champs de ``engine`` sont les suivants.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Champs de engine

   * - ``status``
     - État du cluster. L'une des valeurs ``GREEN`` / ``YELLOW`` / ``RED`` (en majuscules). ``UNAVAILABLE`` si le moteur de recherche est injoignable.
   * - ``ping_status``
     - Statut du ping (int). La valeur est ``1`` lorsque le cluster est ``RED`` ou que le moteur de recherche est injoignable, et ``0`` dans les autres cas (``GREEN`` / ``YELLOW``).

Tableau : Champs de engine

Le nom du cluster (``cluster_name``) n'est pas retourné, car ce point de terminaison peut être appelé sans authentification.

Paramètres de requête
---------------------

Aucun paramètre de requête n'est disponible.

Réponse
-------

Lorsque le cluster est ``GREEN`` ou ``YELLOW`` (200), l'enveloppe de succès est retournée avec ``engine``.

::

    {
      "response": {
        "status": 0,
        "engine": {
          "status": "GREEN",
          "ping_status": 0
        }
      }
    }

Lorsque le cluster est ``RED`` (503), l'enveloppe d'erreur est retournée, avec l'instantané du moteur intégré sous ``error.details.engine``.

::

    {
      "response": {
        "status": 9,
        "error": {
          "code": "service_unavailable",
          "message": "search engine cluster is red",
          "details": {
            "engine": {
              "status": "RED",
              "ping_status": 1
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
     - Le cluster est ``GREEN`` ou ``YELLOW`` et joignable. L'enveloppe de succès contient ``engine``.
   * - 405 Method Not Allowed
     - La méthode HTTP n'est pas autorisée.
   * - 503 Service Unavailable
     - Le cluster est ``RED`` ou le moteur de recherche est injoignable. L'enveloppe d'erreur (``error.code: service_unavailable``) contient l'instantané du moteur sous ``error.details.engine``.

Tableau : Liste des réponses
