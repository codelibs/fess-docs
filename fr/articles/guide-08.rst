============================================================
Partie 8 : Cultiver la qualite de recherche -- Un cycle d'ajustement de recherche base sur les donnees de comportement des utilisateurs
============================================================

Introduction
============

Le deploiement d'un systeme de recherche ne marque pas la fin du travail.
Une fois que les utilisateurs commencent a utiliser la recherche en pratique, des retours tels que "je ne trouve pas les resultats attendus" ou "des resultats non pertinents apparaissent en haut" peuvent emerger.

Cet article presente un cycle d'ajustement de la qualite de recherche qui consiste a analyser les journaux de recherche pour identifier les problemes, mettre en oeuvre des ameliorations et mesurer leur efficacite.
Plutot que d'atteindre une qualite de recherche parfaite en une seule fois, il s'agit d'une approche d'amelioration continue basee sur les donnees.

Public cible
============

- Administrateurs de systemes de recherche
- Personnes souhaitant ameliorer la qualite de recherche
- Personnes exploitant deja Fess et ayant recu des retours d'utilisateurs

Le cycle d'ajustement de la qualite de recherche
=================================================

L'amelioration de la qualite de recherche suit un cycle en quatre etapes :

1. **Analyser** : Examiner les journaux de recherche et identifier les problemes
2. **Ameliorer** : Mettre en oeuvre des solutions pour les problemes identifies
3. **Verifier** : Confirmer l'efficacite des ameliorations
4. **Poursuivre** : Repeter le cycle pour ameliorer continuellement la qualite

Etape 1 : Analyse des journaux de recherche
============================================

Comment consulter les journaux de recherche
--------------------------------------------

Fess enregistre automatiquement le comportement de recherche des utilisateurs.
Vous pouvez consulter les journaux de recherche depuis [Informations systeme] > [Journal de recherche] dans la console d'administration.

Les journaux de recherche contiennent les informations suivantes :

- Mots-cles de recherche
- Date et heure de recherche
- Nombre de resultats de recherche
- Agent utilisateur

Tendances a surveiller
-----------------------

Lors de l'analyse des journaux de recherche, certaines tendances meritent une attention particuliere.

**Requetes sans resultat**

Il s'agit de requetes qui ne retournent aucun resultat.
L'information recherchee par l'utilisateur peut ne pas exister, ou les mots-cles de recherche peuvent ne pas correspondre de maniere appropriee.

Par exemple, une recherche sur "voyage d'entreprise" ne retourne aucun resultat, mais un document intitule "activite recreative pour les employes" existe.
Cela peut etre resolu en configurant des synonymes.

**Requetes a haute frequence**

Les mots-cles frequemment recherches representent des besoins d'information importants pour l'organisation.
Verifiez si des resultats pertinents s'affichent en tete pour ces requetes.

**Journaux de clics**

Il s'agit des enregistrements indiquant quels liens dans les resultats de recherche ont ete cliques.
Si les premiers resultats ne sont pas cliques et que seuls les resultats de rang inferieur le sont, il y a une marge d'amelioration dans le classement.

Etape 2 : Mise en oeuvre des ameliorations
===========================================

En vous basant sur les resultats de l'analyse, mettez en oeuvre les ameliorations suivantes de maniere combinee.

Configuration des synonymes
----------------------------

Enregistrez des synonymes pour gerer les variations d'ecriture et les abreviations.

Configurez-les en selectionnant le dictionnaire de synonymes depuis [Systeme] > [Dictionnaire] dans la console d'administration.

Exemple de configuration :

::

    社員旅行,従業員レクリエーション,社内イベント
    PC,パソコン,コンピュータ
    AWS,Amazon Web Services
    k8s,Kubernetes

En configurant des synonymes, la recherche d'un terme retournera egalement les documents contenant ses synonymes.

Configuration de Key Match
--------------------------

Cette fonctionnalite affiche un document specifique en premiere position des resultats pour un mot-cle donne.

Configurez-la depuis [Crawler] > [Key Match] dans la console d'administration.

Par exemple, vous pouvez configurer la page du manuel de notes de frais pour qu'elle apparaisse en premiere position lorsque les utilisateurs recherchent "notes de frais."

.. list-table:: Exemple de configuration Key Match
   :header-rows: 1
   :widths: 30 50 20

   * - Terme de recherche
     - Requete
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

