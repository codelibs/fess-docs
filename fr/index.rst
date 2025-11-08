=========================================
Serveur de recherche plein texte open source Fess
=========================================

Aperçu
====

Fess est un «\ **serveur de recherche plein texte facile à construire en 5 minutes**\ ».

.. figure:: ../resources/images/ja/demo-1.png
   :scale: 100%
   :alt: Démo standard
   :figclass: side-by-side
   :target: https://search.n2sm.co.jp/

   Démo standard

.. figure:: ../resources/images/ja/demo-3.png
   :scale: 100%
   :alt: Démo de recherche sur site
   :figclass: side-by-side
   :target: https://www.n2sm.net/search.html?q=Fess

   Démo de recherche sur site

.. figure:: ../resources/images/ja/demo-2.png
   :scale: 100%
   :alt: Code Search
   :figclass: side-by-side
   :target: https://codesearch.codelibs.org/

   Recherche de code source

.. figure:: ../resources/images/ja/demo-4.png
   :scale: 100%
   :alt: Document Search
   :figclass: side-by-side
   :target: https://docsearch.codelibs.org/

   Recherche de documents

Il peut être exécuté sur n'importe quel système d'exploitation avec un environnement d'exécution Java ou Docker.
Fess est fourni sous licence Apache et peut être utilisé gratuitement (logiciel libre).


Téléchargement
============

- :doc:`Fess 15.3.0 <downloads>` (packages zip/rpm/deb)

Caractéristiques
====

-  Fourni sous licence Apache (gratuit car logiciel libre)

-  Crawl du Web, des systèmes de fichiers, des dossiers partagés Windows et des bases de données

-  Prise en charge de nombreux formats de fichiers tels que MS Office (Word/Excel/PowerPoint) et PDF

-  Indépendant du système d'exploitation (construit sur Java)

-  Fourniture de JavaScript pour l'intégration dans des sites existants

-  Utilisation d'OpenSearch ou Elasticsearch comme moteur de recherche

-  Possibilité de rechercher des sites avec authentification BASIC/DIGEST/NTLM/FORM

-  Possibilité de différencier les résultats de recherche en fonction de l'état de connexion

-  Authentification unique (SSO) utilisant Active Directory, SAML, etc.

-  Recherche d'informations géographiques en lien avec des cartes

-  Configuration des cibles de crawl et édition de l'écran de recherche possible dans le navigateur

-  Classification des résultats de recherche par étiquetage

-  Ajout d'informations dans les en-têtes de requête, configuration de domaines en double, transformation des chemins dans les résultats de recherche

-  Possibilité d'intégration avec des systèmes externes grâce à la sortie des résultats de recherche au format JSON

-  Agrégation des journaux de recherche et de clics

-  Support des facettes et du drill-down

-  Fonctionnalités d'autocomplétion et de suggestion

-  Fonction d'édition de dictionnaire utilisateur et de dictionnaire de synonymes

-  Fonction d'affichage du cache et des vignettes des résultats de recherche

-  Fonction proxy pour les résultats de recherche

-  Compatible avec les smartphones (Responsive Web Design)

-  Intégration avec des systèmes externes via des jetons d'accès

-  Prise en charge de l'extraction de texte externe comme l'OCR

-  Conception flexible pour répondre à divers besoins

Actualités
========

2025-10-25
    `Version Fess 15.3.0 <https://github.com/codelibs/fess/releases/tag/fess-15.3.0>`__

2025-09-04
    `Version Fess 15.2.0 <https://github.com/codelibs/fess/releases/tag/fess-15.2.0>`__

2025-07-20
    `Version Fess 15.1.0 <https://github.com/codelibs/fess/releases/tag/fess-15.1.0>`__

2025-06-22
    `Version Fess 15.0.0 <https://github.com/codelibs/fess/releases/tag/fess-15.0.0>`__

2025-05-24
    `Version Fess 14.19.2 <https://github.com/codelibs/fess/releases/tag/fess-14.19.2>`__

