========================
API de configuration UI
========================

Vue d'ensemble
==============

L'API de configuration UI retourne la configuration initiale dont a besoin une application monopage (SPA) : thème, indicateurs de fonctionnalités, limite de pagination, et — si CSRF est requis — un nouveau jeton CSRF.
Ce point de terminaison est appelé de manière anonyme avant la connexion.

Pour l'enveloppe de réponse commune et le modèle d'erreur, voir :doc:`api-overview`.

Récupération de la configuration UI
=====================================

Requête
-------

====================  ====================================================
Méthode HTTP          GET
Point de terminaison  ``/api/v2/ui/config``
====================  ====================================================

Retourne la configuration initiale dont a besoin la SPA.

Réponse
-------

En cas de succès (HTTP 200, UiConfigResponse), une réponse au format d'enveloppe commune est retournée (extrait).

.. code-block:: json

    {
      "response": {
        "status": 0,
        "site_name": "Fess",
        "login_required": false,
        "locales": ["en", "ja"],
        "theme": {
          "name": "default",
          "display_name": "Default Theme",
          "version": "1.0.0",
          "supported_locales": ["en", "ja"]
        },
        "features": {
          "user_favorite": false,
          "popular_word": true,
          "suggest_search_log": true,
          "suggest_documents": true,
          "login_required": false,
          "eoled": false,
          "development_mode": false,
          "search_log_enabled": true,
          "thumbnail_enabled": true,
          "display_label_type": false,
          "clipboard_copy_icon": true,
          "eol_link": "",
          "installation_link": "https://fess.codelibs.org/15.7/install/",
          "login_link": true,
          "rag_chat_enabled": false
        },
        "page_size_default": 20,
        "page_size_max": 100,
        "sort_options": [
          {"value": "", "label_key": "labels.sort_score"}
        ],
        "num_options": [10, 20, 30, 40, 50, 100],
        "lang_options": [
          {"value": "all", "label_key": "labels.search_result_select_lang"},
          {"value": "ja", "label_key": "labels.search_result_select_lang_ja"}
        ],
        "label_options": [],
        "notifications": {
          "search_top": "",
          "advance_search": "",
          "login": ""
        },
        "facet_views": [],
        "filetype_options": [
          {"value": "html", "label_key": "labels.facet_filetype_html"}
        ],
        "csrf_required": true,
        "csrf_token": "0c1f2e3d4a5b6c7d8e9f"
      }
    }

Les détails de chaque élément de ``response`` sont les suivants. Tous les champs sont obligatoires.

.. tabularcolumns:: |p{4cm}|p{2.5cm}|p{8.5cm}|
.. list-table:: Informations de réponse
   :header-rows: 1
   :widths: 25 15 60

   * - Champ
     - Type
     - Description
   * - ``site_name``
     - string
     - Nom du site.
   * - ``login_required``
     - boolean
     - Indique si la connexion est requise.
   * - ``locales``
     - string[]
     - Tableau des paramètres régionaux disponibles.
   * - ``theme``
     - object
     - Descripteur du thème actif. Voir le tableau ci-dessous.
   * - ``features``
     - object
     - Indicateurs de fonctionnalités. Voir le tableau ci-dessous.
   * - ``page_size_default``
     - integer
     - Taille de page par défaut.
   * - ``page_size_max``
     - integer
     - Taille de page maximale.
   * - ``sort_options``
     - object[]
     - Options de tri pour l'interface de recherche. Voir le tableau ci-dessous.
   * - ``num_options``
     - integer[]
     - Tableau des tailles de page sélectionnables. Limité aux valeurs ne dépassant pas ``page_size_max``.
   * - ``lang_options``
     - object[]
     - Options de filtre de langue. Voir le tableau ci-dessous.
   * - ``label_options``
     - object[]
     - Options des étiquettes configurées. Voir le tableau ci-dessous.
   * - ``notifications``
     - object
     - Extraits HTML de notification affichés en haut de certaines vues. Voir le tableau ci-dessous.
   * - ``facet_views``
     - object[]
     - Groupes de vues de facettes configurés. Voir le tableau ci-dessous.
   * - ``filetype_options``
     - object[]
     - Options de facette de type de fichier pour le formulaire de recherche avancée. Voir le tableau ci-dessous.
   * - ``csrf_required``
     - boolean
     - Indique si un jeton CSRF est requis.
   * - ``csrf_token``
     - string
     - Chaîne vide si ``csrf_required`` vaut ``false`` ; sinon, nouveau jeton associé à la session courante.

theme
~~~~~

``theme`` est toujours présent, mais peut être un objet vide si aucun thème personnalisé n'est associé à la requête.
Les clés issues du manifeste (``display_name`` / ``version`` / ``supported_locales``) ne sont présentes que si le thème actif inclut un manifeste.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: theme
   :header-rows: 1
   :widths: 28 15 57

   * - Champ
     - Type
     - Description
   * - ``name``
     - string
     - Nom du thème.
   * - ``display_name``
     - string
     - Nom d'affichage du thème.
   * - ``version``
     - string
     - Version du thème.
   * - ``supported_locales``
     - string[]
     - Tableau des paramètres régionaux pris en charge par le thème.

features
~~~~~~~~

