====================
Journal de recherche
====================

Présentation
============

Les recherches, les clics et les favoris sont enregistrés. La page Journal de recherche affiche des
rapports d'analyse qui les agrègent, ainsi qu'une liste des journaux individuels.

Pour ouvrir la page, sélectionnez [Informations système > Journal de recherche] dans le menu de
gauche. L'onglet « Aperçu » s'affiche en premier. La consultation nécessite le rôle
``admin-searchlog`` ou ``admin-searchlog-view`` ; ``admin-searchlog-view`` ne permet pas de supprimer
des journaux.

Rapports d'analyse
==================

Période et filtres
------------------

En haut de chaque onglet, choisissez la période à agréger parmi « Aujourd’hui », « Hier »,
« 7 derniers jours », « 28 derniers jours » et « 90 derniers jours », ou indiquez une date de début
et de fin avec « Personnalisée » (366 jours au plus). Avec « Comparer à la période précédente », les
valeurs sont comparées à la période de même durée qui précède. Vous pouvez aussi choisir le type
d'accès et le nombre de lignes des tableaux. Les périodes et les intervalles des graphiques suivent
les jours calendaires du fuseau horaire du serveur.

Onglets
-------

- **Aperçu** : les recherches, les utilisateurs, le taux de zéro résultat, le taux de clics et le
  temps de réponse moyen, chacun avec un petit graphique de tendance et son évolution par rapport à la
  période précédente ; un graphique de tendance avec choix de la métrique (la période précédente est
  tracée en pointillés lors d'une comparaison) ; ainsi que les requêtes les plus fréquentes et les
  requêtes sans résultat.
- **Requêtes** : par requête, les recherches, les utilisateurs, le nombre moyen de résultats, les
  clics, le taux de clics et la position moyenne des clics. Il affiche aussi les requêtes sans
  résultat (avec la date de la dernière recherche) et les requêtes sans clic, qui avaient des
  résultats jamais ouverts.
- **Clics** : les URL les plus cliquées, les URL les plus ajoutées aux favoris, la distribution des
  positions de clic et la proportion de consultations de la page 2 et suivantes.
- **Performances** : le temps de réponse moyen, médian (p50), p95 et p99, la distribution des temps
  de réponse, les requêtes les plus lentes et le temps de requête.
- **Audience** : les utilisateurs nouveaux et récurrents, les types d'accès, les recherches par jour
  de la semaine et par heure, ainsi que les principaux user agents, référents, langues et hôtes
  virtuels. « Recherches par rôle et par groupe » affiche les recherches, les utilisateurs et le taux
  de zéro résultat de chaque rôle et groupe. Une recherche compte pour chaque rôle et groupe de
  l'utilisateur qui l'a lancée, de sorte que la somme des lignes peut dépasser le total. Aucun
  utilisateur individuel n'est affiché.
- **Chat IA** : les requêtes, les utilisateurs, le total de tokens, le temps de réponse moyen et le
  taux d'erreur du mode de recherche IA (chat RAG), avec les principaux utilisateurs et les requêtes
  par intention et par modèle. L'utilisation du chat est enregistrée tant que
  ``rag.chat.log.enabled`` (par défaut : ``true``) est activé. Les questions et les réponses ne sont
  pas enregistrées. Le nombre de tokens n'est enregistré que si le plugin LLM le communique.
- **Journaux** : la liste des journaux individuels ; voir « Liste des journaux » ci-dessous.

.. note::

   Les métriques de clics par requête et les requêtes sans clic ne comptent que les clics enregistrés
   depuis que le mot recherché est enregistré avec les clics (|Fess| 15.9 et ultérieur). Le total des
   clics et le taux de clics incluent les clics plus anciens. Certaines valeurs, comme le nombre
   d'utilisateurs, sont approximatives.

Examiner les requêtes sans résultat
-----------------------------------

Dans les onglets « Aperçu » et « Requêtes », cliquez sur une requête sans résultat pour ouvrir
l'onglet « Journaux » avec les journaux de recherche de cette requête, filtrés sur « Sans résultat
uniquement ». Vous voyez ainsi quelles recherches n'ont rien trouvé et pouvez ajouter des documents,
des synonymes ou des requêtes associées.

Télécharger le CSV
------------------

Chaque tableau et chaque graphique des rapports d'analyse a un lien CSV qui télécharge ce qu'il agrège
pour la période, la comparaison, le type d'accès et la taille en cours. La barre de filtres a aussi
un lien vers un CSV des métriques. Les nombres sont écrits tels quels (proportions de 0 à 1, durées
en millisecondes). Un graphique comparé reçoit une colonne supplémentaire ``<series>_previous``.

Liste des journaux
==================

L'onglet « Journaux » liste les journaux de recherche, de clics, de favoris et utilisateur. Vous
pouvez les filtrer par type de journal, ID de requête, ID utilisateur, plage horaire, type d'accès et
mot recherché, et les journaux de recherche aussi par nombre de résultats (« Tous », « Sans résultat
uniquement », « Un résultat ou plus »). Pour voir les détails d'un journal, cliquez dessus.

|image0|

Cliquez sur [Télécharger le CSV] pour télécharger en CSV les journaux qui correspondent au filtre en
cours, du plus récent au plus ancien et sans limite de lignes. La ligne d'en-tête contient les noms
des champs ; elle ne dépend donc pas de la langue de l'interface.

Les fichiers CSV, y compris ceux des rapports d'analyse, sont écrits dans l'encodage de
``csv.file.encoding`` ; un fichier UTF-8 commence par une marque d'ordre des octets. Une valeur qui
commence par ``=``, ``+``, ``-``, ``@``, une tabulation ou un retour chariot reçoit un ``'`` initial,
afin qu'un tableur ne l'exécute pas comme une formule.

Détails
-------

Cliquez sur un journal de la liste pour afficher ses détails.

|image1|


.. |image0| image:: ../../../resources/images/en/15.9/admin/searchlog-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/searchlog-2.png