Pour les anciennes actualités, veuillez consulter :doc:`ici <news>`.

Forum
==========

Si vous avez des questions, veuillez utiliser le `forum <https://discuss.codelibs.org/c/FessJA/>`__.

Support commercial
============

Fess est un produit open source fourni sous licence Apache et peut être utilisé librement et gratuitement à des fins personnelles ou commerciales.

Si vous avez besoin de services de support pour la personnalisation, l'introduction ou la construction de Fess, veuillez consulter le \ `support commercial (payant) <https://www.n2sm.net/products/n2search.html>`__\.
Le support commercial prend également en charge l'optimisation des performances, notamment l'amélioration de la qualité de recherche et de la vitesse de crawl.

- `N2 Search <https://www.n2sm.net/products/n2search.html>`__ (package commercial optimisé de Fess)

- `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__ (service alternatif à Google Site Search)

- :doc:`Divers services de support <support-services>`


Fess Site Search
================

Le projet CodeLibs propose `Fess Site Search (FSS) <https://fss-generator.codelibs.org/ja/>`__.
Il suffit de placer du JavaScript sur un site existant pour intégrer la page de recherche Fess.
En utilisant FSS, vous pouvez facilement migrer depuis Google Site Search ou Yahoo! Custom Search.
Si vous avez besoin d'un serveur Fess abordable, veuillez consulter `N2 Search Super Lite <https://www.n2sm.net/services/n2search-asp-lite.html>`__.

Plugins Data Store
====================

- `Confluence/Jira <https://github.com/codelibs/fess-ds-atlassian>`__
- `Box <https://github.com/codelibs/fess-ds-box>`__
- `CSV <https://github.com/codelibs/fess-ds-csv>`__
- `Database <https://github.com/codelibs/fess-ds-db>`__
- `Dropbox <https://github.com/codelibs/fess-ds-dropbox>`__
- `Elasticsearch <https://github.com/codelibs/fess-ds-elasticsearch>`__
- `Git <https://github.com/codelibs/fess-ds-git>`__
- `Gitbucket <https://github.com/codelibs/fess-ds-gitbucket>`__
- `G Suite <https://github.com/codelibs/fess-ds-gsuite>`__
- `JSON <https://github.com/codelibs/fess-ds-json>`__
- `Office 365 <https://github.com/codelibs/fess-ds-office365>`__
- `S3 <https://github.com/codelibs/fess-ds-s3>`__
- `Salesforce <https://github.com/codelibs/fess-ds-salesforce>`__
- `SharePoint <https://github.com/codelibs/fess-ds-sharepoint>`__
- `Slack <https://github.com/codelibs/fess-ds-slack>`__

Plugins Theme
===============

- `Simple <https://github.com/codelibs/fess-theme-simple>`__
- `Classic <https://github.com/codelibs/fess-theme-classic>`__

Plugins Ingester
==================

- `Logger <https://github.com/codelibs/fess-ingest-logger>`__
- `NDJSON <https://github.com/codelibs/fess-ingest-ndjson>`__

Plugins Script
==================

- `Groovy <https://github.com/codelibs/fess-script-groovy>`__
- `OGNL <https://github.com/codelibs/fess-script-ognl>`__

Projets connexes
================

- `Code Search <https://github.com/codelibs/docker-codesearch>`__
- `Document Search <https://github.com/codelibs/docker-docsearch>`__
- `Fione <https://github.com/codelibs/docker-fione>`__
- `Form Assist <https://github.com/codelibs/docker-formassist>`__


.. |image0| image:: ../resources/images/ja/demo-1.png
.. |image1| image:: ../resources/images/ja/demo-2.png
.. |image2| image:: ../resources/images/ja/demo-3.png
.. |image3| image:: ../resources/images/ja/n2search_225x50.png
   :target: https://www.n2sm.net/products/n2search.html
.. |image4| image:: ../resources/images/ja/n2search_b.png


.. toctree::
   :hidden:

   overview
   basic
   documentation
   tutorial
   development
   others
   archives