Tous les champs sont obligatoires.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: features
   :header-rows: 1
   :widths: 28 15 57

   * - Champ
     - Type
     - Description
   * - ``user_favorite``
     - boolean
     - Indique si la fonctionnalité de favoris utilisateur est activée.
   * - ``popular_word``
     - boolean
     - Indique si la fonctionnalité de mots populaires est activée.
   * - ``suggest_search_log``
     - boolean
     - Indique si la suggestion basée sur les journaux de recherche est activée.
   * - ``suggest_documents``
     - boolean
     - Indique si la suggestion basée sur les documents est activée.
   * - ``login_required``
     - boolean
     - Indique si la connexion est requise.
   * - ``eoled``
     - boolean
     - Indique si ce build de |Fess| a atteint sa fin de vie (EOL).
   * - ``development_mode``
     - boolean
     - Vaut ``true`` lorsque le moteur de recherche intégré (mode développement) est utilisé.
   * - ``search_log_enabled``
     - boolean
     - Indique si les journaux de recherche sont activés.
   * - ``thumbnail_enabled``
     - boolean
     - Indique si les miniatures sont activées.
   * - ``display_label_type``
     - boolean
     - Vaut ``true`` lorsqu'au moins une étiquette est configurée.
   * - ``clipboard_copy_icon``
     - boolean
     - Indique si l'icône de copie dans le presse-papiers doit être affichée.
   * - ``eol_link``
     - string
     - URL résolue des informations EOL. Chaîne vide si non en EOL ou si l'URL ne peut pas être résolue.
   * - ``installation_link``
     - string
     - URL résolue du guide d'installation. Chaîne vide si l'URL ne peut pas être résolue.
   * - ``login_link``
     - boolean
     - Indique si le lien de connexion doit être affiché.
   * - ``rag_chat_enabled``
     - boolean
     - Indique si la fonctionnalité de chat RAG est disponible.

sort_options
~~~~~~~~~~~~

Tableau des options de tri pour l'interface de recherche.
Chaque élément possède ``value`` et ``label_key``.
Les éléments ``click_count.*`` ne sont présents que si les journaux de recherche sont activés, et les éléments ``favorite_count.*`` ne sont présents que si les favoris utilisateur sont activés.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Éléments de sort_options
   :header-rows: 1
   :widths: 28 15 57

   * - Champ
     - Type
     - Description
   * - ``value``
     - string
     - Valeur de tri.
   * - ``label_key``
     - string
     - Clé de libellé.

num_options
~~~~~~~~~~~

Tableau d'entiers des tailles de page sélectionnables. Limité aux valeurs ne dépassant pas ``page_size_max``.

lang_options
~~~~~~~~~~~~

Tableau des options de filtre de langue.
Chaque élément possède ``value`` et ``label_key``.
Le premier élément est la sentinelle ``all``, suivie d'un élément par code de langue pris en charge.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Éléments de lang_options
   :header-rows: 1
   :widths: 28 15 57

   * - Champ
     - Type
     - Description
   * - ``value``
     - string
     - Valeur de langue.
   * - ``label_key``
     - string
     - Clé de libellé.

label_options
~~~~~~~~~~~~~

Tableau des options des étiquettes configurées. Tableau vide si aucune étiquette n'est définie.
Chaque élément possède ``value`` et ``name``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Éléments de label_options
   :header-rows: 1
   :widths: 28 15 57

   * - Champ
     - Type
     - Description
   * - ``value``
     - string
     - Valeur de l'étiquette.
   * - ``name``
     - string
     - Nom de l'étiquette.

notifications
~~~~~~~~~~~~~

Extraits HTML de notification affichés en haut de certaines vues. Une chaîne vide signifie qu'il n'y a pas de notification pour cette vue.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: notifications
   :header-rows: 1
   :widths: 28 15 57

   * - Champ
     - Type
     - Description
   * - ``search_top``
     - string
     - Notification affichée sur la page d'accueil de recherche.
   * - ``advance_search``
     - string
     - Notification affichée sur la page de recherche avancée.
   * - ``login``
     - string
     - Notification affichée sur la page de connexion.

facet_views
~~~~~~~~~~~

Tableau des groupes de vues de facettes configurés. Tableau vide si aucun groupe n'est défini.
Chaque élément possède ``group_name`` et ``queries``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Éléments de facet_views
   :header-rows: 1
   :widths: 28 15 57

   * - Champ
     - Type
     - Description
   * - ``group_name``
     - string
     - Nom du groupe.
   * - ``queries``
     - object[]
     - Tableau des requêtes de facette de ce groupe. Chaque élément possède ``label_key`` (string) et ``value`` (string).

filetype_options
~~~~~~~~~~~~~~~~

Tableau des options de facette de type de fichier pour le formulaire de recherche avancée.
Chaque élément possède ``value`` et ``label_key``.

.. tabularcolumns:: |p{4.5cm}|p{2.5cm}|p{8cm}|
.. list-table:: Éléments de filetype_options
   :header-rows: 1
   :widths: 28 15 57

   * - Champ
     - Type
     - Description
   * - ``value``
     - string
     - Valeur du type de fichier.
   * - ``label_key``
     - string
     - Clé de libellé.

Réponse d'erreur
~~~~~~~~~~~~~~~~

.. tabularcolumns:: |p{4cm}|p{11cm}|
.. list-table:: Réponses d'erreur
   :header-rows: 1
   :widths: 25 75

   * - Code de statut
     - Description
   * - 405 Method Not Allowed
     - Une méthode HTTP non prise en charge a été spécifiée.
   * - 500 Internal Server Error
     - Une erreur interne s'est produite sur le serveur.
