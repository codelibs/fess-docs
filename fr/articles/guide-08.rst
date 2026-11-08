===========================================
Partie 8 : Cultiver la qualité de recherche
===========================================

Introduction
============

Le déploiement d'un système de recherche ne marque pas la fin du travail.
Une fois que les utilisateurs commencent à utiliser la recherche en pratique, des retours tels que "je ne trouve pas les résultats attendus" ou "des résultats non pertinents apparaissent en haut" peuvent émerger.

Cet article présente un cycle d'ajustement de la qualité de recherche qui consiste à analyser les journaux de recherche pour identifier les problèmes, mettre en œuvre des améliorations et mesurer leur efficacité.
Plutôt que d'atteindre une qualité de recherche parfaite en une seule fois, il s'agit d'une approche d'amélioration continue basée sur les données.

Public cible
============

- Administrateurs de systèmes de recherche
- Personnes souhaitant améliorer la qualité de recherche
- Personnes exploitant déjà Fess et ayant reçu des retours d'utilisateurs

Le cycle d'ajustement de la qualité de recherche
=================================================

L'amélioration de la qualité de recherche suit un cycle en quatre étapes :

1. **Analyser** : Examiner les journaux de recherche et identifier les problèmes
2. **Améliorer** : Mettre en œuvre des solutions pour les problèmes identifiés
3. **Vérifier** : Confirmer l'efficacité des améliorations
4. **Poursuivre** : Répéter le cycle pour améliorer continuellement la qualité

Étape 1 : Analyse des journaux de recherche
============================================

Comment consulter les journaux de recherche
--------------------------------------------

Fess enregistre automatiquement le comportement de recherche des utilisateurs.
Vous pouvez consulter les journaux de recherche depuis [Informations système] > [Journal de recherche] dans la console d'administration.

Les journaux de recherche contiennent les informations suivantes :

- Mots-clés de recherche
- Date et heure de recherche
- Nombre de résultats de recherche
- Agent utilisateur

Tendances à surveiller
-----------------------

Lors de l'analyse des journaux de recherche, certaines tendances méritent une attention particulière.

**Requêtes sans résultat**

Il s'agit de requêtes qui ne retournent aucun résultat.
L'information recherchée par l'utilisateur peut ne pas exister, ou les mots-clés de recherche peuvent ne pas correspondre de manière appropriée.

Par exemple, une recherche sur "voyage d'entreprise" ne retourne aucun résultat, mais un document intitulé "activité récréative pour les employés" existe.
Cela peut être résolu en configurant des synonymes.

**Requêtes à haute fréquence**

Les mots-clés fréquemment recherchés représentent des besoins d'information importants pour l'organisation.
Vérifiez si des résultats pertinents s'affichent en tête pour ces requêtes.

**Journaux de clics**

Il s'agit des enregistrements indiquant quels liens dans les résultats de recherche ont été cliqués.
Si les premiers résultats ne sont pas cliqués et que seuls les résultats de rang inférieur le sont, il y a une marge d'amélioration dans le classement.

Étape 2 : Mise en œuvre des améliorations
===========================================

En vous basant sur les résultats de l'analyse, mettez en œuvre les améliorations suivantes de manière combinée.

Configuration des synonymes
----------------------------

Enregistrez des synonymes pour gérer les variations d'écriture et les abréviations.

Configurez-les en sélectionnant le dictionnaire de synonymes depuis [Système] > [Dictionnaire] dans la console d'administration.

Exemple de configuration :

::

    社員旅行,従業員レクリエーション,社内イベント
    PC,パソコン,コンピュータ
    AWS,Amazon Web Services
    k8s,Kubernetes

En configurant des synonymes, la recherche d'un terme retournera également les documents contenant ses synonymes.

Configuration de Key Match
--------------------------

Cette fonctionnalité affiche un document spécifique en première position des résultats pour un mot-clé donné.

Configurez-la depuis [Crawler] > [Key Match] dans la console d'administration.

Par exemple, vous pouvez configurer la page du manuel de notes de frais pour qu'elle apparaisse en première position lorsque les utilisateurs recherchent "notes de frais."

.. list-table:: Exemple de configuration Key Match
   :header-rows: 1
   :widths: 30 50 20

   * - Terme de recherche
     - Requête
     - Valeur de boost
   * - 経費精算
     - url:https://portal/manual/expense.html
     - 100
   * - 有給申請
     - url:https://portal/manual/paid-leave.html
     - 100
   * - VPN接続
     - url:https://portal/manual/vpn-setup.html
     - 100

