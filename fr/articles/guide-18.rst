===========================================
Partie 18 : Fondamentaux de la recherche IA
===========================================

Introduction
=============

Dans les articles précédents, nous nous sommes concentrés sur la recherche en texte intégral basée sur les mots-clés.
La recherche en texte intégral est très efficace lorsque les utilisateurs peuvent saisir les mots-clés appropriés.
Cependant, il existe des cas où la recherche par mots-clés seule ne peut pas répondre adéquatement à des besoins tels que "je ne sais pas quels mots-clés utiliser" ou "je souhaite obtenir une réponse à une question conceptuelle".

Cet article organise le spectre des technologies de recherche et explique comment la recherche évolue de la recherche par mots-clés vers la recherche sémantique.

Public cible
=============

- Personnes intéressées par la recherche IA qui souhaitent organiser les concepts
- Personnes envisageant l'introduction de la recherche sémantique
- Personnes souhaitant comprendre les fonctionnalités liées à l'IA de Fess

Spectre des technologies de recherche
=======================================

Les technologies de recherche forment un spectre allant du simple au plus avancé, comme présenté ci-dessous.

.. list-table:: Spectre des technologies de recherche
   :header-rows: 1
   :widths: 20 35 45

   * - Technologie
     - Mécanisme
     - Caractéristiques
   * - Recherche par mots-clés
     - Compare les termes saisis avec les termes des documents
     - Rapide et fiable. Nécessite une correspondance exacte des termes
   * - Recherche floue
     - Compare également les termes ayant une orthographe similaire
     - Gestion des fautes de frappe
   * - Recherche par synonymes
     - Étend les synonymes pour la comparaison
     - Gestion des variantes de notation (configuration manuelle)
   * - Recherche sémantique
     - Compare sur la base de la similarité sémantique
     - Trouve des documents liés même sans correspondance de termes
   * - Recherche hybride
     - Combinaison de la recherche par mots-clés et sémantique
     - Exploite les forces des deux approches

Limites de la recherche par mots-clés
=======================================

La recherche par mots-clés est efficace dans de nombreuses situations, mais ses limites apparaissent dans les cas suivants.

Décalage de vocabulaire
-------------------------

Cela se produit lorsque les mots utilisés par les utilisateurs diffèrent de ceux utilisés dans les documents.

Exemple : Même si un utilisateur recherche "je veux changer la destination du virement de mon salaire", si le document interne utilise le terme "procédure de changement de compte salarial", les mots-clés peuvent ne pas correspondre.

Cela peut être partiellement résolu avec les synonymes (voir Partie 8), mais il n'est pas réaliste d'enregistrer toutes les combinaisons de vocabulaire possibles à l'avance.

Recherche conceptuelle
------------------------

C'est le cas où les utilisateurs souhaitent effectuer une recherche par concept plutôt que par mots-clés spécifiques, comme "règles internes sur le télétravail".
Dans ce cas, divers documents liés peuvent être pertinents, y compris ceux portant sur le "travail à domicile", le "télétravail", les "règles de présence au bureau" et la "gestion du temps de travail".

Fonctionnement de la recherche sémantique
============================================

Représentation vectorielle (Embedding)
-----------------------------------------

Le fondement de la recherche sémantique est la conversion du texte en "vecteurs (tableaux de nombres)".
Ces vecteurs sont des représentations mathématiques du "sens" du texte.

Les textes ayant des significations similaires sont placés près les uns des autres dans l'espace vectoriel.
Par exemple, les vecteurs de "chien" et "animal de compagnie" sont proches, tandis que les vecteurs de "chien" et "automobile" sont éloignés.

Fonctionnement de la recherche
---------------------------------

1. L'utilisateur saisit une requête de recherche
2. La requête est convertie en vecteur
3. La similarité avec les vecteurs de documents dans l'index est calculée
4. Les documents sont renvoyés par ordre de similarité décroissante

