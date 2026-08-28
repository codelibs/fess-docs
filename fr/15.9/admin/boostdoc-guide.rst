=================
Boost de document
=================

Présentation
============

Cette section explique la configuration du boost de document.
En configurant le boost de document, vous pouvez positionner des documents en haut des résultats de recherche indépendamment du terme de recherche.

Gestion
=======

Affichage
---------

Pour ouvrir la page de liste de configuration du boost de document illustrée ci-dessous, cliquez sur [Robot d'exploration > Boost de document] dans le menu de gauche.

|image0|

Cliquez sur le nom de la configuration pour la modifier.

Création de configuration
-------------------------

Cliquez sur le bouton Nouvelle création pour ouvrir la page de configuration du boost de document.

|image1|

Paramètres de configuration
---------------------------

Condition
:::::::::

Spécifie la condition des documents que vous souhaitez positionner en haut.
Par exemple, pour afficher en haut les URL contenant https://www.n2sm.net/, décrivez url.matches("https://www.n2sm.net/.\*").
Les conditions sont écrites dans la syntaxe du moteur de script spécifié dans « Type de Script » ci-dessous.

Expression de boost
:::::::::::::::::::

Spécifie la valeur de pondération du document.
L'expression est écrite dans la syntaxe du moteur de script spécifié dans « Type de Script » ci-dessous.

Type de Script
::::::::::::::

Spécifie le moteur de script utilisé pour évaluer la condition et l'expression de boost.
Les nouvelles configurations sont préremplies avec ``javascript``. Sélectionner ``groovy`` nécessite
le plugin ``fess-script-groovy``. Si le champ est laissé vide, les expressions sont évaluées en tant que Groovy.

Ordre de tri
::::::::::::

Configure l'ordre de tri du boost de document.

Suppression de configuration
----------------------------

Cliquez sur le nom de la configuration dans la page de liste, puis cliquez sur le bouton Supprimer pour afficher l'écran de confirmation. Appuyer sur le bouton Supprimer supprimera la configuration.


.. |image0| image:: ../../../resources/images/en/15.9/admin/boostdoc-1.png
.. |image1| image:: ../../../resources/images/en/15.9/admin/boostdoc-2.png
