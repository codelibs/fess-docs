================
Requête associée
================

Présentation
============

Cette section explique la configuration des requêtes associées.
Vous pouvez améliorer les résultats de recherche avec les requêtes associées enregistrées.
Les requêtes associées peuvent être utilisées comme mots alternatifs pour les termes de recherche.


Gestion
=======

Affichage
---------

Pour ouvrir la page de liste pour configurer les requêtes associées illustrée ci-dessous, cliquez sur [Robot d'exploration > Requête associée] dans le menu de gauche.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Création de configuration
-------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration des requêtes associées.

|image1|

Paramètres de configuration
---------------------------

Terme de recherche
::::::::::::::::::

Spécifie le terme de recherche à faire correspondre avec la requête de recherche.

Requête
:::::::

Spécifie la requête.

Hôte virtuel
::::::::::::

Spécifie le nom d'hôte de l'hôte virtuel.
Pour plus de détails, consultez :doc:`Configuration de l'hôte virtuel dans le guide de configuration <../config/security-virtual-host>`.

Suppression de configuration
----------------------------

Cliquez sur le nom de la configuration dans la page de liste, puis cliquez sur le bouton Supprimer pour afficher l'écran de confirmation.
Appuyer sur le bouton Supprimer supprimera la configuration.

Générer à partir des journaux de recherche
------------------------------------------

Cliquez sur le bouton [Générer à partir des journaux de recherche] de la page de liste pour créer
des requêtes associées à partir des journaux de recherche récents. Une recherche que la même session
utilisateur lance peu après une autre (une faute de frappe suivie de sa correction, ou un terme
général suivi d'un terme plus précis) compte comme une reformulation. Pour les termes souvent
recherchés, les reformulations les plus fréquentes deviennent les requêtes associées du terme.

Les requêtes associées s'appliquent à tous et élargissent chaque recherche de leur terme ; la
génération est donc prudente :

- Seules les recherches visibles par un invité sont utilisées. Un journal de recherche n'est lu que
  si tous ses rôles satisfont ``suggest.search.log.permissions`` (le même réglage que la suggestion).
- Les termes contenant un filtre de champ comme ``label:"x"``, des opérateurs, des jokers,
  ``sort:`` ou un ``+`` / ``-`` initial ne sont pas utilisés.
- Les mots enregistrés dans [Suggérer > Mot incorrect] ne servent ni de termes ni de requêtes
  associées.
- Un terme et chacune de ses requêtes associées doivent provenir d'au moins
  ``related_query.generate.min.sessions`` sessions, et les reformulations doivent avoir des
  résultats.
- Les entrées sont générées séparément pour chaque hôte virtuel. Les journaux sans hôte virtuel sont
  traités comme l'hôte par défaut.
- Les termes qui ont déjà des requêtes associées ne sont pas modifiés (le résultat indique combien
  ont été ignorés), et pas plus d'entrées ne sont créées que le cache des requêtes associées ne peut
  en charger (``page.relatedquery.max.fetch.size``).

Les requêtes associées générées se modifient ou se suppriment comme celles saisies à la main. Elles
ne peuvent pas être générées tant que « Journal de recherche » ou « Journal utilisateur » est
désactivé dans [Système > Général], et une seconde exécution ne peut pas démarrer pendant qu'une
autre est en cours.

Les réglages suivants de ``fess_config.properties`` ajustent la génération.

.. list-table::
   :header-rows: 1
   :widths: 45 40 15

   * - Propriété
     - Description
     - Défaut
   * - ``related_query.generate.days``
     - Nombre de jours de journaux de recherche lus
     - ``30``
   * - ``related_query.generate.term.size``
     - Nombre maximal de termes par hôte virtuel
     - ``100``
   * - ``related_query.generate.query.size``
     - Nombre maximal de requêtes associées par terme
     - ``5``
   * - ``related_query.generate.min.sessions``
     - Nombre minimal de sessions où un terme et sa requête associée doivent apparaître
     - ``3``
   * - ``related_query.generate.session.interval``
     - Délai dans lequel une recherche compte comme reformulation (minutes)
     - ``10``
   * - ``related_query.generate.seed.log.size``
     - Nombre maximal de journaux de recherche lus par terme
     - ``1000``
   * - ``related_query.generate.seed.session.size``
     - Nombre maximal de sessions lues par terme
     - ``200``
   * - ``related_query.generate.log.fetch.size``
     - Nombre maximal de recherches suivantes lues par terme
     - ``2000``
   * - ``related_query.generate.query.min.length``
     - Longueur minimale d’un terme et d’une requête associée (caractères)
     - ``2``
   * - ``related_query.generate.query.max.length``
     - Longueur maximale d’un terme et d’une requête associée (caractères)
     - ``50``

.. |image0| image:: ../../../resources/images/en/15.9/admin/relatedquery-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/relatedquery-2.png
