==================
API de suggestions
==================

Obtention de la liste des mots suggérés
=========================================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/suggest-words``
====================  ====================================================

En envoyant une requête à |Fess| de type ``http://<Server Name>/api/v2/suggest-words?q=fes``, vous pouvez recevoir au format JSON la liste des mots suggérés pour le préfixe saisi.

Les mots suggérés proviennent de trois sources :

- **Documents** — Générés à partir des documents explorés. Pour les obtenir, activez « Suggérer à partir des documents » dans l'interface d'administration sous Système > Général.
- **Termes de recherche (journal de recherche)** — Générés à partir des journaux de recherche des utilisateurs. Pour les obtenir, activez « Suggérer à partir des termes de recherche » dans l'interface d'administration sous Système > Général.
- **Dictionnaire utilisateur** — Mots suggérés enregistrés par les administrateurs. Ils sont toujours retournés indépendamment des paramètres ci-dessus.

Même lorsque « Suggérer à partir des documents » et « Suggérer à partir des termes de recherche » sont désactivés, l'API ne retourne pas d'erreur ; les mots suggérés correspondants sont simplement omis des résultats.
Les mots suggérés sont également filtrés automatiquement en fonction des rôles de l'utilisateur effectuant la requête.

Pour l'enveloppe de réponse commune et le modèle d'erreur, voir :doc:`api-overview`.

Paramètres de requête
---------------------

Les paramètres de requête disponibles sont les suivants.

.. tabularcolumns:: |p{3cm}|p{12cm}|
.. list-table:: Paramètres de requête

   * - q
     - Terme de recherche (préfixe) pour la suggestion. Si omis, les mots suggérés sont retournés sans filtrage par préfixe. (Ex.) ``q=fes``
   * - num
     - Nombre de mots suggérés (entier >= 0). Valeur par défaut ``10``. Si une valeur non numérique est spécifiée, la valeur par défaut est utilisée. (Ex.) ``num=20``
   * - fn
     - Nom de champ pour affiner les cibles de suggestion. Peut être répété pour être traité comme un tableau. (Ex.) ``fn=content&fn=title``
   * - lang
     - Langue de recherche. Peut être répété pour être traité comme un tableau. (Ex.) ``lang=en``
   * - label
     - Nom d'étiquette (tag) pour filtrer. Peut être répété pour être traité comme un tableau. Les valeurs spécifiées sont comparées aux ``types`` de chaque mot suggéré. (Ex.) ``label=java``

.. note::

   En v2, le paramètre de nom de champ est ``fn`` (et non ``fields`` comme en v1).
   De même, au lieu de transmettre les valeurs sous forme de chaîne séparée par des virgules, ``fn`` est répété pour passer plusieurs valeurs.

Réponse
-------

En cas de succès, une réponse au format d'enveloppe commune est retournée.

::

    {
      "response": {
        "status": 0,
        "q": "fes",
        "page_size": 10,
        "record_count": 355,
        "query_time": 18,
        "suggest_words": [
          {
            "text": "fess",
            "types": [
              "label1"
            ]
          }
        ]
      }
    }

Les détails de chaque élément de ``response`` sont les suivants.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Informations de réponse

   * - q
     - Terme de recherche demandé (chaîne de caractères). Retourne une chaîne vide lorsque ``q`` est omis.
   * - page_size
     - Nombre de mots suggérés demandés (valeur de ``num``, entier).
   * - record_count
     - Nombre total de mots suggérés correspondants (entier 64 bits).
   * - query_time
     - Temps de traitement de la requête en millisecondes (entier 64 bits).
   * - suggest_words
     - Tableau des mots suggérés. Chaque élément possède ``text`` et ``types``.
   * - text
     - Mot suggéré (chaîne de caractères).
   * - types
     - Tableau des étiquettes (tags) associées au mot suggéré (tableau de chaînes de caractères). Chaque étiquette est dérivée du champ ``label`` ou ``virtual_host`` d'un document, ou des conditions de filtre extraites du journal de recherche. Retourne un tableau vide lorsqu'il n'y a pas d'étiquettes.

.. note::

   ``types`` contient des valeurs d'étiquettes (tags), et non le type du mot suggéré (tel que ``document`` ou ``query``). Ce tableau correspond au champ ``labels`` des éléments de suggestion en v1.
   Le paramètre de requête ``label`` filtre sur ces valeurs ``types``.

Exemples d'utilisation
=======================

Exemple de requête avec la commande curl :

::

    curl "http://localhost:8080/api/v2/suggest-words?q=fes"

Réponse d'erreur
================

En cas d'échec de l'API de suggestions, l'enveloppe d'erreur commune est retournée. Pour le détail du modèle d'erreur, voir :doc:`api-overview`.

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur

   * - Code de statut
     - Description
   * - 405 Method Not Allowed
     - Une méthode HTTP non prise en charge a été spécifiée. L'en-tête ``Allow`` indique ``GET``.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.
