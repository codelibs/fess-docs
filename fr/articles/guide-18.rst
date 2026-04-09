============================================================
Partie 18 : Fondamentaux de la recherche IA -- De la recherche par mots-cles a la recherche semantique
============================================================

Introduction
=============

Dans les articles precedents, nous nous sommes concentres sur la recherche en texte integral basee sur les mots-cles.
La recherche en texte integral est tres efficace lorsque les utilisateurs peuvent saisir les mots-cles appropries.
Cependant, il existe des cas ou la recherche par mots-cles seule ne peut pas repondre adequatement a des besoins tels que "je ne sais pas quels mots-cles utiliser" ou "je souhaite obtenir une reponse a une question conceptuelle".

Cet article organise le spectre des technologies de recherche et explique comment la recherche evolue de la recherche par mots-cles vers la recherche semantique.

Public cible
=============

- Personnes interessees par la recherche IA qui souhaitent organiser les concepts
- Personnes envisageant l'introduction de la recherche semantique
- Personnes souhaitant comprendre les fonctionnalites liees a l'IA de Fess

Spectre des technologies de recherche
=======================================

Les technologies de recherche forment un spectre allant du simple au plus avance, comme presente ci-dessous.

.. list-table:: Spectre des technologies de recherche
   :header-rows: 1
   :widths: 20 35 45

   * - Technologie
     - Mecanisme
     - Caracteristiques
   * - Recherche par mots-cles
     - Compare les termes saisis avec les termes des documents
     - Rapide et fiable. Necessite une correspondance exacte des termes
   * - Recherche floue
     - Compare egalement les termes ayant une orthographe similaire
     - Gestion des fautes de frappe
   * - Recherche par synonymes
     - Etend les synonymes pour la comparaison
     - Gestion des variantes de notation (configuration manuelle)
   * - Recherche semantique
     - Compare sur la base de la similarite semantique
     - Trouve des documents lies meme sans correspondance de termes
   * - Recherche hybride
     - Combinaison de la recherche par mots-cles et semantique
     - Exploite les forces des deux approches

Limites de la recherche par mots-cles
=======================================

La recherche par mots-cles est efficace dans de nombreuses situations, mais ses limites apparaissent dans les cas suivants.

Decalage de vocabulaire
-------------------------

Cela se produit lorsque les mots utilises par les utilisateurs different de ceux utilises dans les documents.

Exemple : Meme si un utilisateur recherche "je veux changer la destination du virement de mon salaire", si le document interne utilise le terme "procedure de changement de compte salarial", les mots-cles peuvent ne pas correspondre.

Cela peut etre partiellement resolu avec les synonymes (voir Partie 8), mais il n'est pas realiste d'enregistrer toutes les combinaisons de vocabulaire possibles a l'avance.

Recherche conceptuelle
------------------------

C'est le cas ou les utilisateurs souhaitent effectuer une recherche par concept plutot que par mots-cles specifiques, comme "regles internes sur le teletravail".
Dans ce cas, divers documents lies peuvent etre pertinents, y compris ceux portant sur le "travail a domicile", le "teletravail", les "regles de presence au bureau" et la "gestion du temps de travail".

Fonctionnement de la recherche semantique
============================================

Representation vectorielle (Embedding)
-----------------------------------------

Le fondement de la recherche semantique est la conversion du texte en "vecteurs (tableaux de nombres)".
Ces vecteurs sont des representations mathematiques du "sens" du texte.

Les textes ayant des significations similaires sont places pres les uns des autres dans l'espace vectoriel.
Par exemple, les vecteurs de "chien" et "animal de compagnie" sont proches, tandis que les vecteurs de "chien" et "automobile" sont eloignes.

Fonctionnement de la recherche
---------------------------------

1. L'utilisateur saisit une requete de recherche
2. La requete est convertie en vecteur
3. La similarite avec les vecteurs de documents dans l'index est calculee
4. Les documents sont renvoyes par ordre de similarite decroissante