Cette fonctionnalite ajuste le score global des documents correspondant a des conditions specifiques.

Configurez-la depuis [Crawler] > [Document Boost] dans la console d'administration.

Par exemple, les strategies de boost suivantes peuvent etre envisagees :

- Augmenter le score des manuels officiels (site du portail)
- Prioriser les documents avec des dates de derniere modification plus recentes
- Augmenter le score des documents portant un label specifique (documents officiels)

Configuration des requetes associees
-------------------------------------

Cette fonctionnalite suggere des mots-cles associes sur la page de resultats de recherche.
Elle aide les utilisateurs a affiner leur recherche ou a rechercher sous un angle different.

Configurez-la depuis [Crawler] > [Requete associee] dans la console d'administration.

Exemple de configuration :

::

    「VPN」→ 関連クエリ: 「VPN接続方法」「リモートワーク」「社外アクセス」

Configuration des mots vides
-----------------------------

Configurez les mots qui doivent etre ignores lors de la recherche.
Les particules courantes telles que "no", "wa" et "wo" sont traitees par defaut, mais vous pouvez ajouter des mots parasites specifiques a votre secteur si necessaire.

Configurez-les en selectionnant le dictionnaire de mots vides depuis [Systeme] > [Dictionnaire] dans la console d'administration.

Etape 3 : Verification de l'efficacite
=======================================

Apres avoir mis en oeuvre les ameliorations, verifiez leur efficacite.

Methodes de verification
-------------------------

**Evolution du taux de requetes sans resultat**

Verifiez comment la proportion de requetes sans resultat a evolue avant et apres l'amelioration.
Si le taux de requetes sans resultat a diminue apres l'ajout de synonymes ou la configuration de Key Match, vous pouvez conclure que l'amelioration a ete efficace.

**Evolution de la position des clics**

Verifiez la distribution de la position dans les resultats de recherche ou les clics sont effectues.
Si la proportion de clics sur les premiers resultats a augmente, vous pouvez conclure que le classement s'est ameliore.

**Verification des mots populaires**

Verifiez les mots populaires affiches sur la page de recherche et les mots-cles frequemment recherches agreges a partir des journaux de recherche.
Il est egalement efficace de verifier manuellement si des resultats pertinents sont retournes en recherchant les mots populaires.

Etape 4 : Amelioration continue
================================

L'ajustement de la qualite de recherche n'est pas une tache ponctuelle.

Etablissement d'un cycle operationnel
--------------------------------------

Nous recommandons d'etablir un cycle operationnel tel que le suivant.

.. list-table:: Exemple de cycle d'ajustement
   :header-rows: 1
   :widths: 25 35 40

   * - Frequence
     - Action
     - Details
   * - Hebdomadaire
     - Verifier les requetes sans resultat
     - Verifier s'il y a de nouvelles requetes sans resultat et les traiter avec des synonymes ou Key Match
   * - Mensuelle
     - Analyse globale des journaux de recherche
     - Examiner les tendances des requetes a haute frequence, des taux de clics et des taux de requetes sans resultat
   * - Trimestrielle
     - Revue comprehensive
     - Realiser une evaluation globale de la qualite de recherche et formuler un plan d'amelioration

Retours des utilisateurs
-------------------------

En plus de l'analyse des journaux, les retours des utilisateurs reels constituent egalement une contribution importante pour l'amelioration.
Mettez en place un mecanisme pour recueillir des retours tels que "je n'ai pas pu trouver ce que je cherchais avec ce mot-cle" ou "ce resultat m'a ete utile."

Resume
======

Cet article a presente un cycle d'ajustement pour ameliorer continuellement la qualite de recherche.

- Analyse des journaux de recherche (requetes sans resultat, requetes a haute frequence, journaux de clics)
- Ameliorations par les synonymes, Key Match, Document Boost et requetes associees
- Methodes de verification de l'efficacite des ameliorations
- Etablissement d'un cycle operationnel continu

Cultivons la qualite de recherche par une amelioration basee sur les donnees, en passant d'une "recherche utilisee" a une "recherche utile."

Le prochain article traitera de la construction d'une infrastructure de recherche dans des environnements multilingues.

References
==========

- `Fess Journal de recherche <https://fess.codelibs.org/ja/15.5/admin/searchlog.html>`__

- `Fess Gestion des dictionnaires <https://fess.codelibs.org/ja/15.5/admin/dict.html>`__
