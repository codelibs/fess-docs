===============
Dictionnaire
===============

Présentation
============

Cette section explique les paramètres de configuration concernant les dictionnaires.

Les modifications du dictionnaire doivent être effectuées avec une compréhension des spécifications de chaque dictionnaire.
Un échec lors de la modification du dictionnaire peut rendre l'index inaccessible.

Liste
=====

Pour ouvrir la page de liste des dictionnaires gérables illustrée ci-dessous, cliquez sur [Système > Dictionnaire] dans le menu de gauche.


|image0|


Kuromoji
========

Gère le dictionnaire pour l'analyse morphologique japonaise.
ja/kuromoji.txt est le fichier de dictionnaire pour l'analyse morphologique japonaise.

Synonyme
========

Gère le dictionnaire de synonymes.
synonym.txt est le fichier de dictionnaire de synonymes utilisé en commun pour toutes les langues.

Mapping
=======

Gère le dictionnaire de remplacement de caractères.
mapping.txt est le fichier de dictionnaire de remplacement de mots commun à toutes les langues ou pour chaque langue.

Protwords
=========

Gère le dictionnaire de mots protégés.
protwords.txt est placé pour chaque langue et est un fichier de liste de mots à exclure du stemming.

Mots vides
==========

Gère le dictionnaire de mots vides.
stopwords.txt est placé pour chaque langue et est un fichier de liste de mots à exclure lors de la création de l'index.

Remplacement de Stemmer
========================

Gère le dictionnaire de remplacement de stemmer.
stemmer_override.txt est placé pour chaque langue et est un fichier de dictionnaire de remplacement de mots pour remplacer le traitement de stemming.


.. |image0| image:: ../../../resources/images/en/15.3/admin/dict-1.png
            :height: 940px
