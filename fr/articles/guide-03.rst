============================================================
Partie 3 : Intégrer la recherche dans un portail interne -- Ajout d'une fonction de recherche à un site Web existant
============================================================

Introduction
============

Dans la partie précédente, nous avons lancé Fess avec Docker Compose et expérimenté la recherche.
Cependant, dans la pratique, il ne s'agit pas seulement d'utiliser l'interface de recherche de Fess telle quelle ; le besoin le plus fréquent est d'ajouter une fonction de recherche à un site interne ou à un portail existant.

Dans cet article, nous présentons trois approches pour intégrer la fonction de recherche de Fess dans un site Web existant, en expliquant les caractéristiques et les critères de choix de chacune.

Public cible
============

- Personnes souhaitant ajouter une fonction de recherche à un portail interne ou un site Web
- Personnes ayant des connaissances de base en développement front-end
- Fess doit être opérationnel conformément aux étapes de la Partie 2

Environnement requis
====================

- L'environnement Fess construit dans la Partie 2 (Docker Compose)
- Une page Web de test (un fichier HTML local convient également)

Trois approches d'intégration
==============================

Il existe trois grandes méthodes pour intégrer la fonction de recherche de Fess dans un site existant.

.. list-table:: Comparaison des approches d'intégration
   :header-rows: 1
   :widths: 15 30 25 30

   * - Approche
     - Description
     - Effort de développement
     - Cas d'utilisation adapté
   * - FSS (Fess Site Search)
     - Insertion d'une simple balise JavaScript
     - Minimal (quelques lignes de code)
     - Ajouter rapidement une recherche
   * - Liaison par formulaire de recherche
     - Redirection vers Fess via un formulaire HTML
     - Faible (modification HTML uniquement)
     - Utiliser l'interface de recherche de Fess telle quelle
   * - Intégration via l'API de recherche
     - Construction d'une interface personnalisée via l'API JSON
     - Moyen à élevé (développement front-end)
     - Personnalisation complète du design et du comportement

Examinons chaque méthode à travers des scénarios concrets.

Approche 1 : Ajout rapide avec FSS (Fess Site Search)
=======================================================

Scénario
--------

Vous disposez d'un portail interne et avez les droits de modification du HTML, mais vous souhaitez éviter des modifications majeures.
Vous voulez permettre la recherche de documents internes depuis le portail avec un minimum de changements.

Qu'est-ce que FSS ?
--------------------

Fess Site Search (FSS) est un mécanisme qui permet d'ajouter une fonction de recherche simplement en intégrant une balise JavaScript dans une page Web.
Le champ de recherche et l'affichage des résultats sont entièrement gérés par JavaScript, ce qui ne nécessite quasiment aucune modification de la structure de la page existante.

Procédure de mise en oeuvre
----------------------------

1. Autorisez l'accès à l'API depuis l'interface d'administration de Fess.
   Dans la page [Système] > [Général], activez la réponse JSON.

2. Intégrez le code suivant dans la page à laquelle vous souhaitez ajouter la fonction de recherche.

.. code-block:: html

    <script>
      (function() {
        var fess = document.createElement('script');
        fess.type = 'text/javascript';
        fess.async = true;
        fess.src = 'http://localhost:8080/js/fess-ss.min.js';
        fess.charset = 'utf-8';
        fess.setAttribute('id', 'fess-ss');
        fess.setAttribute('fess-url', 'http://localhost:8080/api/v1/documents');
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(fess, s);
      })();
    </script>

    <fess:search></fess:search>

Le champ de recherche et les résultats s'affichent à l'emplacement de la balise ``<fess:search>``.

Personnalisation
-----------------

L'apparence de FSS peut être personnalisée en CSS.
En surchargeant les styles par défaut fournis par Fess, vous pouvez adapter l'apparence au design de votre site existant.

.. code-block:: css

    .fessWrapper {
      font-family: 'Noto Sans JP', sans-serif;
      max-width: 800px;
      margin: 0 auto;
    }
    .fessWrapper .searchButton {
      background-color: #1a73e8;
    }

Approche 2 : Liaison par formulaire de recherche pour une solution simple
==========================================================================

Scénario
--------

Votre portail interne dispose déjà d'une barre de navigation dans l'en-tête.
Vous souhaitez y ajouter un champ de recherche qui redirige vers la page de résultats de Fess lors de l'exécution de la recherche.
Vous voulez le faire uniquement en HTML, sans JavaScript.

Procédure de mise en oeuvre
----------------------------

Ajoutez le formulaire HTML suivant à votre barre de navigation existante.

.. code-block:: html

    <form action="http://localhost:8080/search" method="get">
      <input type="text" name="q" placeholder="Recherche interne..." />
      <button type="submit">Rechercher</button>
    </form>

C'est tout ce qu'il faut pour rediriger vers la page de résultats de Fess lors de l'exécution d'une recherche.
En personnalisant le design de la page de recherche de Fess, vous pouvez offrir une expérience cohérente.

Personnalisation de la page de recherche Fess
-----------------------------------------------

La page de recherche de Fess est composée de fichiers JSP et peut également être modifiée depuis l'interface d'administration.

1. Sélectionnez [Système] > [Design de la page] dans l'interface d'administration
2. Personnalisez l'en-tête, le pied de page, le CSS, etc.

