==================================================
Partie 21 : Recherche croisée d'images et de texte
==================================================

Introduction
=============

Dans les articles précédents, nous nous sommes principalement concentrés sur la recherche de documents basés sur du texte.
Cependant, les connaissances d'entreprise comprennent également de nombreux contenus au-delà du texte.
Photos de produits, plans techniques, images de diapositives de présentations, photos de tableaux blancs -- si ces "images" pouvaient également être recherchées, les possibilités d'exploitation des connaissances s'élargiraient considérablement.

Dans cet article, nous présentons comment construire un environnement de recherche multimodale permettant la recherche croisée de texte et d'images.

Public cible
=============

- Les personnes qui rencontrent des difficultés dans la recherche de documents contenant des images
- Les personnes intéressées par les applications de la recherche vectorielle
- Les personnes souhaitant comprendre le concept d'IA multimodale

Qu'est-ce que la recherche multimodale ?
==========================================

La recherche multimodale est une technologie qui permet la recherche croisée entre différents types de données (texte, images, audio, etc.).

Par exemple, lorsque vous recherchez avec le texte "design d'une voiture de sport rouge", les images correspondant conceptuellement s'affichent dans les résultats de recherche.
C'est un mécanisme qui permet de rechercher des images à partir de texte, ou du texte à partir d'images.

Modèle CLIP
-----------

La base de la recherche multimodale repose sur des modèles tels que CLIP (Contrastive Language-Image Pre-Training).
CLIP convertit le texte et les images dans le même espace vectoriel, rendant ainsi possible le calcul de la similarité entre texte et images.

Recherche multimodale dans Fess
==================================

Fess peut réaliser la recherche croisée de texte et d'images grâce à son plugin de recherche multimodale.

Composants
-----------

Les composants de la recherche multimodale sont les suivants :

1. **Serveur CLIP** : Convertit le texte et les images en vecteurs
2. **OpenSearch** : Recherche les vecteurs par KNN (K-Nearest Neighbor)
3. **Fess** : Fournit le crawling, l'indexation et l'interface de recherche

Procédure de configuration
----------------------------

**1. Préparation du serveur CLIP**

Préparez un serveur pour exécuter le modèle CLIP.
Un environnement avec un GPU disponible est recommandé.

Vous pouvez ajouter un serveur CLIP avec Docker Compose.

**2. Installation du plugin**

Installez le plugin de recherche multimodale pour Fess.

**3. Configuration de l'index KNN**

Configurez les paramètres de l'index KNN pour effectuer la recherche vectorielle dans OpenSearch.
Définissez les dimensions du vecteur en fonction du modèle CLIP utilisé.

**4. Configuration du crawl**

Configurez les répertoires et sites web contenant des images comme cibles de crawl.
Les fichiers image (PNG, JPEG, GIF, etc.) sont également collectés comme cibles de crawl.

Expérience de recherche
========================

Rechercher des images avec du texte
--------------------------------------

Lorsque vous recherchez avec du texte tel que "photo extérieure du produit", "tableau blanc de réunion" ou "plan technique", les images correspondant conceptuellement s'affichent dans les résultats de recherche.

Des vignettes sont affichées dans les résultats de recherche, ce qui permet de trouver visuellement les images souhaitées.

Résultats mixtes de texte et d'images
----------------------------------------

Dans la recherche multimodale, les résultats de recherche contiennent un mélange de documents textuels et d'images.
Le Rank Fusion (voir Partie 18) est utilisé pour intégrer les résultats de la recherche textuelle et de la recherche d'images.

Cas d'utilisation
==================

Industrie manufacturière : Recherche d'images de pièces et de produits
------------------------------------------------------------------------

Dans l'industrie manufacturière, un grand nombre de photos de pièces et d'images de produits sont gérées.
En recherchant avec du texte tel que "pièce métallique ronde" ou en recherchant des pièces similaires à partir de la photo d'une pièce spécifique, les ressources de conception antérieures peuvent être exploitées.

Équipes de design : Gestion des ressources de design
-------------------------------------------------------

Les équipes de design gèrent de grands volumes de ressources visuelles telles que des logos, des icônes, des matériaux photographiques et des maquettes.
La recherche avec un langage naturel tel que "fond avec dégradé bleu" facilite la découverte des ressources.

Recherche et développement : Recherche de données expérimentales
------------------------------------------------------------------

Les départements de R&D gèrent des graphiques de résultats expérimentaux, des photos au microscope et des images de données de mesure.
En rendant ces images recherchables, la consultation des données expérimentales antérieures est facilitée.

Considérations pour le déploiement
=====================================

Exigences matérielles
----------------------

La recherche multimodale nécessite des ressources de calcul pour exécuter le modèle CLIP.

- **Recommandé** : Serveur GPU (NVIDIA GPU)
- **Minimum** : Peut fonctionner sur CPU, mais la vitesse d'indexation sera réduite

Le temps d'indexation dépend de la vitesse de traitement du modèle. Un environnement GPU est donc fortement recommandé lors de l'indexation d'un grand nombre d'images.

Formats d'image pris en charge
---------------------------------

Les formats d'image courants (JPEG, PNG, GIF, BMP, TIFF, etc.) sont pris en charge.
La prise en charge des images dans les PDF et des images intégrées dans les documents bureautiques dépend des paramètres de crawl.

Déploiement progressif
------------------------

La recherche multimodale peut être déployée en complément d'un environnement de recherche textuelle existant.

1. Commencez par un déploiement pilote sur les répertoires et sites contenant de nombreuses images
2. Vérifiez la qualité de recherche et l'utilisation
3. Élargissez progressivement le périmètre

Synthèse
=========

Dans cet article, nous avons présenté la recherche croisée d'images et de texte grâce à la recherche multimodale.

- Le concept de recherche multimodale (espace vectoriel unifié pour le texte et les images via CLIP)
- Les composants et la configuration de la recherche multimodale dans Fess
- L'expérience de la recherche d'images par le texte et de la recherche d'images similaires par l'image
- Les cas d'utilisation dans l'industrie manufacturière, le design et la recherche et développement
- Les exigences GPU et une approche de déploiement progressif

Dans le prochain article, nous aborderons la visualisation des connaissances organisationnelles par l'analyse des données de recherche.

Références
==========

- `OpenSearch KNN Search <https://opensearch.org/docs/latest/search-plugins/knn/>`__

- `Fess Plugin Management <https://fess.codelibs.org/ja/15.5/admin/plugin.html>`__