Configuration de Document Boost
--------------------------------

Cette fonctionnalité ajuste le score global des documents correspondant à des conditions spécifiques.

Configurez-la depuis [Crawler] > [Document Boost] dans la console d'administration.

Par exemple, les stratégies de boost suivantes peuvent être envisagées :

- Augmenter le score des manuels officiels (site du portail)
- Prioriser les documents avec des dates de dernière modification plus récentes
- Augmenter le score des documents portant un label spécifique (documents officiels)

Configuration des requêtes associées
-------------------------------------

Cette fonctionnalité suggère des mots-clés associés sur la page de résultats de recherche.
Elle aide les utilisateurs à affiner leur recherche ou à rechercher sous un angle différent.

Configurez-la depuis [Crawler] > [Requête associée] dans la console d'administration.

Exemple de configuration :

::

    「VPN」→ 関連クエリ: 「VPN接続方法」「リモートワーク」「社外アクセス」

Configuration des mots vides
-----------------------------

Configurez les mots qui doivent être ignorés lors de la recherche.
Les particules courantes telles que "no", "wa" et "wo" sont traitées par défaut, mais vous pouvez ajouter des mots parasites spécifiques à votre secteur si nécessaire.

Configurez-les en sélectionnant le dictionnaire de mots vides depuis [Système] > [Dictionnaire] dans la console d'administration.

Étape 3 : Vérification de l'efficacité
=======================================

Après avoir mis en œuvre les améliorations, vérifiez leur efficacité.

Méthodes de vérification
-------------------------

**Évolution du taux de requêtes sans résultat**

Vérifiez comment la proportion de requêtes sans résultat a évolué avant et après l'amélioration.
Si le taux de requêtes sans résultat a diminué après l'ajout de synonymes ou la configuration de Key Match, vous pouvez conclure que l'amélioration a été efficace.

**Évolution de la position des clics**

Vérifiez la distribution de la position dans les résultats de recherche où les clics sont effectués.
Si la proportion de clics sur les premiers résultats a augmenté, vous pouvez conclure que le classement s'est amélioré.

**Vérification des mots populaires**

Vérifiez les mots populaires affichés sur la page de recherche et les mots-clés fréquemment recherchés agrégés à partir des journaux de recherche.
Il est également efficace de vérifier manuellement si des résultats pertinents sont retournés en recherchant les mots populaires.

Étape 4 : Amélioration continue
================================

L'ajustement de la qualité de recherche n'est pas une tâche ponctuelle.

Établissement d'un cycle opérationnel
--------------------------------------

Nous recommandons d'établir un cycle opérationnel tel que le suivant.

.. list-table:: Exemple de cycle d'ajustement
   :header-rows: 1
   :widths: 25 35 40

   * - Fréquence
     - Action
     - Détails
   * - Hebdomadaire
     - Vérifier les requêtes sans résultat
     - Vérifier s'il y a de nouvelles requêtes sans résultat et les traiter avec des synonymes ou Key Match
   * - Mensuelle
     - Analyse globale des journaux de recherche
     - Examiner les tendances des requêtes à haute fréquence, des taux de clics et des taux de requêtes sans résultat
   * - Trimestrielle
     - Revue compréhensive
     - Réaliser une évaluation globale de la qualité de recherche et formuler un plan d'amélioration

Retours des utilisateurs
-------------------------

En plus de l'analyse des journaux, les retours des utilisateurs réels constituent également une contribution importante pour l'amélioration.
Mettez en place un mécanisme pour recueillir des retours tels que "je n'ai pas pu trouver ce que je cherchais avec ce mot-clé" ou "ce résultat m'a été utile."

Résumé
======

Cet article a présenté un cycle d'ajustement pour améliorer continuellement la qualité de recherche.

- Analyse des journaux de recherche (requêtes sans résultat, requêtes à haute fréquence, journaux de clics)
- Améliorations par les synonymes, Key Match, Document Boost et requêtes associées
- Méthodes de vérification de l'efficacité des améliorations
- Établissement d'un cycle opérationnel continu

Cultivons la qualité de recherche par une amélioration basée sur les données, en passant d'une "recherche utilisée" à une "recherche utile."

Le prochain article traitera de la construction d'une infrastructure de recherche dans des environnements multilingues.

Références
==========

- `Fess Journal de recherche <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `Fess Gestion des dictionnaires <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__