Cela permet de trouver des documents semantiquement lies meme lorsque les mots-cles ne correspondent pas exactement.

Recherche semantique dans Fess
=================================

Fess peut realiser une recherche basee sur les vecteurs grace a des plugins de recherche semantique.

Activation de la recherche semantique
----------------------------------------

1. Installer le plugin de recherche semantique
2. Configurer le modele d'embedding
3. Reconstruire l'index (vectoriser les documents existants)

Choix du modele d'embedding
------------------------------

Selectionnez un modele (modele d'embedding) pour convertir le texte en vecteurs.

Les criteres de selection sont les suivants :

- **Support linguistique** : Capacite a traiter correctement la langue cible
- **Precision** : Qualite des vecteurs (precision de la capture semantique)
- **Vitesse** : Temps necessaire a la conversion
- **Cout** : Frais d'utilisation de l'API, exigences materielles

Recherche hybride : Rank Fusion
==================================

La recherche semantique est puissante, mais pas omnipotente.
Pour la recherche de noms propres ou dans les cas necessitant une correspondance exacte, la recherche par mots-cles est plus appropriee.

Le concept de recherche hybride
---------------------------------

La recherche hybride execute a la fois la recherche par mots-cles et la recherche semantique, puis integre les resultats.

Fess utilise le Rank Fusion pour fusionner les resultats de differentes methodes de recherche.
Concretement, l'algorithme RRF (Reciprocal Rank Fusion) garantit que les documents bien classes dans les deux resultats de recherche se retrouvent finalement en tete du classement.

Avantages de la recherche hybride
------------------------------------

- Combine la "fiabilite" de la recherche par mots-cles avec la "flexibilite" de la recherche semantique
- Les noms propres sont couverts par la recherche par mots-cles
- Les recherches conceptuelles sont couvertes par la recherche semantique
- La qualite globale de la recherche s'ameliore par rapport a l'utilisation d'une seule methode

Criteres d'adoption
=====================

La recherche semantique ne doit pas necessairement etre introduite dans tous les environnements.

Cas ou l'adoption devrait etre envisagee
-------------------------------------------

- Il y a de nombreuses "requetes sans resultats" dans les journaux de recherche
- Les utilisateurs signalent qu'ils "ne connaissent pas les bons mots-cles"
- Vous souhaitez prendre en charge les questions en langage naturel (un prerequis pour le RAG dans la Partie 19)
- Vous souhaitez ameliorer la recherche interlinguistique pour les documents multilingues

Cas ou elle n'est pas encore necessaire
-----------------------------------------

- Une qualite de recherche suffisante est obtenue avec la recherche par mots-cles + synonymes
- Le nombre de documents est faible et les utilisateurs connaissent les mots-cles appropries
- Les ressources de calcul (GPU ou couts d'API cloud) sont limitees

Adoption progressive
----------------------

1. D'abord, ameliorer la qualite avec la recherche par mots-cles + synonymes (Partie 8)
2. Si les requetes sans resultats restent frequentes, envisager la recherche semantique
3. Utiliser la recherche hybride pour beneficier des deux approches

Resume
=======

Cet article a organise le chemin d'evolution de la recherche par mots-cles vers la recherche semantique.

- Le spectre des technologies de recherche (mots-cles -> floue -> synonymes -> semantique -> hybride)
- Le fonctionnement de la recherche semantique (representation vectorielle et calcul de similarite)
- La recherche semantique et la recherche hybride dans Fess (Rank Fusion)
- Les criteres d'adoption et une approche progressive

Dans le prochain article, nous developperons davantage la recherche semantique et construirons un assistant IA utilisant le RAG.

References
==========

- `Fonctionnalites de recherche IA de Fess <https://fess.codelibs.org/ja/15.5/config/rag-chat.html>`__

- `Recherche vectorielle OpenSearch <https://opensearch.org/docs/latest/search-plugins/knn/>`__
