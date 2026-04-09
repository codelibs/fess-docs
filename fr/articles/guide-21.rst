============================================================
Partie 21 : Recherche croisee d'images et de texte -- Gestion des connaissances de nouvelle generation avec la recherche multimodale
============================================================

Introduction
=============

Dans les articles precedents, nous nous sommes principalement concentres sur la recherche de documents bases sur du texte.
Cependant, les connaissances d'entreprise comprennent egalement de nombreux contenus au-dela du texte.
Photos de produits, plans techniques, images de diapositives de presentations, photos de tableaux blancs -- si ces "images" pouvaient egalement etre recherchees, les possibilites d'exploitation des connaissances s'elargiraient considerablement.

Dans cet article, nous presentons comment construire un environnement de recherche multimodale permettant la recherche croisee de texte et d'images.

Public cible
=============

- Les personnes qui rencontrent des difficultes dans la recherche de documents contenant des images
- Les personnes interessees par les applications de la recherche vectorielle
- Les personnes souhaitant comprendre le concept d'IA multimodale

Qu'est-ce que la recherche multimodale ?
==========================================

La recherche multimodale est une technologie qui permet la recherche croisee entre differents types de donnees (texte, images, audio, etc.).

Par exemple, lorsque vous recherchez avec le texte "design d'une voiture de sport rouge", les images correspondant conceptuellement s'affichent dans les resultats de recherche.
C'est un mecanisme qui permet de rechercher des images a partir de texte, ou du texte a partir d'images.

Modele CLIP
-----------

La base de la recherche multimodale repose sur des modeles tels que CLIP (Contrastive Language-Image Pre-Training).
CLIP convertit le texte et les images dans le meme espace vectoriel, rendant ainsi possible le calcul de la similarite entre texte et images.

Recherche multimodale dans Fess
==================================

Fess peut realiser la recherche croisee de texte et d'images grace a son plugin de recherche multimodale.

Composants
-----------

Les composants de la recherche multimodale sont les suivants :

1. **Serveur CLIP** : Convertit le texte et les images en vecteurs
2. **OpenSearch** : Recherche les vecteurs par KNN (K-Nearest Neighbor)
3. **Fess** : Fournit le crawling, l'indexation et l'interface de recherche

Procedure de configuration
----------------------------

**1. Preparation du serveur CLIP**

Preparez un serveur pour executer le modele CLIP.
Un environnement avec un GPU disponible est recommande.

Vous pouvez ajouter un serveur CLIP avec Docker Compose.

**2. Installation du plugin**

Installez le plugin de recherche multimodale pour Fess.

**3. Configuration de l'index KNN**

Configurez les parametres de l'index KNN pour effectuer la recherche vectorielle dans OpenSearch.
Definissez les dimensions du vecteur en fonction du modele CLIP utilise.

**4. Configuration du crawl**

Configurez les repertoires et sites web contenant des images comme cibles de crawl.
Les fichiers image (PNG, JPEG, GIF, etc.) sont egalement collectes comme cibles de crawl.

Experience de recherche
========================

Rechercher des images avec du texte
--------------------------------------

Lorsque vous recherchez avec du texte tel que "photo exterieure du produit", "tableau blanc de reunion" ou "plan technique", les images correspondant conceptuellement s'affichent dans les resultats de recherche.

Des vignettes sont affichees dans les resultats de recherche, ce qui permet de trouver visuellement les images souhaitees.

Resultats mixtes de texte et d'images
----------------------------------------

Dans la recherche multimodale, les resultats de recherche contiennent un melange de documents textuels et d'images.
Le Rank Fusion (voir Partie 18) est utilise pour integrer les resultats de la recherche textuelle et de la recherche d'images.

Cas d'utilisation
==================

Industrie manufacturiere : Recherche d'images de pieces et de produits
------------------------------------------------------------------------

Dans l'industrie manufacturiere, un grand nombre de photos de pieces et d'images de produits sont gerees.
En recherchant avec du texte tel que "piece metallique ronde" ou en recherchant des pieces similaires a partir de la photo d'une piece specifique, les ressources de conception anterieures peuvent etre exploitees.

Equipes de design : Gestion des ressources de design
-------------------------------------------------------

Les equipes de design gerent de grands volumes de ressources visuelles telles que des logos, des icones, des materiaux photographiques et des maquettes.
La recherche avec un langage naturel tel que "fond avec degrade bleu" facilite la decouverte des ressources.

Recherche et developpement : Recherche de donnees experimentales
------------------------------------------------------------------

Les departements de R&D gerent des graphiques de resultats experimentaux, des photos au microscope et des images de donnees de mesure.
En rendant ces images recherchables, la consultation des donnees experimentales anterieures est facilitee.

Considerations pour le deploiement
=====================================

Exigences materielles
----------------------

La recherche multimodale necessite des ressources de calcul pour executer le modele CLIP.

- **Recommande** : Serveur GPU (NVIDIA GPU)
- **Minimum** : Peut fonctionner sur CPU, mais la vitesse d'indexation sera reduite

Le temps d'indexation depend de la vitesse de traitement du modele. Un environnement GPU est donc fortement recommande lors de l'indexation d'un grand nombre d'images.

Formats d'image pris en charge
---------------------------------

Les formats d'image courants (JPEG, PNG, GIF, BMP, TIFF, etc.) sont pris en charge.
La prise en charge des images dans les PDF et des images integrees dans les documents bureautiques depend des parametres de crawl.

Deploiement progressif
------------------------

La recherche multimodale peut etre deployee en complement d'un environnement de recherche textuelle existant.

1. Commencez par un deploiement pilote sur les repertoires et sites contenant de nombreuses images
2. Verifiez la qualite de recherche et l'utilisation
3. Elargissez progressivement le perimetre

Synthese
=========

Dans cet article, nous avons presente la recherche croisee d'images et de texte grace a la recherche multimodale.

- Le concept de recherche multimodale (espace vectoriel unifie pour le texte et les images via CLIP)
- Les composants et la configuration de la recherche multimodale dans Fess
- L'experience de la recherche d'images par le texte et de la recherche d'images similaires par l'image
- Les cas d'utilisation dans l'industrie manufacturiere, le design et la recherche et developpement
- Les exigences GPU et une approche de deploiement progressif

Dans le prochain article, nous aborderons la visualisation des connaissances organisationnelles par l'analyse des donnees de recherche.

References
==========

- `OpenSearch KNN Search <https://opensearch.org/docs/latest/search-plugins/knn/>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
