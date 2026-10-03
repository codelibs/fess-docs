====================
Rapport de documents
====================

Présentation
============

La page Rapport de documents aide à faire le ménage dans les serveurs de fichiers crawlés et autres.
Elle liste les documents au contenu identique et ceux qui n'ont pas été modifiés depuis longtemps ;
chaque liste peut être téléchargée en CSV.

Pour ouvrir la page, sélectionnez [Informations système > Rapport de documents] dans le menu de
gauche. La consultation nécessite le rôle ``admin-docreport`` ou ``admin-docreport-view``. La page ne
fait qu'afficher et télécharger des rapports ; elle ne modifie aucun document.

Les deux onglets peuvent être restreints avec « Préfixe d’URL », par exemple ``smb://server/share/``.

Doublons
========

Les documents au contenu identique ou presque identique sont regroupés, le groupe le plus grand en
premier. Les groupes reposent sur la signature de contenu calculée à l'indexation
(``content_minhash_bits``, la même qui regroupe les résultats de recherche en double) ; aucune
réindexation n'est donc nécessaire. Les documents dont le contenu ne contient aucun mot (comme les
fichiers vides) sont exclus.

L'écran affiche au plus ``docreport.duplicate.group.size`` (par défaut : 100) groupes et au plus
``docreport.duplicate.docs.size`` (par défaut : 10) documents par groupe. Utilisez [Télécharger le
CSV] pour obtenir tous les groupes. Le CSV lit tous les groupes, même sur un grand index, avec les
colonnes
``group, groupSize, url, title, filename, contentLength, lastModified, owner, lastModifier, clickCount, docId``.

.. note::

   Sur un index qui ne conserve pas la signature de contenu (les mappings ``cloud`` et ``aws``), le
   rapport de doublons n'est pas disponible.

Documents inactifs
==================

Les documents dont la dernière modification est antérieure au nombre de jours indiqué (« Non modifiés
depuis (jours) », 365 par défaut d'après ``docreport.dormant.days``) sont listés, du plus ancien au
plus récent. Les documents sans date de dernière modification ne sont pas listés. Avec « Jamais
ouverts depuis les résultats de recherche », les documents cliqués depuis les résultats de recherche
sont exclus.

L'écran affiche le nombre de documents correspondants, leur taille totale et une liste paginée. La
pagination s'arrête à ``indexer.max.result.window.size`` ; utilisez [Télécharger le CSV] pour obtenir
les documents au-delà.

Paramètres
==========

Les réglages suivants de ``fess_config.properties`` ajustent le rapport.

.. list-table::
   :header-rows: 1
   :widths: 40 45 15

   * - Propriété
     - Description
     - Défaut
   * - ``docreport.duplicate.group.size``
     - Nombre maximal de groupes de doublons affichés par l’écran
     - ``100``
   * - ``docreport.duplicate.docs.size``
     - Nombre maximal de documents listés par groupe à l’écran
     - ``10``
   * - ``docreport.duplicate.export.page.size``
     - Nombre de signatures de contenu lues par requête lors du téléchargement du CSV
     - ``10000``
   * - ``docreport.dormant.days``
     - Nombre de jours par défaut depuis la dernière modification au-delà duquel un document est inactif
     - ``365``