Par exemple, en harmonisant le logo avec celui du portail interne ou en unifiant les couleurs, vous pouvez offrir une expérience de recherche familière pour les utilisateurs.

Utilisation du mapping de chemins
----------------------------------

Vous pouvez convertir les URL affichées dans les résultats de recherche en URL plus accessibles pour les utilisateurs.
Par exemple, même si l'URL lors du crawl est ``http://internal-server:8888/docs/``, il est possible d'afficher ``https://portal.example.com/docs/`` dans les résultats de recherche.

Ce paramétrage est accessible depuis [Crawler] > [Mapping de chemins] dans l'interface d'administration.

Approche 3 : Personnalisation complète via l'API de recherche
==============================================================

Scénario
--------

Vous souhaitez intégrer une fonction de recherche dans une application métier interne.
Vous voulez un contrôle total sur le design et la manière dont les résultats de recherche sont affichés.
Vous disposez de ressources en développement front-end.

Principes de base de l'API de recherche
-----------------------------------------

Fess fournit une API de recherche basée sur JSON.

::

    GET http://localhost:8080/api/v1/documents?q=検索キーワード

La réponse est au format JSON suivant.

.. code-block:: json

    {
      "record_count": 10,
      "page_count": 5,
      "data": [
        {
          "title": "ドキュメントタイトル",
          "url": "https://example.com/doc.html",
          "content_description": "...検索キーワードを含む本文の抜粋..."
        }
      ]
    }

Exemple d'implémentation en JavaScript
-----------------------------------------

Voici un exemple d'implémentation de base utilisant l'API de recherche.

.. code-block:: javascript

    async function searchFess(query) {
      const url = new URL('http://localhost:8080/api/v1/documents');
      url.searchParams.set('q', query);
      const response = await fetch(url);
      const data = await response.json();

      const results = data.data;
      const container = document.getElementById('search-results');
      container.textContent = '';

      results.forEach(item => {
        const div = document.createElement('div');
        const heading = document.createElement('h3');
        const link = document.createElement('a');
        link.href = item.url;
        link.textContent = item.title;
        heading.appendChild(link);
        const desc = document.createElement('p');
        desc.textContent = item.content_description;
        div.appendChild(heading);
        div.appendChild(desc);
        container.appendChild(div);
      });
    }

Paramètres supplémentaires de l'API
--------------------------------------

L'API de recherche permet de personnaliser le comportement de la recherche via divers paramètres.

.. list-table:: Principaux paramètres de l'API
   :header-rows: 1
   :widths: 20 50 30

   * - Paramètre
     - Description
     - Exemple
   * - ``q``
     - Mot-clé de recherche
     - ``q=Fess``
   * - ``num``
     - Nombre de résultats par page
     - ``num=20``
   * - ``start``
     - Position de départ des résultats
     - ``start=20``
   * - ``fields.label``
     - Filtrage par label
     - ``fields.label=intranet``
   * - ``sort``
     - Ordre de tri
     - ``sort=last_modified.desc``

En exploitant l'API, vous pouvez contrôler finement le filtrage, le tri et la pagination des résultats de recherche.

Quelle approche choisir ?
===========================

Les trois approches se choisissent en fonction de la situation.

**Choisir FSS lorsque :**

- Les ressources de développement sont limitées
- Vous souhaitez ajouter la recherche avec un minimum de modifications sur les pages existantes
- Une apparence standard de la fonction de recherche est suffisante

**Choisir la liaison par formulaire de recherche lorsque :**

- Le design de la page de recherche de Fess est suffisant
- Vous ne souhaitez pas utiliser JavaScript
- Il suffit d'ajouter un champ de recherche dans l'en-tête ou la barre latérale

**Choisir l'API de recherche lorsque :**

- Vous souhaitez personnaliser entièrement l'affichage des résultats de recherche
- Vous voulez l'intégrer dans une SPA (Single Page Application)
- Vous souhaitez appliquer une logique personnalisée aux résultats (filtrage, mise en surbrillance, etc.)
- Vous disposez de ressources en développement front-end

Les combinaisons sont possibles
---------------------------------

Ces approches ne sont pas mutuellement exclusives.
Par exemple, vous pouvez ajouter facilement une fonction de recherche sur la page d'accueil avec FSS, tout en offrant une interface personnalisée basée sur l'API sur une page de recherche dédiée. Cette combinaison est tout à fait valable.

Conclusion
==========

Dans cet article, nous avons présenté trois approches pour intégrer la fonction de recherche de Fess dans un site Web existant.

- **FSS** : ajout d'une fonction de recherche par simple insertion d'une balise JavaScript
- **Liaison par formulaire de recherche** : redirection vers la page de recherche de Fess via un formulaire HTML
- **API de recherche** : construction d'une expérience de recherche entièrement personnalisée via l'API JSON

Quelle que soit l'approche choisie, vous bénéficiez de la qualité de recherche fournie par le back-end de Fess.
Choisissez la méthode la plus adaptée en fonction de vos exigences et de vos ressources de développement.

Dans la prochaine partie, nous aborderons un scénario de recherche unifiée sur plusieurs sources de données, telles que des serveurs de fichiers et des services de stockage cloud.

Références
==========

- `Fess Site Search <https://github.com/codelibs/fess-site-search>`__

- `API de recherche Fess <https://fess.codelibs.org/ja/15.5/api/api-search.html>`__