Cela permet de trouver des documents sémantiquement liés même lorsque les mots-clés ne correspondent pas exactement.

Recherche sémantique dans Fess
=================================

Fess peut réaliser une recherche basée sur les vecteurs grâce à des plugins de recherche sémantique.

Activation de la recherche sémantique
----------------------------------------

1. Installer le plugin de recherche sémantique
2. Configurer le modèle d'embedding
3. Reconstruire l'index (vectoriser les documents existants)

Choix du modèle d'embedding
------------------------------

Sélectionnez un modèle (modèle d'embedding) pour convertir le texte en vecteurs.

Les critères de sélection sont les suivants :

- **Support linguistique** : Capacité à traiter correctement la langue cible
- **Précision** : Qualité des vecteurs (précision de la capture sémantique)
- **Vitesse** : Temps nécessaire à la conversion
- **Coût** : Frais d'utilisation de l'API, exigences matérielles

Recherche hybride : Rank Fusion
==================================

La recherche sémantique est puissante, mais pas omnipotente.
Pour la recherche de noms propres ou dans les cas nécessitant une correspondance exacte, la recherche par mots-clés est plus appropriée.

Le concept de recherche hybride
---------------------------------

La recherche hybride exécute à la fois la recherche par mots-clés et la recherche sémantique, puis intègre les résultats.

Fess utilise le Rank Fusion pour fusionner les résultats de différentes méthodes de recherche.
Concrètement, l'algorithme RRF (Reciprocal Rank Fusion) garantit que les documents bien classés dans les deux résultats de recherche se retrouvent finalement en tête du classement.

Avantages de la recherche hybride
------------------------------------

- Combine la "fiabilité" de la recherche par mots-clés avec la "flexibilité" de la recherche sémantique
- Les noms propres sont couverts par la recherche par mots-clés
- Les recherches conceptuelles sont couvertes par la recherche sémantique
- La qualité globale de la recherche s'améliore par rapport à l'utilisation d'une seule méthode

Critères d'adoption
=====================

La recherche sémantique ne doit pas nécessairement être introduite dans tous les environnements.

Cas où l'adoption devrait être envisagée
-------------------------------------------

- Il y a de nombreuses "requêtes sans résultats" dans les journaux de recherche
- Les utilisateurs signalent qu'ils "ne connaissent pas les bons mots-clés"
- Vous souhaitez prendre en charge les questions en langage naturel (un prérequis pour le RAG dans la Partie 19)
- Vous souhaitez améliorer la recherche interlinguistique pour les documents multilingues

Cas où elle n'est pas encore nécessaire
-----------------------------------------

- Une qualité de recherche suffisante est obtenue avec la recherche par mots-clés + synonymes
- Le nombre de documents est faible et les utilisateurs connaissent les mots-clés appropriés
- Les ressources de calcul (GPU ou coûts d'API cloud) sont limitées

Adoption progressive
----------------------

1. D'abord, améliorer la qualité avec la recherche par mots-clés + synonymes (Partie 8)
2. Si les requêtes sans résultats restent fréquentes, envisager la recherche sémantique
3. Utiliser la recherche hybride pour bénéficier des deux approches

Résumé
=======

Cet article a organisé le chemin d'évolution de la recherche par mots-clés vers la recherche sémantique.

- Le spectre des technologies de recherche (mots-clés -> floue -> synonymes -> sémantique -> hybride)
- Le fonctionnement de la recherche sémantique (représentation vectorielle et calcul de similarité)
- La recherche sémantique et la recherche hybride dans Fess (Rank Fusion)
- Les critères d'adoption et une approche progressive

Dans le prochain article, nous développerons davantage la recherche sémantique et construirons un assistant IA utilisant le RAG.

Références
==========

- `Fonctionnalités de recherche IA de Fess <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `Recherche vectorielle OpenSearch <https://opensearch.org/docs/latest/search-plugins/knn/>`__
